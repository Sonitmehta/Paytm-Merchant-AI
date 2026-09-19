# Agent Tools - Actions the AI can take
from langchain.tools import tool
from data import get_merchant_context, PENDING_PAYMENTS, INVENTORY, SALES_TREND, MERCHANT
import json

# Simulated action log (in real world, these would call Paytm APIs / WhatsApp API)
ACTION_LOG = []

def log_action(action_type, details):
    # Prevent duplicate daily summary entries
    if action_type == "daily_summary":
        if any(a.get("type") == "daily_summary" for a in ACTION_LOG):
            return details
    ACTION_LOG.append({"type": action_type, "details": details})
    return details

@tool
def get_merchant_data(query: str) -> str:
    """Fetches the current merchant's sales, inventory, and payment data. Use this first to understand the merchant's situation."""
    ctx = get_merchant_context()
    return json.dumps(ctx, indent=2)

@tool
def send_payment_reminder(customer_name: str, amount: float, phone: str, message: str) -> str:
    """Sends a WhatsApp payment reminder to a customer. Provide customer_name, amount owed, phone number, and a friendly message."""
    result = {
        "action": "PAYMENT_REMINDER_SENT",
        "to": customer_name,
        "phone": phone,
        "amount": f"₹{amount}",
        "message": message,
        "channel": "WhatsApp",
        "status": "✅ Delivered"
    }
    log_action("payment_reminder", result)
    return f"✅ Payment reminder sent to {customer_name} ({phone}) for ₹{amount} via WhatsApp."

@tool
def flag_slow_inventory(item_name: str, days_unsold: int, suggested_action: str) -> str:
    """Flags a slow-moving inventory item and suggests a corrective action like discount or reorder pause."""
    result = {
        "action": "INVENTORY_FLAGGED",
        "item": item_name,
        "days_unsold": days_unsold,
        "suggested_action": suggested_action,
        "status": "⚠️ Flagged"
    }
    log_action("inventory_flag", result)
    return f"⚠️ Flagged '{item_name}' as slow-moving ({days_unsold} days). Suggestion: {suggested_action}"

@tool
def draft_promotional_offer(offer_title: str, target_items: str, discount_percent: int, valid_days: int) -> str:
    """Drafts a promotional offer for slow-moving or seasonal items to boost sales."""
    ctx = get_merchant_context()
    m = ctx["merchant"]
    offer = (
        f"🎉 *{m['name']} Special Offer!*\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"📦 Items: {target_items}\n"
        f"💰 Discount: {discount_percent}% OFF\n"
        f"⏰ Valid for: {valid_days} days only\n"
        f"📲 Pay via Paytm UPI: {m.get('upi_id', 'merchant@paytm')} & get instant cashback!\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"Call/WhatsApp: {m.get('phone', '+91-98765-43210')}"
    )
    result = {
        "action": "PROMO_DRAFTED",
        "title": offer_title,
        "offer_text": offer,
        "status": "📝 Draft Ready"
    }
    log_action("promo_draft", result)
    return f"📝 Promotional offer drafted:\n\n{offer}"

@tool
def generate_daily_summary(date: str) -> str:
    """Generates a merchant daily business summary including sales performance, top items, and action items."""
    ctx = get_merchant_context()
    m = ctx["merchant"]
    s = ctx["sales_trend"]
    dues = ctx["pending_payments"]
    
    growth = round(((s['today'] - s['yesterday']) / s['yesterday']) * 100, 1) if s['yesterday'] else 0
    weekly_growth = round(((s['this_week'] - s['last_week']) / s['last_week']) * 100, 1) if s['last_week'] else 0
    
    summary = (
        f"📊 *Daily Summary — {date}*\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"🏪 Business: {m['name']} ({m.get('category', 'Retail')})\n"
        f"💵 Today's Sales: ₹{s['today']:,} ({'+' if growth > 0 else ''}{growth}% vs yesterday)\n"
        f"📅 This Week: ₹{s['this_week']:,} ({'+' if weekly_growth > 0 else ''}{weekly_growth}% vs last week)\n"
        f"🔥 Best Sellers: {', '.join(s['best_selling_today'])}\n"
        f"🐢 Slow Movers: {', '.join(s['slowest_this_week'])}\n"
        f"💳 Paytm Balance: ₹{m['paytm_balance']:,}\n"
        f"⏳ Pending Receivables: {len(dues)} customers | "
        f"₹{sum(p['amount'] for p in dues):,} total\n"
        f"━━━━━━━━━━━━━━━━━━━━━"
    )
    log_action("daily_summary", {"date": date, "sales": s['today'], "merchant": m['name']})
    return summary

@tool
def reorder_alert(item_name: str, current_stock: int, reorder_quantity: int) -> str:
    """Sends a reorder alert for a low-stock item so the merchant knows to restock."""
    result = {
        "action": "REORDER_ALERT",
        "item": item_name,
        "current_stock": current_stock,
        "reorder_qty": reorder_quantity,
        "status": "🔔 Alert Sent"
    }
    log_action("reorder_alert", result)
    return f"🔔 Reorder alert: '{item_name}' has only {current_stock} units left. Suggested reorder: {reorder_quantity} units."

def get_all_tools():
    return [
        get_merchant_data,
        send_payment_reminder,
        flag_slow_inventory,
        draft_promotional_offer,
        generate_daily_summary,
        reorder_alert,
    ]

def get_action_log():
    return list(ACTION_LOG)

def clear_action_log():
    global ACTION_LOG
    ACTION_LOG.clear()
