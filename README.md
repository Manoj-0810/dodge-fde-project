# 🚀 ERP Graph Assistant

An interactive system that models SAP Order-to-Cash (O2C) data as a graph and enables users to query it using natural language. The system combines graph-based reasoning, structured query translation, and visualization to provide accurate, data-grounded insights.

---

## 🧠 Overview

This project transforms ERP transactional data into a **directed graph** and allows users to:

- Explore relationships between business entities
- Query the system using natural language
- Visualize process flows interactively
- Detect incomplete or broken workflows

---

## 🏗️ Architecture

### 🔹 Core Components

1. **Graph Layer (NetworkX)**
   - Constructs a directed graph from SAP O2C dataset
   - Nodes represent entities
   - Edges represent relationships

2. **Visualization Layer (Streamlit + AGraph)**
   - Interactive graph rendering
   - Node selection and metadata inspection
   - Dynamic highlighting of flows

3. **Query Engine**
   - Converts natural language → structured queries
   - Executes graph traversal logic
   - Returns deterministic, data-backed results

4. **UI Layer (Streamlit)**
   - Left panel: Graph visualization
   - Right panel: Chat interface

---

## 📊 Graph Modeling

### 🔹 Nodes (Entities)

| Entity Type   | Representation |
|--------------|--------------|
| Sales Order  | `SO_<id>` |
| Delivery     | `D_<id>` |
| Billing      | `B_<id>` |

Each node contains metadata such as:
- Amount
- Type
- Billing type
- Date

---

### 🔹 Edges (Relationships)

- `Sales Order → Delivery`
- `Delivery → Billing`

This models the real-world ERP flow:

Sales Order → Delivery → Billing

---

### 🔹 Why Graph?

Graph modeling enables:
- Easy traversal of business flows
- Relationship-based queries
- Efficient detection of missing links (broken flows)

---

## 📈 Graph Visualization

The system uses **streamlit-agraph** for interactive visualization.

### 🔹 Features

- Interactive node graph
- Click any node → inspect metadata
- Directed edges show process flow
- Color-coded entities:
  - 🔵 Sales Orders
  - 🟠 Deliveries
  - 🟢 Billing

---

### 🔥 Flow Highlighting (Key Feature)

When a user queries a flow:

1. Relevant nodes are identified via graph traversal  
2. These nodes are stored in session state (`flow_nodes`)  
3. During rendering:
   - Matching nodes are highlighted in **red**
   - Edges between them are also highlighted  

This creates a **visual trace of the query result directly on the graph**

---

## 💬 Conversational Query System

### 🔹 How It Works

1. User inputs natural language query  
2. Query is parsed into structured format  
3. Query is executed on the graph  
4. Results are returned in human-readable form  

---

### 🔹 Query Translation

Example:

"trace flow for sales order 740573"

↓

{
  "type": "trace_flow",
  "sales_order_id": "740573"
}

---

### 🔹 Supported Queries

- Trace full process flow  
- Retrieve billing documents  
- Detect broken/incomplete flows  
- Top sales orders by value  
- Multi-query support (comma-separated)  

---

### 🔹 Multi-Query Handling

Example:

trace flow for sales order 740573, show me top orders

- Input is split into multiple sub-queries  
- Each query is executed independently  
- Results are aggregated into a single response  
- Graph highlights all relevant nodes  

---

## 🧾 Response Design

Responses are:
- Deterministic (no hallucination)  
- Fully grounded in dataset  
- Structured and consistent  

Example:

Flow for Sales Order 740573:

• Delivery 80738093 → Billing 91150165, 90504277

---

## 🛡️ Guardrails

To prevent misuse, the system enforces domain restrictions.

### 🔹 Implementation

- Keyword-based filtering  
- Rejects non-ERP queries  

Example:

User: who is the president of india  
System: This system is designed to answer ERP dataset-related queries only.

---

## ⚙️ Design Decisions

### 🔹 Why NetworkX?

- Lightweight and easy to use  
- Ideal for prototyping graph-based systems  
- Supports traversal and relationship queries  

### 🔹 Tradeoff

- Not scalable for very large datasets  
- Production alternative: **Neo4j / graph databases**  

---

### 🔹 Why Not Full LLM Integration?

Instead of relying on LLM APIs:

- Used rule-based parsing for reliability  
- Ensures zero hallucination  
- Guarantees deterministic outputs  

---

## 📦 Tech Stack

- Python  
- NetworkX  
- Streamlit  
- streamlit-agraph  

---

## 🚀 Features Summary

| Feature | Status |
|--------|--------|
| Graph Modeling | ✅ |
| Interactive Visualization | ✅ |
| Node Metadata Inspection | ✅ |
| Flow Highlighting | ✅🔥 |
| Natural Language Queries | ✅ |
| Multi-Query Support | ✅ |
| Guardrails | ✅ |
| Broken Flow Detection | ✅ |
| Top Orders Analysis | ✅ |

---

## 🧪 Example Queries

trace flow for sales order 740573  
show billing for sales order 740573  
find broken flow for sales order 740573  
show me top orders  
trace flow for sales order 740573, show me top orders  

---

## 📁 Project Structure

src/
├── app.py  
├── graph_builder.py  
├── query_engine.py  
├── utils/  
│   └── graph_visualization.py  

---

## 📊 Future Improvements

- Product-level aggregation queries  
- Graph database integration (Neo4j)  
- Semantic search using embeddings  
- Advanced graph analytics  

---

## 🤖 AI Coding Workflow

This project was developed using AI-assisted tools.

Included:
- Prompt iterations  
- Debugging sessions  
- Incremental improvements  

See `/ai_logs/` for full transcripts.

---
## Dataset Note

The original SAP O2C dataset is large and exceeds GitHub/Streamlit deployment limits.

For deployment purposes, a representative subset of the dataset has been used (`dataset_sample/`), preserving the original structure and relationships.

This ensures:
- Full functionality of the system
- Successful deployment and demo access
- Realistic graph behavior


## 🎯 Conclusion

This system demonstrates how graph-based modeling combined with structured query interpretation can enable powerful, accurate, and interactive exploration of ERP data.

It prioritizes:
- correctness over hallucination  
- clarity over complexity  
- usability over over-engineering  
