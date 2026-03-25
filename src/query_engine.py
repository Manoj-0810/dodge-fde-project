import re
import json
import streamlit as st
from graph_builder import G, get_billing_from_sales_order

# ---------------- LLM SETUP ----------------
USE_LLM = False

try:
    import google.generativeai as genai

    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        MODEL = genai.GenerativeModel("gemini-2.5-flash")
        USE_LLM = True
except:
    USE_LLM = False


# ---------------- GUARDRAILS ----------------
def is_valid_query(query):
    keywords = ["sales", "order", "billing", "delivery", "flow", "top", "broken"]
    return any(k in query.lower() for k in keywords)


# ---------------- LLM PARSER ----------------
def extract_with_llm(query):
    if not USE_LLM:
        return None, None

    prompt = f"""
    Extract intent and sales_order_id from this ERP query.

    Query: "{query}"

    Return ONLY JSON:
    {{
        "intent": "...",
        "sales_order_id": "..."
    }}

    Possible intents:
    - trace_flow
    - billing_lookup
    - broken_flow
    - top_orders
    - top_billed_orders
    """

    try:
        response = MODEL.generate_content(prompt)
        text = response.text.strip()

        json_start = text.find("{")
        json_text = text[json_start:]

        data = json.loads(json_text)

        return data.get("intent"), data.get("sales_order_id")

    except:
        return None, None


# ---------------- RULE-BASED FALLBACK ----------------
def extract_rule_based(query):
    query = query.lower()

    so_match = re.findall(r"\d+", query)
    so_id = so_match[0] if so_match else None

    if "highest" in query and "billing" in query:
        return "top_billed_orders", None

    elif "top" in query and "billing" in query:
        return "top_billed_orders", None

    elif "trace" in query:
        return "trace_flow", so_id

    elif "billing" in query or "invoice" in query:
        return "billing_lookup", so_id

    elif "broken" in query:
        return "broken_flow", so_id

    elif "top" in query:
        return "top_orders", None

    return None, None


# ---------------- CORE FUNCTIONS ----------------
def trace_flow(graph, so_id):
    if not so_id:
        return {"text": "Please provide a valid Sales Order ID", "flow": []}

    so_node = f"SO_{so_id}"

    if so_node not in graph:
        return {"text": f"Sales Order {so_id} not found", "flow": []}

    deliveries = list(graph.successors(so_node))

    if not deliveries:
        return {"text": f"No delivery found for Sales Order {so_id}", "flow": []}

    flow_nodes = [so_node]
    response = f"Flow for Sales Order {so_id}:\n"

    for d in deliveries:
        flow_nodes.append(d)
        bills = list(graph.successors(d))
        d_id = d.replace("D_", "")

        if bills:
            for b in bills:
                flow_nodes.append(b)

            b_ids = [b.replace("B_", "") for b in bills]
            response += f"• Delivery {d_id} → Billing {', '.join(b_ids)}\n"
        else:
            response += f"• Delivery {d_id} → Not billed\n"

    return {"text": response, "flow": flow_nodes}


# 🔥 FIXED
def get_top_orders(graph):
    orders = []

    for node, data in graph.nodes(data=True):
        if data.get("type") == "SalesOrder":
            amount = data.get("amount", 0)
            orders.append((node, amount))

    orders.sort(key=lambda x: x[1], reverse=True)

    response = "Top Sales Orders:\n"
    flow_nodes = []

    for node, amt in orders[:5]:
        so_id = node.replace("SO_", "")
        response += f"• {so_id} → {amt}\n"
        flow_nodes.append(node)

    return {"text": response, "flow": flow_nodes}


# 🔥 FIXED
def get_top_billed_orders(graph):
    counts = {}

    for node in graph.nodes:
        if node.startswith("SO_"):
            deliveries = list(graph.successors(node))
            bill_count = 0

            for d in deliveries:
                bills = list(graph.successors(d))
                bill_count += len(bills)

            counts[node] = bill_count

    sorted_orders = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:5]

    response = "Top Sales Orders by Billing Count:\n"
    flow_nodes = []

    for so, count in sorted_orders:
        so_id = so.replace("SO_", "")
        response += f"• {so_id} → {count} billings\n"
        flow_nodes.append(so)

    return {"text": response, "flow": flow_nodes}


def find_broken_flow(graph, so_id):
    if not so_id:
        return {"text": "Please provide a valid Sales Order ID", "flow": []}

    so_node = f"SO_{so_id}"

    if so_node not in graph:
        return {"text": f"Sales Order {so_id} not found", "flow": []}

    deliveries = list(graph.successors(so_node))

    if not deliveries:
        return {"text": f"Broken flow: No delivery for Sales Order {so_id}", "flow": [so_node]}

    for d in deliveries:
        if not list(graph.successors(d)):
            return {"text": f"Broken flow: Delivery exists but not billed for Sales Order {so_id}", "flow": [so_node, d]}

    return {"text": f"Sales Order {so_id} has complete flow", "flow": [so_node]}


# ---------------- MAIN HANDLER ----------------
def handle_query(query):

    if not is_valid_query(query):
        return {"text": "This system is designed to answer ERP dataset-related queries only.", "flow": []}

    intent, so_id = extract_with_llm(query)

    if not intent:
        intent, so_id = extract_rule_based(query)

    if not intent:
        return {"text": "Could not understand the query", "flow": []}

    if intent == "trace_flow":
        return trace_flow(G, so_id)

    elif intent == "billing_lookup":
        result = get_billing_from_sales_order(G, so_id)

        if not result:
            return {"text": f"No billing found for Sales Order {so_id}", "flow": []}

        flow_nodes = [f"SO_{so_id}"] + result

        return {"text": f"Billing documents: {result}", "flow": flow_nodes}

    elif intent == "broken_flow":
        return find_broken_flow(G, so_id)

    elif intent == "top_orders":
        return get_top_orders(G)

    elif intent == "top_billed_orders":
        return get_top_billed_orders(G)

    return {"text": "Query not supported", "flow": []}


# ---------------- MULTI QUERY ----------------
def handle_multi_query(query):
    queries = [q.strip() for q in query.split(",") if q.strip()]

    all_text = []
    all_flow = []

    for q in queries:
        res = handle_query(q)
        all_text.append(res["text"])
        all_flow.extend(res["flow"])

    return {"text": "\n\n".join(all_text), "flow": all_flow}
