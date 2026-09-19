# Paytm Merchant AI Teammate - Streamlit Frontend
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from data import (
    get_merchant_context, load_profile, update_merchant_info,
    add_pending_payment, add_inventory_item, PRESET_PROFILES
)
from tools import get_action_log, ACTION_LOG

st.set_page_config(
    page_title="Paytm Merchant AI Teammate",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "active_profile" not in st.session_state:
    st.session_state.active_profile = "custom"

# ── PAYTM ADAPTIVE HIGH-CONTRAST THEME (LIGHT & DARK MODE READY) ───────────────
st.markdown("""
<style>
/* ── BASE CONTAINER ── */
.block-container {
    padding-top: 2rem !important;
    max-width: 1280px;
}

/* ── HEADER TOOLBAR, 3-DOTS (⋮), DEPLOY ICON — ADAPTIVE CONTRAST ── */
header[data-testid="stHeader"] {
    background: transparent !important;
    z-index: 999999 !important;
}
[data-testid="stToolbar"],
[data-testid="stMainMenu"],
[data-testid="stStatusWidget"],
button[title="View app in Streamlit Community Cloud"],
[data-testid="stHeader"] button {
    visibility: visible !important;
    opacity: 1 !important;
    background: rgba(0, 186, 242, 0.15) !important;
    border: 1.5px solid #00BAF2 !important;
    border-radius: 8px !important;
}
[data-testid="stToolbar"] svg,
[data-testid="stMainMenu"] svg,
[data-testid="stHeader"] svg {
    fill: #00BAF2 !important;
    stroke: #00BAF2 !important;
    stroke-width: 1.5px !important;
    visibility: visible !important;
}
@media (prefers-color-scheme: dark) {
    [data-testid="stToolbar"] svg,
    [data-testid="stMainMenu"] svg,
    [data-testid="stHeader"] svg {
        fill: #FFFFFF !important;
        stroke: #FFFFFF !important;
    }
    [data-testid="stToolbar"] button,
    [data-testid="stMainMenu"] button {
        background: rgba(255, 255, 255, 0.20) !important;
        border: 1.5px solid #00BAF2 !important;
    }
}

/* ── PAGE TITLE — VIBRANT & VISIBLE ON BOTH LIGHT & DARK ── */
.paytm-header {
    font-size: 2.2rem;
    font-weight: 900;
    color: #002970;
    letter-spacing: -0.5px;
    margin-bottom: 2px;
}
.paytm-header span {
    color: #00BAF2;
    text-shadow: 0 0 12px rgba(0, 186, 242, 0.3);
}
@media (prefers-color-scheme: dark) {
    .paytm-header {
        color: #FFFFFF !important;
    }
}

/* ── UNIVERSAL TEXT READABILITY ── */
.stApp p, .stApp li, .stApp span,
div[data-testid="stMarkdownContainer"] p,
div[data-testid="stMarkdownContainer"] li,
div[data-testid="stMarkdownContainer"] span {
    font-weight: 600;
}
label, .stWidgetLabel, [data-testid="stWidgetLabel"] p {
    font-weight: 800 !important;
    font-size: 0.95rem !important;
}

/* ── METRIC CARDS ── */
[data-testid="stMetric"] {
    background: #FFFFFF !important;
    padding: 14px 18px !important;
    border-radius: 12px !important;
    border: 1.5px solid #CBD5E1 !important;
    border-top: 4px solid #00BAF2 !important;
    box-shadow: 0 4px 12px rgba(0, 41, 112, 0.08) !important;
}
[data-testid="stMetric"] label,
[data-testid="stMetricLabel"] p {
    color: #002970 !important;
    font-weight: 800 !important;
    font-size: 0.95rem !important;
}
[data-testid="stMetricValue"], [data-testid="stMetricValue"] div {
    color: #002970 !important;
    font-weight: 900 !important;
    font-size: 1.85rem !important;
}
@media (prefers-color-scheme: dark) {
    [data-testid="stMetric"] {
        background: #001A4A !important;
        border-color: #00BAF2 !important;
    }
    [data-testid="stMetric"] label,
    [data-testid="stMetricLabel"] p,
    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] div {
        color: #FFFFFF !important;
    }
}

/* ── INPUT FIELDS (MAIN PAGE) ── */
.stTextInput input, .stNumberInput input, .stTextArea textarea {
    background: #FFFFFF !important;
    color: #000000 !important;
    border: 2px solid #00BAF2 !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
}

/* ── SIDEBAR — DEEP PAYTM NAVY WITH HIGH-CONTRAST INPUTS ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #001538 0%, #002970 100%) !important;
    box-shadow: 4px 0 24px rgba(0, 41, 112, 0.4) !important;
}
[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}
[data-testid="stSidebar"] strong,
[data-testid="stSidebar"] b {
    color: #00BAF2 !important;
    font-weight: 800 !important;
}
[data-testid="stSidebar"] hr {
    border-color: rgba(0, 186, 242, 0.5) !important;
}

/* SIDEBAR INPUTS — SOLID WHITE BACKGROUND FOR MAXIMUM READABILITY IN ALL MODES */
[data-testid="stSidebar"] .stTextInput input,
[data-testid="stSidebar"] .stNumberInput input {
    background: #FFFFFF !important;
    color: #001538 !important;
    border: 2px solid #00BAF2 !important;
    border-radius: 8px !important;
    font-weight: 800 !important;
}
[data-testid="stSidebar"] .stTextInput input::placeholder,
[data-testid="stSidebar"] .stNumberInput input::placeholder {
    color: #64748B !important;
    font-weight: 600 !important;
}
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: #FFFFFF !important;
    color: #001538 !important;
    border: 2px solid #00BAF2 !important;
    border-radius: 8px !important;
    font-weight: 800 !important;
}
[data-testid="stSidebar"] .stSelectbox svg {
    fill: #002970 !important;
}
[data-testid="stSidebar"] [data-testid="stExpander"] {
    background: rgba(255, 255, 255, 0.12) !important;
    border: 1.5px solid #00BAF2 !important;
}
[data-testid="stSidebar"] [data-testid="stExpander"] summary {
    color: #FFFFFF !important;
    font-weight: 800 !important;
}
[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, #00BAF2 0%, #0077B6 100%) !important;
    color: #FFFFFF !important;
    font-weight: 800 !important;
    border: none !important;
    box-shadow: 0 4px 12px rgba(0, 186, 242, 0.35) !important;
}

/* ── SIDEBAR TOGGLE / COLLAPSE BUTTON (<< and >>) ── */
[data-testid="stSidebarCollapseButton"] button,
[data-testid="collapsedControl"] button {
    background: #002970 !important;
    border: 2px solid #00BAF2 !important;
    border-radius: 8px !important;
    box-shadow: 0 2px 10px rgba(0, 186, 242, 0.4) !important;
}
[data-testid="stSidebarCollapseButton"] svg,
[data-testid="collapsedControl"] svg {
    fill: #00BAF2 !important;
    stroke: #00BAF2 !important;
    stroke-width: 2px !important;
}

/* ── UDHAAR / ALERT CARDS ── */
.alert-card {
    background: #FFF5F5;
    padding: 0.85rem 1.1rem;
    border-radius: 10px;
    border-left: 4px solid #EF4444;
    border-top: 1px solid #FECACA;
    border-right: 1px solid #FECACA;
    border-bottom: 1px solid #FECACA;
    box-shadow: 0 2px 8px rgba(239, 68, 68, 0.12);
    margin: 0.4rem 0;
}
.alert-card, .alert-card p, .alert-card span, .alert-card small {
    color: #000000 !important;
}
.alert-card b {
    color: #991B1B !important;
    font-weight: 800 !important;
}
.alert-card small {
    color: #475569 !important;
    font-weight: 700 !important;
}

/* ── API BADGES ── */
.api-badge-ok {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #DCFCE7;
    color: #14532D !important;
    border: 1.5px solid #4ADE80;
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 0.85rem;
    font-weight: 800;
    margin-top: 6px;
}
.api-badge-none {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #FEF9C3;
    color: #713F12 !important;
    border: 1.5px solid #FACC15;
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 0.85rem;
    font-weight: 800;
    margin-top: 6px;
}

/* ── PRIMARY SCAN BUTTON ── */
.stButton > button {
    background: linear-gradient(135deg, #00BAF2 0%, #0088CC 100%) !important;
    color: #FFFFFF !important;
    border-radius: 10px !important;
    border: none !important;
    font-weight: 900 !important;
    box-shadow: 0 4px 14px rgba(0, 136, 204, 0.45) !important;
    font-size: 1rem !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #00CCFF 0%, #0099DD 100%) !important;
    box-shadow: 0 6px 20px rgba(0, 136, 204, 0.65) !important;
}

/* ── PLOTLY CHARTS ── */
[data-testid="stPlotlyChart"] {
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 12px rgba(0, 41, 112, 0.10);
    background: #FFFFFF !important;
    border: 1.5px solid #CBD5E1 !important;
}

/* ── EXPANDERS ── */
[data-testid="stExpander"] {
    background: #FFFFFF !important;
    border: 1.5px solid #CBD5E1 !important;
    border-radius: 10px !important;
    box-shadow: 0 2px 8px rgba(0, 41, 112, 0.06) !important;
    margin-bottom: 0.5rem !important;
}
[data-testid="stExpander"] summary {
    color: #002970 !important;
    font-weight: 800 !important;
    font-size: 1rem !important;
}
@media (prefers-color-scheme: dark) {
    [data-testid="stExpander"] {
        background: #001A4A !important;
        border-color: #00BAF2 !important;
    }
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] p,
    [data-testid="stExpander"] span {
        color: #FFFFFF !important;
    }
}

/* ── CHAT INPUT ── */
[data-testid="stChatInput"] {
    border-radius: 12px !important;
}
[data-testid="stChatInput"] textarea {
    color: #000000 !important;
    background: #FFFFFF !important;
    border: 2px solid #00BAF2 !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #475569 !important;
}
[data-testid="stChatMessage"] {
    background: #FFFFFF !important;
    border: 1.5px solid #CBD5E1 !important;
    border-radius: 12px !important;
    box-shadow: 0 2px 6px rgba(0, 41, 112, 0.06) !important;
    margin: 8px 0 !important;
}
@media (prefers-color-scheme: dark) {
    [data-testid="stChatMessage"] {
        background: #001A4A !important;
        border-color: #00BAF2 !important;
    }
    [data-testid="stChatMessage"] * {
        color: #FFFFFF !important;
    }
}

/* ── FOOTER ── */
.paytm-footer {
    text-align: center;
    color: #475569;
    font-size: 0.85rem;
    font-weight: 700;
    padding: 1.4rem 0 0.6rem;
    border-top: 1.5px solid #CBD5E1;
    margin-top: 1.5rem;
}
.paytm-footer b {
    color: #002970;
}
@media (prefers-color-scheme: dark) {
    .paytm-footer {
        color: #A0C4FF !important;
    }
    .paytm-footer b {
        color: #00BAF2 !important;
    }
}
</style>
""", unsafe_allow_html=True)


# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    logo_dark_path = os.path.join(os.path.dirname(__file__), "paytm_logo_dark.png")
    logo_path = os.path.join(os.path.dirname(__file__), "paytm_logo.png")
    if os.path.exists(logo_dark_path):
        st.image(logo_dark_path, width=150)
    elif os.path.exists(logo_path):
        st.image(logo_path, width=150)
    else:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/Paytm_Logo_%28standalone%29.svg/250px-Paytm_Logo_%28standalone%29.svg.png", width=150)
    
    st.markdown("### 🤖 AI Teammate")
    st.caption("Track 3: Autonomous AI Teammates — HackBriven 2026")
    st.markdown("---")

    mode_selection = st.selectbox(
        "🏪 Business Mode",
        options=["custom", "electronics", "cafe"],
        format_func=lambda x: {
            "custom":      "👤 My Business (Live)",
            "electronics": "📱 Demo: Apex Tech & Mobile",
            "cafe":        "☕ Demo: Bean & Brew Cafe"
        }[x],
        index=0 if st.session_state.active_profile == "custom"
              else (1 if st.session_state.active_profile == "electronics" else 2)
    )
    if mode_selection != st.session_state.active_profile:
        st.session_state.active_profile = mode_selection
        load_profile(mode_selection)
        st.rerun()

    current_context  = get_merchant_context()
    merchant         = current_context["merchant"]
    inventory        = current_context["inventory"]
    pending_payments = current_context["pending_payments"]
    sales_trend      = current_context["sales_trend"]

    st.markdown(f"**Business:** {merchant['name']}")
    st.markdown(f"**MID:** `{merchant['merchant_id']}`")
    st.markdown(f"**UPI:** `{merchant.get('upi_id', 'merchant@paytm')}`")
    st.markdown(f"**Balance:** ₹{merchant['paytm_balance']:,}")

    with st.expander("⚙️ Customize My Store"):
        st.caption("Enter your actual business details:")
        new_name  = st.text_input("Store Name",    value=merchant["name"])
        new_mid   = st.text_input("Paytm MID",     value=merchant["merchant_id"])
        new_cat   = st.text_input("Category",      value=merchant["category"])
        new_upi   = st.text_input("Paytm UPI ID",  value=merchant.get("upi_id", "mybusiness@paytm"))
        new_bal   = st.number_input("Balance (₹)", value=int(merchant["paytm_balance"]), step=1000)
        new_phone = st.text_input("Phone",         value=merchant.get("phone", "+91-98765-43210"))
        if st.button("💾 Save Profile", use_container_width=True):
            update_merchant_info(name=new_name, merchant_id=new_mid, category=new_cat,
                                 balance=new_bal, upi_id=new_upi, phone=new_phone)
            st.success("Profile updated!")
            st.rerun()

    with st.expander("➕ Add Debtor / Receivable"):
        st.caption("Add a customer due to test auto-reminders:")
        c_name   = st.text_input("Customer Name",   placeholder="e.g. Ramesh Verma")
        c_phone  = st.text_input("Phone Number",    placeholder="+91-98101-99999")
        c_amount = st.number_input("Amount (₹)", min_value=50, value=750, step=50)
        c_days   = st.number_input("Days Overdue",  min_value=1, value=10)
        c_items  = st.text_input("Items Purchased", placeholder="Order details")
        if st.button("➕ Add Due Record"):
            if c_name and c_phone:
                add_pending_payment(c_name, c_phone, c_amount, c_days, c_items)
                st.success(f"Added due for {c_name}!")
                st.rerun()

    st.markdown("---")

    api_key = st.text_input(
        "🔑 Gemini API Key (Optional)",
        type="password",
        placeholder="AIza...",
        help="aistudio.google.com/apikey — enables live conversational Gemini chat"
    )
    if api_key and len(api_key) > 10:
        st.markdown(
            '<span class="api-badge-ok">✓ API Key Active — Gemini Enabled</span>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<span class="api-badge-none">⚡ Auto Mode — No Key Needed</span>',
            unsafe_allow_html=True
        )
    st.markdown("[Get free key →](https://aistudio.google.com/apikey)")
    st.markdown("---")
    st.markdown("**Autonomous Execution**")
    run_scan = st.button("🔍 Run Full AI Scan", use_container_width=True)
    st.caption("Agent audits transactions, sends reminders, drafts promos & reorders — automatically.")


# ── REFRESH CONTEXT ──────────────────────────────────────────────────────────
current_context  = get_merchant_context()
merchant         = current_context["merchant"]
inventory        = current_context["inventory"]
pending_payments = current_context["pending_payments"]
sales_trend      = current_context["sales_trend"]


# ── MAIN HEADER ──────────────────────────────────────────────────────────────
st.markdown(
    '<p class="paytm-header">🤖 Paytm Merchant <span>AI Teammate</span></p>',
    unsafe_allow_html=True
)
st.markdown(
    f"**Autonomous Business Partner — {merchant['name']}** &nbsp;·&nbsp; "
    f"*{merchant['category']}* &nbsp;·&nbsp; *{datetime.now().strftime('%d %b %Y, %I:%M %p')}*"
)
st.markdown("---")


# ── METRICS ROW ──────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
with col1:
    delta = sales_trend['today'] - sales_trend['yesterday']
    st.metric("💵 Today's Sales", f"₹{sales_trend['today']:,}",
              delta=f"{'+' if delta >= 0 else ''}₹{delta:,}")
with col2:
    total_dues = sum(p['amount'] for p in pending_payments)
    st.metric("⏳ Pending Receivables", f"₹{total_dues:,}",
              delta=f"{len(pending_payments)} customers", delta_color="inverse")
with col3:
    low_stock = [i for i in inventory if i['stock'] <= 3]
    st.metric("🔔 Low Stock Items", len(low_stock),
              delta="Needs Restock", delta_color="inverse")
with col4:
    st.metric("💳 Paytm Balance", f"₹{merchant['paytm_balance']:,}",
              delta=f"UPI: {merchant.get('upi_id', 'Active')}")

st.markdown("---")


# ── CHARTS + TABLES ──────────────────────────────────────────────────────────
left, right = st.columns([1.2, 1])

with left:
    st.subheader("📈 Sales & Revenue Velocity")
    days  = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Today']
    base  = sales_trend['today']
    sales = [int(base*0.70), int(base*0.65), int(base*0.80),
             int(base*0.95), int(base*0.88), int(base*1.10), base]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=days, y=sales,
        marker_color=['#90CAF9']*6 + ['#00BAF2'],
        text=[f'₹{s:,}' for s in sales],
        textposition='outside',
        textfont=dict(color='#002970', size=11)
    ))
    fig.update_layout(
        plot_bgcolor='rgba(255,255,255,1)',
        paper_bgcolor='rgba(255,255,255,1)',
        height=270, margin=dict(t=20, b=10, l=10, r=10),
        yaxis=dict(gridcolor='#E8EDF5', color='#64748B'),
        xaxis=dict(color='#64748B'),
        font=dict(color='#002970', size=11)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📦 Live Inventory & Velocity")
    inv_data = []
    for item in inventory:
        days_left = item['stock'] / item['daily_sales'] if item['daily_sales'] > 0 else 999
        status = ("🔴 Critical" if days_left < 2
                  else "🟡 Low"    if days_left < 5
                  else "🐢 Slow"   if item['days_in_stock'] > 30
                  else "🟢 Healthy")
        inv_data.append({
            "Product / SKU": item['item'],
            "In Stock":      item['stock'],
            "Days Left":     f"{days_left:.1f}d",
            "Unit Price":    f"₹{item['price']}",
            "Status":        status
        })
    st.dataframe(pd.DataFrame(inv_data), use_container_width=True, hide_index=True)

with right:
    st.subheader("💸 Overdue Customer Credit (Udhaar)")
    for p in sorted(pending_payments, key=lambda x: -x['due_days']):
        urgency = "🔴" if p['due_days'] > 10 else ("🟡" if p['due_days'] > 5 else "🔵")
        st.markdown(
            f"<div class='alert-card'>"
            f"{urgency} <b>{p['customer']}</b> — <b>₹{p['amount']}</b><br/>"
            f"Overdue: <b>{p['due_days']} days</b> &nbsp;·&nbsp; {p['items']}<br/>"
            f"<small>📞 {p['phone']}</small></div>",
            unsafe_allow_html=True
        )

    st.markdown("")
    st.subheader("🔥 Top Velocity Products")
    labels = sales_trend['best_selling_today'] + ['Other']
    values = [40, 35, 25] if len(labels) == 3 else [30, 25, 20, 25]
    fig2 = go.Figure(go.Pie(
        labels=labels, values=values[:len(labels)], hole=0.48,
        marker_colors=['#00BAF2', '#0077B6', '#90CAF9', '#BFDBFE']
    ))
    fig2.update_layout(
        height=220, margin=dict(t=10, b=10, l=0, r=0),
        paper_bgcolor='rgba(255,255,255,1)',
        font=dict(color='#002970'), showlegend=True,
        legend=dict(orientation='v', font=dict(size=10, color='#334155'))
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")


# ── AI AGENT SECTION ─────────────────────────────────────────────────────────
st.subheader("🤖 AI Teammate — Autonomous Actions")

if not api_key or len(api_key) <= 10:
    st.info(
        "⚡ **Running in Instant Autonomous Mode** — Scan works without an API key. "
        "Enter a Gemini key in the sidebar to also unlock live conversational chat."
    )

if 'messages'   not in st.session_state: st.session_state.messages   = []
if 'action_log' not in st.session_state: st.session_state.action_log = []

_, col_c = st.columns([6, 1])
with col_c:
    if st.button("🗑️ Clear", use_container_width=True):
        st.session_state.messages   = []
        st.session_state.action_log = []
        st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg['role'],
                         avatar='🤖' if msg['role'] == 'assistant' else '👨‍💼'):
        st.markdown(msg['content'])

# AUTONOMOUS SCAN
if run_scan:
    with st.spinner("🤖 AI Teammate is auditing your business..."):
        try:
            import agent, importlib
            importlib.reload(agent)
            key = api_key if (api_key and len(api_key) > 10) else ""
            result = agent.run_autonomous_scan(key)
            output = result.get('output', 'Scan complete.')
            st.session_state.messages.append({'role': 'assistant', 'content': output})
            from tools import get_action_log
            st.session_state.action_log = get_action_log()
            st.rerun()
        except Exception as e:
            st.error(f"Agent error: {e}")

# CHAT INPUT
user_input = st.chat_input("💬 Ask your AI Teammate anything about your business...")
if user_input:
    st.session_state.messages.append({'role': 'user', 'content': user_input})
    with st.chat_message('user', avatar='👨‍💼'):
        st.markdown(user_input)
    with st.chat_message('assistant', avatar='🤖'):
        with st.spinner("🤖 Thinking..."):
            try:
                import agent, importlib
                importlib.reload(agent)
                history = st.session_state.messages[:-1]
                key     = api_key if (api_key and len(api_key) > 10) else ""
                result  = agent.run_custom_query(key, user_input, history)
                output  = result.get('output', '')
                st.markdown(output)
                st.session_state.messages.append({'role': 'assistant', 'content': output})
                from tools import get_action_log
                st.session_state.action_log = get_action_log()
            except Exception as e:
                st.error(f"Error: {e}")


# ── LIVE ACTION FEED ─────────────────────────────────────────────────────────
if st.session_state.action_log:
    st.markdown("### ⚡ Live Autonomous Action Feed")
    st.caption("Every action below was executed automatically by the AI teammate — no manual prompt needed.")

    ACTION_META = {
        "payment_reminder": {
            "icon": "📨",
            "label": "WhatsApp Payment Reminder Sent",
            "desc": ("The agent detected an overdue customer balance and dispatched a personalised "
                     "WhatsApp reminder with the merchant's Paytm UPI link for instant one-tap payment.")
        },
        "inventory_alert": {
            "icon": "⚠️",
            "label": "Inventory Alert Triggered",
            "desc": ("Stock for this item has dropped below the safe threshold. "
                     "The agent flagged it for reorder before the shelf runs empty and revenue is lost.")
        },
        "promo_draft": {
            "icon": "🎉",
            "label": "Flash Promo Offer Drafted",
            "desc": ("This product has been sitting in inventory too long, tying up working capital. "
                     "The agent auto-drafted a targeted discount campaign to clear dead stock fast.")
        },
        "reorder_alert": {
            "icon": "🔔",
            "label": "Supplier Reorder Alert",
            "desc": ("Based on current run-rate, the agent predicted a stockout and queued a reorder "
                     "alert so the merchant never faces an empty shelf during peak hours.")
        },
        "daily_summary": {
            "icon": "📊",
            "label": "Daily Business Health Summary",
            "desc": ("A consolidated executive view of today's performance — sales velocity, "
                     "receivables status, and inventory health — generated automatically each morning.")
        },
    }

    for i, action in enumerate(reversed(st.session_state.action_log[-8:])):
        atype   = action.get('type', 'action')
        details = action.get('details', {})
        meta    = ACTION_META.get(atype, {
            "icon":  "📋",
            "label": atype.replace('_', ' ').title(),
            "desc":  "Autonomous action executed by the AI teammate."
        })
        with st.expander(f"{meta['icon']} **{meta['label']}**", expanded=(i == 0)):
            st.markdown(
                f"<div style='background:#EFF6FF; border-left:3px solid #00BAF2; "
                f"border-radius:6px; padding:8px 12px; margin-bottom:10px; "
                f"color:#1E3A5F; font-size:0.88rem;'>"
                f"ℹ️ {meta['desc']}</div>",
                unsafe_allow_html=True
            )
            if isinstance(details, dict):
                for k, v in details.items():
                    label = k.replace('_', ' ').title()
                    val   = str(v)
                    if len(val) > 60:
                        st.markdown(f"**{label}:**")
                        st.code(val, language="")
                    else:
                        st.markdown(f"- **{label}:** `{val}`")
            else:
                st.write(details)


st.markdown(
    '<div class="paytm-footer">Paytm Merchant AI Teammate &nbsp;·&nbsp; '
    'Built by <b>Team Cortex Code</b> for HackBriven 2026 &nbsp;·&nbsp; '
    'Track 3: Autonomous AI Teammates &nbsp;·&nbsp; Powered by Gemini Flash ⚡</div>',
    unsafe_allow_html=True
)
