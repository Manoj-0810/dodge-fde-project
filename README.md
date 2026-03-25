# 🚀 ERP Graph Assistant

An interactive **graph-based ERP analytics system** that enables users to explore Order-to-Cash (O2C) business processes using **natural language queries** and **visual graph exploration**.

---

## 🧠 Overview

This project models ERP transactional data as a **directed graph** and provides:

* 🔍 Conversational query interface (NL → Graph operations)
* 📊 Graph-based reasoning over business flows
* 🎯 Visual highlighting of queried entities
* ⚡ Hybrid LLM + rule-based query processing
* 💾 Cached graph for performance

---

## 🏗️ System Architecture

```
User Query (Natural Language)
        ↓
LLM Parser  + Rule-Based Fallback
        ↓
Query Engine (Intent → Graph Traversal / Aggregation)
        ↓
NetworkX Graph (In-Memory + Cached)
        ↓
Streamlit UI (Chat + Interactive Graph)
```

---

## 📊 Graph Modelling

### 🔹 Nodes (Entities)

* **Sales Orders** (`SO_*`)
* **Deliveries** (`D_*`)
* **Billing Documents** (`B_*`)

### 🔹 Edges (Relationships)

* Sales Order → Delivery
* Delivery → Billing

👉 This directly models the **ERP Order-to-Cash lifecycle**

---

## 💾 Database / Storage Design

* Graph stored using **NetworkX (in-memory)**
* Added **persistent caching (`graph.pkl`)**

  * First run → builds graph
  * Subsequent runs → loads cached graph
* Design allows easy migration to:

  * Neo4j
  * Graph databases at scale

---

## 🤖 LLM Integration & Prompting

* Uses **Gemini (free tier)** for intent extraction
* Converts natural language → structured JSON

### Example:

```
Input:
trace flow for sales order 740573

Output:
{
  "intent": "trace_flow",
  "sales_order_id": "740573"
}
```

### 🔁 Hybrid Design

* LLM → primary parsing
* Rule-based → fallback

👉 Ensures:

* Reliability
* No dependency on API availability

---

## 🛡️ Guardrails

The system restricts queries to ERP domain only.

### Example:

```
Input:
who is the president of india

Output:
This system is designed to answer ERP dataset-related queries only.
```

👉 Prevents:

* Hallucinations
* Irrelevant responses

---

## 💬 Conversational Query Interface

### Supported Queries

#### 🔹 Flow Analysis

* `trace flow for sales order 740573`

#### 🔹 Billing Lookup

* `show billing for sales order 740573`

#### 🔹 Broken Flow Detection

* `find broken flow for sales order 740573`

#### 🔹 Aggregation Queries

* `show me top orders`
* `which sales orders have highest billing count`

#### 🔹 Multi-Query Support

* `trace flow for sales order 740573, show me top orders`

---

## 📈 Graph Visualization & Chat Integration

This is a **core highlight of the system** ⭐

### 🔗 Chat ↔ Graph Integration

* User query → processed by query engine
* Engine returns:

  * Text response
  * **List of relevant graph nodes (`flow_nodes`)**

---

### 🔴 Dynamic Node Highlighting

Based on query results:

| Query Type       | Highlight Behavior                  |
| ---------------- | ----------------------------------- |
| Flow Trace       | Full path (SO → Delivery → Billing) |
| Billing Lookup   | Sales Order + Billing nodes         |
| Top Orders       | Top Sales Order nodes               |
| Advanced Queries | Relevant Sales Orders               |
| Broken Flow      | Problematic nodes                   |

👉 Highlighted nodes:

* Colored **red**
* Increased size
* Connected edges emphasized

---

### 🧩 Interactive Features

* Click nodes → view metadata
* Color-coded entities:

  * Blue → Sales Orders
  * Orange → Deliveries
  * Green → Billing
  * Red → Query result

---

## 🧪 Key Features

* ✅ Graph-based ERP modeling
* ✅ Conversational querying
* ✅ LLM + rule-based hybrid system
* ✅ Multi-query support
* ✅ Graph traversal & analytics
* ✅ Dynamic graph highlighting
* ✅ Persistent caching
* ✅ Clean UI with Streamlit

---

## 📁 Project Structure

```
├── src/
│   ├── app.py
│   ├── graph_builder.py
│   ├── query_engine.py
│   └── utils/
│       └── graph_visualization.py
├── dataset_sample/
├── ai_logs/
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Setup Instructions

### 1️⃣ Install dependencies

```
pip install -r requirements.txt
```

### 2️⃣ Run application

```
streamlit run src/app.py
```

---

## 🌐 Deployment

* Deployed using **Streamlit Cloud**
* Uses `dataset_sample` for lightweight execution
* Supports optional LLM integration via API key

---

## 🧠 Design Decisions

* Used NetworkX for simplicity and flexibility
* Hybrid query parsing ensures robustness
* Focused on **data-grounded responses** (no hallucination)
* Added caching for performance optimization
* Designed UI for **graph + chat synergy**

---

## 🚀 Evaluation Criteria Coverage

| Area               | Implementation                      |
| ------------------ | ----------------------------------- |
| Code Quality       | Modular structure, clean separation |
| Graph Modelling    | Clear entities and relationships    |
| Database / Storage | Graph caching + scalable design     |
| LLM Integration    | Structured parsing + fallback       |
| Guardrails         | Strict domain restriction           |

---

## 📌 Conclusion

This project demonstrates how structured ERP data can be transformed into an **interactive, queryable graph system**, combining:

* Graph analytics
* Natural language interfaces
* Visual exploration

👉 Designed with **real-world system thinking and scalability in mind**

---

## 👨‍💻 Author

**Manoj RS**
