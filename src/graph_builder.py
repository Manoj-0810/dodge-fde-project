import os
import json
import networkx as nx
import pickle

BASE_PATH = "dataset_sample"


# ---------------- HELPERS ----------------
def read_jsonl(folder_path):
    data = []
    for file in os.listdir(folder_path):
        if file.endswith(".jsonl"):
            path = os.path.join(folder_path, file)
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        data.append(json.loads(line))
                    except:
                        continue
    return data


# ---------------- BUILD GRAPH ----------------
def build_graph():
    G = nx.DiGraph()

    # ---------------- LOAD DATA ----------------
    sales_orders = read_jsonl(os.path.join(BASE_PATH, "sales_order_headers"))
    delivery_items = read_jsonl(os.path.join(BASE_PATH, "outbound_delivery_items"))
    deliveries = read_jsonl(os.path.join(BASE_PATH, "outbound_delivery_headers"))
    billing_items = read_jsonl(os.path.join(BASE_PATH, "billing_document_items"))
    billings = read_jsonl(os.path.join(BASE_PATH, "billing_document_headers"))

    # ---------------- ADD NODES ----------------

    # 🔹 Sales Orders
    for so in sales_orders:
        so_id = so.get("salesOrder")
        if so_id:
            G.add_node(
                f"SO_{so_id}",
                type="SalesOrder",
                amount=so.get("totalNetAmount"),
                customer=so.get("soldToParty"),
                date=so.get("creationDate"),
            )

    # 🔹 Deliveries
    for d in deliveries:
        d_id = d.get("deliveryDocument")
        if d_id:
            G.add_node(
                f"D_{d_id}",
                type="Delivery",
                shipping_point=d.get("shippingPoint"),
                date=d.get("actualGoodsMovementDate"),
            )

    # 🔹 Billing Documents
    for b in billings:
        b_id = b.get("billingDocument")
        if b_id:
            G.add_node(
                f"B_{b_id}",
                type="Billing",
                amount=b.get("totalNetAmount"),
                billing_type=b.get("billingDocumentType"),
                date=b.get("billingDocumentDate"),
            )

    # ---------------- ADD EDGES ----------------

    # 🔹 Sales Order → Delivery
    for di in delivery_items:
        so_id = di.get("referenceSdDocument")
        d_id = di.get("deliveryDocument")

        if so_id and d_id:
            G.add_edge(
                f"SO_{so_id}",
                f"D_{d_id}",
                type="SO_TO_DELIVERY"
            )

    # 🔹 Delivery → Billing
    for bi in billing_items:
        d_id = bi.get("referenceSdDocument")
        b_id = bi.get("billingDocument")

        if d_id and b_id:
            G.add_edge(
                f"D_{d_id}",
                f"B_{b_id}",
                type="DELIVERY_TO_BILLING"
            )

    return G


# ---------------- LOAD OR CACHE GRAPH ----------------
def load_or_build_graph():
    if os.path.exists("graph.pkl"):
        with open("graph.pkl", "rb") as f:
            return pickle.load(f)

    G = build_graph()

    with open("graph.pkl", "wb") as f:
        pickle.dump(G, f)

    return G


# ---------------- INITIALIZE GRAPH ----------------
G = load_or_build_graph()


# ---------------- QUERY FUNCTION ----------------
def get_billing_from_sales_order(graph, sales_order_id):
    so_node = f"SO_{sales_order_id}"

    if so_node not in graph:
        return []

    result = []
    deliveries = list(graph.successors(so_node))

    for d in deliveries:
        bills = list(graph.successors(d))
        result.extend(bills)

    return result