# 🚀 Context Graph + LLM Query System for ERP Data

## 📌 Overview

This project implements a **Context Graph-based reasoning system** over ERP Order-to-Cash data, combined with a **Large Language Model (LLM)** interface for natural language querying.

Instead of writing SQL or navigating complex schemas, users can directly ask:

> *"Give me invoices for order 740509"*

and receive structured results instantly.

---

## 🎯 Key Idea

ERP systems are inherently **relational and multi-hop**:

* Orders → Deliveries → Billing → Payments

Traditional querying is rigid and unintuitive.

👉 This project converts ERP data into a **graph representation** and layers an **LLM-driven query interface** on top.

---

## 🧠 Architecture

```id="arch1"
User Query (Natural Language)
        ↓
Gemini LLM (Intent + Entity Extraction)
        ↓
Query Engine (Python)
        ↓
Context Graph (NetworkX)
        ↓
ERP Data Traversal
        ↓
Response (UI / CLI)
```

---

## 🔗 Graph Modeling

We model ERP as a **directed graph**:

### Nodes

* SalesOrder (`SO_xxx`)
* Delivery (`D_xxx`)
* Billing (`B_xxx`)

### Edges

* SalesOrder → Delivery
* Delivery → Billing

This enables natural traversal:

```id="flow1"
SalesOrder → Delivery → Billing
```

---

## 🤖 LLM Integration (Gemini 2.5 Flash)

We use **Gemini 2.5 Flash** to:

* Interpret natural language queries
* Extract structured intent
* Map queries to graph operations

### Example

Input:

```id="ex1"
give me invoices for order 740509
```

LLM Output (parsed):

```id="ex2"
intent = get_billing
sales_order_id = 740509
```

---

## ⚙️ Tech Stack

* Python
* NetworkX (Graph modeling)
* Streamlit (UI)
* Google Gemini API (LLM reasoning)

---

## 🧪 Example Queries

* show billing for sales order 740509
* give me invoices for order 740509
* what billing docs are linked to 740509

---

## 📊 Example Output

```id="out1"
billing documents: ['B_90504204', 'B_91150217']
```

---

## 🧠 Design Decisions

### 1. Graph over Relational Queries

Multi-hop traversal becomes simpler and more intuitive than SQL joins.

### 2. LLM for Query Understanding

Avoids rigid keyword parsing and supports flexible phrasing.

### 3. Modular System Design

* Graph layer
* Query engine
* LLM interface
* UI layer

---

## ⚠️ Limitations

* Limited query types (currently billing-focused)
* In-memory graph (no persistence)
* Basic LLM parsing (can be extended)

---

## 🔮 Future Improvements

* Add Payments and Customer nodes
* Multi-hop reasoning (Order → Payment)
* Graph visualization (interactive)
* Conversational memory (chat history)

---

## 🚀 How to Run

### Install dependencies

```id="run1"
pip install networkx streamlit google-genai
```

### Add API Key

```id="run2"
client = genai.Client(api_key="YOUR_API_KEY")
```

### Run backend

```id="run3"
python src/query_engine.py
```

### Run UI

```id="run4"
streamlit run src/app.py
```

---

## 🏁 Conclusion

This system demonstrates how **graph-based data modeling + LLM reasoning** can transform how users interact with complex enterprise systems.

---

## 👨‍💻 Author

Manoj RS
B.E. Electronics and Communication Engineering
AI/ML Enthusiast
