# Core Agent Logic — Powered by Google Gemini 2.0 Flash & LangGraph
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from tools import get_all_tools
import os

SYSTEM_PROMPT = """You are an autonomous AI business teammate for Paytm merchants (like Rajesh Kirana Store).
Your job is to proactively analyze merchant data, execute actions, and report results concisely.

You have access to these tools:
- get_merchant_data: Always call this FIRST to understand sales, inventory, and pending payments
- send_payment_reminder: Send WhatsApp payment reminders for overdue dues
- flag_slow_inventory: Flag slow-moving stock
- draft_promotional_offer: Draft promotional offers for slow items
- reorder_alert: Alert for critically low stock items
- generate_daily_summary: Record summary

FORMATTING GUIDELINES (CRITICAL):
- Never output a long wall of dense text.
- Present findings like an executive dashboard using clean Markdown:
  1. 🎯 **Quick Executive Summary** (2-3 punchy bullet points)
  2. ⚡ **Actions Executed Automatically** (table or bullet checklist of what tools were triggered)
  3. 💡 **Next Recommendations for Merchant** (1-2 quick actions)
- Use bold numbers, currency signs (₹), and emojis for easy scanning.
- Keep tone encouraging, professional, and straight-to-the-point."""

FALLBACK_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-3.6-flash",
]

def create_agent(api_key: str, model_name: str = "gemini-2.5-flash"):
    llm = ChatGoogleGenerativeAI(
        model=model_name,
        temperature=0.3,
        google_api_key=api_key,
        streaming=True,
    )

    tools = get_all_tools()
    agent = create_react_agent(llm, tools=tools, prompt=SYSTEM_PROMPT)
    return agent

def invoke_with_fallback(api_key: str, messages: list) -> dict:
    """Invokes agent with automatic fallback across available Gemini models on 503/429/404."""
    last_error = None
    for model_name in FALLBACK_MODELS:
        try:
            agent = create_agent(api_key, model_name=model_name)
            result = agent.invoke({"messages": messages})
            last_msg = result["messages"][-1]
            output_text = last_msg.content if hasattr(last_msg, "content") else str(last_msg)
            return {"output": output_text}
        except Exception as e:
            last_error = e
            # Try next model if overloaded (503), rate-limited (429), or not found (404)
            err_str = str(e).lower()
            if any(term in err_str for term in ["503", "unavailable", "demand", "429", "resource_exhausted", "404", "not_found"]):
                continue
            raise e
    raise last_error

def run_autonomous_scan(api_key: str) -> dict:
    """Run the agent's full autonomous merchant scan with auto-fallback."""
    prompt_text = (
        "Perform a full autonomous business scan: check overdue payments, slow-moving items, "
        "and low inventory. Execute all necessary actions (reminders, flags, restock alerts, promo offers). "
        "Then provide a concise, beautifully formatted report strictly in this format:\n\n"
        "### 📊 Business Health Check\n"
        "- 3 brief bullet points summarizing the business status\n\n"
        "### ⚡ Actions Executed Automatically\n"
        "- Bullet list with checkboxes (✓) showing exactly what actions you took (e.g. WhatsApp reminders sent, alerts raised)\n\n"
        "### 💡 Next Opportunities\n"
        "- 1-2 practical tips for the merchant today\n\n"
        "Keep it concise, scannable, and clean. No walls of text."
    )
    return invoke_with_fallback(api_key, [HumanMessage(content=prompt_text)])

def run_custom_query(api_key: str, query: str, chat_history: list = None) -> dict:
    """Run a custom query against the merchant agent with persistent history and auto-fallback."""
    messages = []
    for msg in (chat_history or []):
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(AIMessage(content=msg["content"]))
    messages.append(HumanMessage(content=query))
    return invoke_with_fallback(api_key, messages)

