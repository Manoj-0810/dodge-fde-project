import streamlit as st
from graph_builder import G, get_billing_from_sales_order
from utils.graph_visualization import nx_to_agraph
from streamlit_agraph import agraph, Config
from query_engine import handle_multi_query
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

        if not is_valid_query(user_input):
            response_text = "This system is designed to answer ERP dataset-related queries only."
            st.session_state.messages.append(f"User: {user_input}")
            st.session_state.messages.append(f"System: {response_text}")
            st.rerun()

        # ✅ FIX: Correct handling of response
        result = handle_multi_query(user_input)

        response_text = result["text"]
        st.session_state.flow_nodes = result["flow"]  # 🔴 RESTORES HIGHLIGHT

        st.session_state.messages.append(f"User: {user_input}")
        st.session_state.messages.append(f"System: {response_text}")

        st.rerun()