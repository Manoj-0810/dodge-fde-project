\# 🚀 ERP Context Graph + LLM Query System



\## 📌 Overview



This project implements a \*\*Context Graph-based Query System\*\* over ERP (Order-to-Cash) data, enhanced with a \*\*Large Language Model (LLM)\*\* interface.



The system allows users to query enterprise data using \*\*natural language\*\*, instead of writing SQL or navigating complex relational tables.



\---



\## 🎯 Problem Statement



ERP systems store highly interconnected data across multiple tables (Sales Orders, Deliveries, Billing, Payments).



Traditional querying:



\* Requires SQL joins ❌

\* Difficult for non-technical users ❌

\* Not intuitive ❌



\---



\## ✅ Solution



We transform relational ERP data into a \*\*graph structure\*\*, enabling intuitive traversal, and integrate an \*\*LLM layer\*\* to interpret natural language queries.



\---



\## 🧠 System Architecture



```

User Query (Natural Language)

&#x20;       ↓

Gemini LLM (Intent + Entity Extraction)

&#x20;       ↓

Query Engine (Python)

&#x20;       ↓

Graph (NetworkX आधारित ERP model)

&#x20;       ↓

Result (Billing / Delivery / etc.)

&#x20;       ↓

Streamlit UI

```



\---



\## 🗂️ Dataset



SAP Order-to-Cash dataset containing:



\* Sales Orders

\* Delivery Documents

\* Billing Documents

\* Payment Records



\---



\## 🔗 Graph Modeling



We convert ERP tables into a \*\*directed graph\*\*:



\### Nodes:



\* SalesOrder (`SO\_xxx`)

\* Delivery (`D\_xxx`)

\* Billing (`B\_xxx`)



\### Edges:



\* SalesOrder → Delivery

\* Delivery → Billing



This enables efficient traversal like:



```

SalesOrder → Delivery → Billing

```



\---



\## 🤖 LLM Integration (Gemini)



We use \*\*Google Gemini API\*\* to:



\* Understand user intent

\* Extract relevant entities (e.g., Sales Order ID)

\* Map natural language → graph query



\### Example:



Input:



```

give me invoices for order 740509

```



LLM extracts:



```

intent = get\_billing

sales\_order\_id = 740509

```



\---



\## ⚙️ Tech Stack



\* Python

\* NetworkX (Graph modeling)

\* Streamlit (UI)

\* Google Gemini API (LLM)



\---



\## 🧪 Example Queries



\* show billing for sales order 740509

\* give me invoices for order 740509

\* find billing docs linked to 740509



\---



\## 📊 Output Example



```

billing documents: \['B\_90504204', 'B\_91150217']

```



\---



\## 🚀 How to Run



\### 1. Install dependencies



```

pip install networkx streamlit google-genai

```



\---



\### 2. Set API Key



In `query\_engine.py`:



```

client = genai.Client(api\_key="YOUR\_API\_KEY")

```



\---



\### 3. Run Backend



```

python src/query\_engine.py

```



\---



\### 4. Run UI



```

streamlit run src/app.py

```



\---



\## 💡 Key Design Decisions



\### 1. Graph over SQL



Graph traversal simplifies multi-hop queries compared to complex joins.



\### 2. LLM for Query Understanding



Avoids rigid keyword-based parsing and supports flexible natural language.



\### 3. Modular Architecture



\* Graph layer

\* Query layer

\* LLM layer

\* UI layer



\---



\## ⚠️ Limitations



\* Currently supports limited query types

\* No persistent storage (in-memory graph)

\* Basic LLM parsing (can be extended)



\---



\## 🔮 Future Improvements



\* Add more entity types (Payments, Customers)

\* Multi-hop reasoning queries

\* Graph visualization (interactive)

\* Conversation memory (chat history)



\---



\## 🏁 Conclusion



This project demonstrates how combining:



\* Graph-based data modeling

\* LLM-powered interfaces



can significantly improve how users interact with complex enterprise systems.



\---



\## 👨‍💻 Author



Manoj RS

B.E. Electronics and Communication Engineering

AI/ML Enthusiast



\---



