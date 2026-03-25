
from google import genai
from graph_builder import G, get_billing_from_sales_order
import re

# create Gemini client
client = genai.Client(api_key="AIzaSyD_fmbTiwNYYz1awyzoVdO75l22T63HqCE")


# use LLM to extract info
def extract_info_with_llm(query):
    prompt = f"""
    Extract the intent and sales order ID from the query.

    Query: "{query}"

    Return only JSON like:
    {{
        "intent": "get_billing",
        "sales_order_id": "XXXXXX"
    }}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text

    # extract number from response
    numbers = re.findall(r"\d+", text)

    if numbers:
        return "get_billing", numbers[0]

    return None, None


# main handler
def handle_query(query):
    intent, so_id = extract_info_with_llm(query)

    if not so_id:
        return "could not understand the query"

    if intent == "get_billing":
        result = get_billing_from_sales_order(G, so_id)

        if not result:
            return f"no billing found for sales order {so_id}"

        return f"billing documents: {result}"

    return "query not supported"


# run from terminal
if __name__ == "__main__":
    user_input = input("ask something: ")
    print(handle_query(user_input))