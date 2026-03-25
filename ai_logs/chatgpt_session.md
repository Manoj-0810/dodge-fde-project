# AI Coding Session Logs

## 🧠 Project: ERP Graph Assistant

This document captures the iterative development process, key design decisions, and debugging workflows followed while building the ERP Graph Assistant using AI tools.

---

## 🚀 Development Approach

The system was built incrementally with a focus on:

* Converting structured ERP data into a graph model
* Designing a reliable query system (LLM + deterministic fallback)
* Integrating conversational input with graph visualization
* Ensuring correctness over generative output

AI tools were used as a **collaborative assistant** for:

* Breaking down complex problems
* Generating initial implementations
* Debugging runtime issues
* Refining system design

---

## 1️⃣ Graph Construction & Data Modeling

**Problem:**
How to represent ERP Order-to-Cash data as a graph.

**Prompt Used:**
"How to model relationships between sales orders, deliveries, and billing in NetworkX?"

**Solution:**

* Used `NetworkX DiGraph`
* Created node types:

  * `SO_<id>` → Sales Orders
  * `D_<id>` → Deliveries
  * `B_<id>` → Billing Documents
* Established edges:

  * Sales Order → Delivery
  * Delivery → Billing

**Key Insight:**
Graph structure enables natural representation of business flows and supports traversal queries.

**Outcome:**
Successfully modeled ERP lifecycle as a directed graph.

---

## 2️⃣ Query System Design (Core Engine)

**Problem:**
Translate natural language queries into deterministic graph operations.

**Prompt Used:**
"How to map user queries like 'trace flow' into graph traversal logic?"

**Solution:**

* Built rule-based parser:

  * `trace_flow`
  * `billing_lookup`
  * `broken_flow`
  * `top_orders`
* Designed execution layer using graph traversal (`successors()`)

**Improvement Iteration:**

* Introduced **intent → execution separation**
* Standardized outputs across queries

**Outcome:**
Reliable and deterministic query system with no hallucination.

---

## 3️⃣ LLM Integration (Hybrid Query Parsing)

**Problem:**
Enable flexible natural language understanding without losing reliability.

**Prompt Used:**
"How to extract structured intent and entity from a query using an LLM?"

**Solution:**

* Integrated Gemini API for intent parsing
* Designed prompt to return strict JSON:

```json
{
  "intent": "...",
  "sales_order_id": "..."
}
```

* Implemented fallback:

  * If LLM fails → use rule-based parsing

**Key Design Decision:**
Hybrid approach ensures:

* Flexibility (LLM)
* Reliability (rules)

**Outcome:**
Robust query parsing system with zero dependency on API availability.

---

## 4️⃣ Multi-Query Handling

**Problem:**
Support multiple queries in a single input.

**Prompt Used:**
"How to process comma-separated queries efficiently?"

**Solution:**

* Split input using delimiter
* Process each query independently
* Merge responses and graph outputs

**Key Fix:**

* Ensured flow nodes are aggregated correctly across queries

**Outcome:**
Enabled advanced usage like:

```text
trace flow for sales order 740573, show me top orders
```

---

## 5️⃣ Graph Visualization

**Problem:**
Display graph interactively in UI.

**Prompt Used:**
"How to visualize NetworkX graph in Streamlit?"

**Solution:**

* Used `streamlit-agraph`
* Converted graph → nodes + edges
* Implemented layout + styling

**Outcome:**
Interactive graph embedded in UI.

---

## 6️⃣ Chat ↔ Graph Integration (Core Highlight)

**Problem:**
Link user queries directly to graph visualization.

**Solution:**

* Query engine returns:

  * `text` → response
  * `flow_nodes` → nodes to highlight

* Stored `flow_nodes` in session state

* UI dynamically highlights nodes

**Key Insight:**
Graph is not static — it reacts to queries.

**Outcome:**
Tight integration between:

* Natural language queries
* Graph visualization

---

## 7️⃣ Dynamic Node Highlighting

**Problem:**
Visually represent query results in graph.

**Prompt Used:**
"How to highlight specific nodes and edges dynamically?"

**Solution:**

* Highlight nodes:

  * Change color → red
  * Increase size
* Highlight edges connecting selected nodes

**Enhancement Iteration:**

* Extended highlighting beyond flow:

  * Top orders → highlight nodes
  * Billing queries → highlight relevant nodes

**Outcome:**
Clear visual feedback for all query types.

---

## 8️⃣ Guardrails & Safety

**Problem:**
Prevent irrelevant or off-topic queries.

**Solution:**

* Keyword-based filtering
* Reject non-ERP queries

**Example:**

```text
Input: Who is the president of India?
Output: This system is designed to answer ERP dataset-related queries only.
```

**Outcome:**
Safe and controlled query environment.

---

## 9️⃣ Performance Optimization (Graph Caching)

**Problem:**
Graph construction is expensive on each run.

**Solution:**

* Added caching using `graph.pkl`
* Load graph if exists, else rebuild

**Design Insight:**
Simulates real-world persistence layer

**Outcome:**
Faster startup and improved UX.

---

## 🔟 Debugging & Iterative Fixes

**Key Issues Solved:**

* Fixed edge attribute mismatch (`target → to`)
* Resolved Streamlit form input issues
* Fixed multi-query overriding results
* Corrected LLM parsing JSON errors
* Restored graph highlighting pipeline
* Fixed advanced query routing (`top_billed_orders`)
* Eliminated redundant code (`llm_parser.py`)

**Approach:**

* Iterative debugging
* Small incremental fixes
* Continuous validation via UI

---

## 🎯 Final System Capabilities

* Graph-based ERP modeling
* Conversational querying
* LLM + rule-based hybrid parsing
* Multi-query support
* Dynamic graph highlighting
* Guardrails for safe interaction
* Cached graph for performance

---

## 🧠 Key Takeaways

* Prioritized **correctness over generation**
* Designed system to be **data-grounded**
* Built **tight coupling between query and visualization**
* Focused on **scalable architecture and extensibility**

---

## 📌 Conclusion

This project reflects a structured engineering approach where AI tools were used not just for coding, but for:

* System design
* Iterative refinement
* Debugging complex interactions

The final system demonstrates a **practical, production-oriented mindset** with emphasis on reliability, usability, and extensibility.
