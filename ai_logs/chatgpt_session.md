\# AI Coding Session Logs



\## 🧠 Project: ERP Graph Assistant



This document captures key interactions, problem-solving steps, and iterative improvements made using AI tools during development.



\---



\## 1. Graph Construction



\*\*Problem:\*\*  

How to model SAP O2C dataset into a structured graph.



\*\*Prompt:\*\*  

"How to build a graph using NetworkX for Sales Order → Delivery → Billing?"



\*\*Solution:\*\*  

\- Used NetworkX DiGraph

\- Created nodes:

&#x20; - SO\_<id>

&#x20; - D\_<id>

&#x20; - B\_<id>

\- Created edges:

&#x20; - SO → Delivery

&#x20; - Delivery → Billing



\*\*Outcome:\*\*  

Successfully built a graph representing business flow.



\---



\## 2. Query System Design



\*\*Problem:\*\*  

Convert natural language queries into graph operations.



\*\*Prompt:\*\*  

"How to map user queries like 'trace flow' into graph traversal?"



\*\*Solution:\*\*  

\- Built rule-based parser (`llm\_to\_query`)

\- Mapped queries into structured format:

&#x20; - trace\_flow

&#x20; - billing

&#x20; - broken\_flow

&#x20; - top\_orders



\*\*Outcome:\*\*  

Deterministic query execution without hallucination.



\---



\## 3. Multi-Query Handling



\*\*Problem:\*\*  

Support multiple queries in one input.



\*\*Prompt:\*\*  

"How to process comma-separated queries?"



\*\*Solution:\*\*  

\- Split input using regex

\- Process each query independently

\- Aggregate results



\*\*Outcome:\*\*  

Enabled multi-query support.



\---



\## 4. Graph Visualization



\*\*Problem:\*\*  

How to visualize graph interactively.



\*\*Prompt:\*\*  

"How to show NetworkX graph in Streamlit?"



\*\*Solution:\*\*  

\- Used streamlit-agraph

\- Converted graph → nodes + edges

\- Added UI panel



\*\*Outcome:\*\*  

Interactive graph displayed in UI.



\---



\## 5. Flow Highlighting



\*\*Problem:\*\*  

Visually highlight query results.



\*\*Prompt:\*\*  

"How to highlight specific nodes and edges?"



\*\*Solution:\*\*  

\- Stored relevant nodes in session state

\- Applied color change (red)

\- Highlighted edges dynamically



\*\*Outcome:\*\*  

Visual tracing of query results implemented.



\---



\## 6. Guardrails



\*\*Problem:\*\*  

Prevent non-ERP queries.



\*\*Prompt:\*\*  

"How to restrict queries to domain?"



\*\*Solution:\*\*  

\- Keyword-based filtering

\- Reject unrelated queries



\*\*Outcome:\*\*  

System safely handles invalid input.



\---



\## 7. UI Improvements



\*\*Problem:\*\*  

Chat UI and interaction issues.



\*\*Prompt:\*\*  

"Fix alignment and input issues in Streamlit chat."



\*\*Solution:\*\*  

\- Used form-based input

\- Ensured Enter + button both work

\- Simplified UI



\*\*Outcome:\*\*  

Clean and stable chat interface.



\---



\## 8. Response Standardization



\*\*Problem:\*\*  

Inconsistent responses across queries.



\*\*Prompt:\*\*  

"Make responses consistent and simple."



\*\*Solution:\*\*  

\- Unified response format:

&#x20; - Title

&#x20; - Bullet points

\- Removed verbose explanations



\*\*Outcome:\*\*  

Professional and consistent responses.



\---



\## 9. Debugging \& Fixes



\*\*Key Issues Solved:\*\*

\- Edge attribute error (`target → to`)

\- Chat input not working with Enter

\- Multi-query override bug

\- Missing query handling (top\_orders)



\---



\## 🎯 Summary



The development process involved:

\- Iterative problem solving

\- Debugging real issues

\- Improving architecture and UX



AI tools were used for:

\- Code generation

\- Debugging

\- Design decisions

\- Optimization



Final system is:

\- Fully functional

\- Deterministic

\- Graph-driven

\- Production-ready (prototype level)

