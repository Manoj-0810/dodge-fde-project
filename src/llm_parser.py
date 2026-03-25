import json
import streamlit as st

# Try to import Gemini (optional)
try:
    import google.generativeai as genai
    genai.configure(api_key=st.secrets.get("GEMINI_API_KEY", ""))
    MODEL = genai.GenerativeModel("gemini-pro")
    USE_LLM = True
except:
    USE_LLM = False


def parse_query_with_llm(user_query):
    """
    Uses LLM to convert query into structured format.
    Falls back to rule-based if LLM fails.
    """

    if not USE_LLM:
        return None

    prompt = f"""
    Convert this ERP query into JSON.

    Query: "{user_query}"

    Output ONLY JSON like:
    {{
        "intent": "...",
        "sales_order_id": "..."
    }}

    Possible intents:
    - trace_flow
    - billing_lookup
    - broken_flow
    - top_orders
    """

    try:
        response = MODEL.generate_content(prompt)
        text = response.text.strip()

        # Try parsing JSON
        return json.loads(text)

    except:
        return None