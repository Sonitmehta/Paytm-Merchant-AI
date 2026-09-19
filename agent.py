# Core Agent Logic — Powered by Google Gemini Flash & LangGraph
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

import time

# High-quota production models on Google AI Studio Free Tier
FALLBACK_MODELS = [
    "gemini-2.5-flash",
    "gemini-1.5-flash",
    "gemini-2.5-pro",
    "gemini-1.5-pro",
]

def create_agent(api_key: str, model_name: str = "gemini-2.5-flash"):
    if not api_key:
        return None
    llm = ChatGoogleGenerativeAI(
        model=model_name,
        temperature=0.2,
        google_api_key=api_key,
        streaming=False,
    )

    tools = get_all_tools()
    agent = create_react_agent(llm, tools=tools, prompt=SYSTEM_PROMPT)
    return agent

def run_direct_business_execution():
    """Deterministic autonomous execution fallback if all remote model quotas are temporarily exhausted."""
    from data import get_merchant_context
    from tools import (
        send_payment_reminder, flag_slow_inventory, 
        draft_promotional_offer, reorder_alert, generate_daily_summary
    )
    from datetime import datetime
    
    ctx = get_merchant_context()
    m = ctx["merchant"]
    inv = ctx["inventory"]
    dues = ctx["pending_payments"]
    sales = ctx["sales_trend"]
    
    actions_taken = []
    
    # 1. Overdue payments
    for p in dues:
        if p.get("due_days", 0) >= 7:
            msg = f"Namaste {p['customer']}, friendly reminder from {m['name']} regarding pending balance of ₹{p['amount']}. Pay via Paytm UPI: {m.get('upi_id', 'merchant@paytm')}."
            send_payment_reminder.invoke({
                "customer_name": p["customer"],
                "amount": float(p["amount"]),
                "phone": p["phone"],
                "message": msg
            })
            actions_taken.append(f"Dispatched WhatsApp reminder to **{p['customer']}** (₹{p['amount']})")
    
    # 2. Slow inventory
    slow_items = [i for i in inv if i.get("days_in_stock", 0) >= 30]
    if slow_items:
        slowest = max(slow_items, key=lambda x: x.get("days_in_stock", 0))
        flag_slow_inventory.invoke({
            "item_name": slowest["item"],
            "days_unsold": int(slowest["days_in_stock"]),
            "suggested_action": "Run flash discount promo"
        })
        draft_promotional_offer.invoke({
            "offer_title": f"{slowest['item']} Flash Clearance",
            "target_items": slowest["item"],
            "discount_percent": 15,
            "valid_days": 3
        })
        actions_taken.append(f"Flagged slow-moving **{slowest['item']}** & drafted 15% flash offer")
    
    # 3. Low stock reorder
    low_stock = [i for i in inv if i.get("stock", 0) <= 3]
    for item in low_stock:
        reorder_alert.invoke({
            "item_name": item["item"],
            "current_stock": int(item["stock"]),
            "reorder_quantity": 25
        })
        actions_taken.append(f"Triggered reorder alert for **{item['item']}** (Stock: {item['stock']})")
        
    generate_daily_summary.invoke({"date": datetime.now().strftime("%d %b %Y")})
    
    report = (
        "### 📊 Business Health Check\n"
        f"- **Revenue:** ₹{sales['today']:,} today across active categories.\n"
        f"- **Receivables:** ₹{sum(p['amount'] for p in dues):,} in pending credit across {len(dues)} customers.\n"
        f"- **Inventory:** {len(low_stock)} items need restock; {len(slow_items)} slow items flagged.\n\n"
        "### ⚡ Actions Executed Automatically\n" +
        "\n".join([f"- ✓ {a}" for a in actions_taken]) + "\n\n"
        "### 💡 Next Opportunities\n"
        "- Promote your newly drafted clearance offer on WhatsApp Business status.\n"
        "- Confirm vendor delivery for flagged low-stock items before peak evening footfall."
    )
    return {"output": report, "model_used": "Autonomous Rule Engine (Zero Latency)"}

def invoke_with_fallback(api_key: str, messages: list) -> dict:
    """Invokes agent with fast retry and automatic fallback across Gemini models on 503/429/404. If no API key is provided, seamlessly runs the local autonomous engine."""
    if not api_key:
        return run_direct_business_execution()
        
    for model_name in FALLBACK_MODELS:
        try:
            agent = create_agent(api_key, model_name=model_name)
            if not agent:
                continue
            result = agent.invoke({"messages": messages})
            last_msg = result["messages"][-1]
            output_text = last_msg.content if hasattr(last_msg, "content") else str(last_msg)
            return {"output": output_text, "model_used": model_name}
        except Exception as e:
            # Continue trying next model in chain
            continue
            
    # If all remote models hit rate limits (429) or spikes (503), engage zero-failure autonomous engine
    return run_direct_business_execution()

def run_autonomous_scan(api_key: str) -> dict:
    """Run fast autonomous merchant scan with pre-injected telemetry context for sub-3s response."""
    from data import get_merchant_context
    import json
    
    ctx = get_merchant_context()
    ctx_str = json.dumps(ctx, indent=1)
    
    prompt_text = (
        f"Here is the LIVE MERCHANT TELEMETRY:\n```json\n{ctx_str}\n```\n\n"
        "You do NOT need to fetch merchant data again. Immediately execute necessary actions using your tools: "
        "1. Send WhatsApp reminders for overdue payments.\n"
        "2. Flag slow-moving stock & draft a promo offer for the slowest item.\n"
        "3. Send reorder alert for low stock items.\n"
        "4. Generate daily summary.\n\n"
        "Then provide a concise executive report:\n"
        "### 📊 Business Health Check\n"
        "- 3 brief bullet points on performance\n\n"
        "### ⚡ Actions Executed Automatically\n"
        "- Checkbox list (✓) of actions taken\n\n"
        "### 💡 Next Opportunities\n"
        "- 1-2 practical tips for the merchant today"
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

