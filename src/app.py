import streamlit as st
from graph_builder import G, get_billing_from_sales_order
from utils.graph_visualization import nx_to_agraph
from streamlit_agraph import agraph, Config
import re

# ---------------- CONFIG ----------------
st.set_page_config(page_title="ERP Graph Assistant", layout="wide")
st.title("ERP Graph Assistant")

# ---------------- SESSION ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_node" not in st.session_state:
    st.session_state.selected_node = None

if "flow_nodes" not in st.session_state:
    st.session_state.flow_nodes = []

# ---------------- GUARDRAIL ----------------
def is_valid_query(user_input):
    keywords = ["sales", "order", "delivery", "billing", "flow", "top"]
    return any(k in user_input.lower() for k in keywords)

# ---------------- PARSER ----------------
def llm_to_query(user_input):
    parts = re.split(r",| and ", user_input.lower())
    queries = []

    for part in parts:
        numbers = re.findall(r"\d+", part)

        if "top" in part and "order" in part:
            queries.append({"type": "top_orders"})
            continue

        if not numbers:
            continue

        if "trace" in part:
            t = "trace_flow"
        elif "broken" in part:
            t = "broken_flow"
        else:
            t = "billing"

        queries.append({"type": t, "sales_order_id": numbers[0]})

    return queries

# ---------------- RESPONSE (STANDARDIZED) ----------------
def format_trace(so, deliveries):
    if not deliveries:
        return f"Flow for Sales Order {so}:\n\n• No deliveries found"

    text = f"Flow for Sales Order {so}:\n\n"

    for d, bills in deliveries:
        d_id = d.split("_")[1]

        if bills:
            bills_clean = ", ".join([b.split("_")[1] for b in bills])
            text += f"• Delivery {d_id} → Billing {bills_clean}\n"
        else:
            text += f"• Delivery {d_id} → No billing\n"

    return text

# ---------------- QUERY ----------------
def execute_query(q):

    # TOP ORDERS
    if q["type"] == "top_orders":
        so_nodes = [n for n in G.nodes if n.startswith("SO_")]

        orders = []
        for so in so_nodes:
            amount = G.nodes[so].get("amount", 0)
            if amount:
                try:
                    orders.append((so, float(amount)))
                except:
                    continue

        top = sorted(orders, key=lambda x: x[1], reverse=True)[:5]

        if not top:
            return {"text": "Top Orders:\n\n• No data available", "flow": []}

        text = "Top Orders:\n\n"
        for so, amt in top:
            text += f"• {so.split('_')[1]} → {amt}\n"

        return {"text": text, "flow": [so for so, _ in top]}

    so = q["sales_order_id"]
    so_node = f"SO_{so}"

    if so_node not in G:
        return {"text": f"Sales Order {so} not found", "flow": []}

    if q["type"] == "trace_flow":
        deliveries = list(G.successors(so_node))

        flow_nodes = [so_node]
        delivery_data = []

        for d in deliveries:
            bills = list(G.successors(d))
            delivery_data.append((d, bills))
            flow_nodes.append(d)
            flow_nodes.extend(bills)

        return {"text": format_trace(so, delivery_data), "flow": flow_nodes}

    if q["type"] == "billing":
        bills = get_billing_from_sales_order(G, so)

        if bills:
            readable = ", ".join([b.split("_")[1] for b in bills])
            return {
                "text": f"Billing for Sales Order {so}:\n\n• {readable}",
                "flow": bills
            }
        else:
            return {
                "text": f"Billing for Sales Order {so}:\n\n• No billing found",
                "flow": []
            }

    if q["type"] == "broken_flow":
        deliveries = list(G.successors(so_node))
        broken = []

        for d in deliveries:
            if not list(G.successors(d)):
                broken.append(d)

        if broken:
            readable = ", ".join([d.split("_")[1] for d in broken])
            return {
                "text": f"Broken Flow for Sales Order {so}:\n\n• {readable}",
                "flow": broken
            }
        else:
            return {
                "text": f"Broken Flow for Sales Order {so}:\n\n• No issues",
                "flow": []
            }

    return {"text": "Unsupported query", "flow": []}

# ---------------- COLOR ----------------
def apply_node_colors(nodes):
    for node in nodes:
        if node.id.startswith("SO_"):
            node.color = "#3b82f6"
        elif node.id.startswith("D_"):
            node.color = "#f59e0b"
        elif node.id.startswith("B_"):
            node.color = "#10b981"
    return nodes

# ---------------- HIGHLIGHT ----------------
def highlight(nodes, edges, flow_nodes):
    for node in nodes:
        if node.id in flow_nodes:
            node.color = "#ef4444"
            node.size = 30

    for edge in edges:
        if edge.source in flow_nodes and edge.to in flow_nodes:
            edge.color = "#ef4444"

    return nodes, edges

# ---------------- LAYOUT ----------------
left, right = st.columns([2, 1])

# -------- GRAPH --------
with left:
    st.subheader("Graph")

    nodes, edges = nx_to_agraph(G)
    nodes = apply_node_colors(nodes)

    if st.session_state.flow_nodes:
        nodes, edges = highlight(nodes, edges, st.session_state.flow_nodes)

    selected = agraph(
        nodes=nodes,
        edges=edges,
        config=Config(width=800, height=500, directed=True)
    )

    if selected:
        st.session_state.selected_node = selected

    if st.session_state.selected_node:
        data = G.nodes[st.session_state.selected_node]

        clean = {}
        for k, v in data.items():
            if v:
                if "date" in k.lower():
                    v = str(v).replace("T", " ").replace("Z", "")
                clean[k.replace("_", " ").title()] = v

        st.subheader(f"Node Details: {st.session_state.selected_node}")
        st.json(clean)

# -------- CHAT --------
with right:
    st.subheader("Chat")

    chat_box = st.container()

    with chat_box:
        for msg in st.session_state.messages:
            st.write(msg)

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Type your query")
        submitted = st.form_submit_button("Send")

    if submitted and user_input:
        st.session_state.flow_nodes = []

        if not is_valid_query(user_input):
            response_text = "This system is designed to answer ERP dataset-related queries only."
            st.session_state.messages.append(f"User: {user_input}")
            st.session_state.messages.append(f"System: {response_text}")
            st.rerun()

        queries = llm_to_query(user_input)

        all_text = []
        all_flow = []

        for q in queries:
            res = execute_query(q)
            all_text.append(res["text"])
            all_flow.extend(res["flow"])

        st.session_state.flow_nodes = all_flow

        st.session_state.messages.append(f"User: {user_input}")
        st.session_state.messages.append(f"System: {' '.join(all_text)}")

        st.rerun()