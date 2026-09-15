# Paytm Merchant AI Teammate - Streamlit Frontend
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from data import MERCHANT, INVENTORY, PENDING_PAYMENTS, SALES_TREND
from tools import get_action_log, ACTION_LOG

st.set_page_config(
    page_title="Paytm Merchant AI Teammate",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header { font-size: 2rem; font-weight: 700; color: #00BAF2; }
    .metric-card { background: #1e1e2e; padding: 1rem; border-radius: 10px; border-left: 4px solid #00BAF2; }
    .alert-card { background: #2d1b1b; padding: 0.8rem; border-radius: 8px; border-left: 4px solid #ff4444; margin: 0.3rem 0; }
    .success-card { background: #1b2d1b; padding: 0.8rem; border-radius: 8px; border-left: 4px solid #44ff44; margin: 0.3rem 0; }
    .agent-message { background: #1a1a2e; padding: 1rem; border-radius: 10px; border: 1px solid #00BAF2; margin: 0.5rem 0; }
    .stButton>button { background-color: #00BAF2; color: white; border-radius: 8px; border: none; font-weight: 600; }
    .stButton>button:hover { background-color: #0099CC; }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/Paytm_Logo_%28standalone%29.svg/320px-Paytm_Logo_%28standalone%29.svg.png", width=140)
    st.markdown("## 🤖 AI Teammate")
    st.markdown("---")
    st.markdown(f"**Merchant:** {MERCHANT['name']}")
    st.markdown(f"**ID:** {MERCHANT['merchant_id']}")
    st.markdown(f"**Category:** {MERCHANT['category']}")
    st.markdown(f"**Location:** {MERCHANT['location']}")
    st.markdown("---")

    api_key = st.text_input(
        "🔑 Google AI API Key",
        type="password",
        placeholder="AIza...",
        help="Free key from Google AI Studio"
    )
    st.markdown("[🆓 Get free API key →](https://aistudio.google.com/apikey)", unsafe_allow_html=False)
    st.markdown("---")
    st.markdown("**⚡ Quick Actions**")
    run_scan = st.button("🔍 Run Full AI Scan", use_container_width=True)
    st.markdown("*Agent autonomously checks payments, inventory & sales*")

# Main Header
st.markdown('<p class="main-header">🤖 Paytm Merchant AI Teammate</p>', unsafe_allow_html=True)
st.markdown(f"*Autonomous AI for **{MERCHANT['name']}** — {datetime.now().strftime('%d %b %Y, %I:%M %p')}*")
st.markdown("---")

# Metrics Row
col1, col2, col3, col4 = st.columns(4)
with col1:
    delta = SALES_TREND['today'] - SALES_TREND['yesterday']
    st.metric("💵 Today's Sales", f"₹{SALES_TREND['today']:,}", delta=f"+₹{delta:,}")
with col2:
    total_dues = sum(p['amount'] for p in PENDING_PAYMENTS)
    st.metric("⏳ Pending Dues", f"₹{total_dues:,}", delta=f"{len(PENDING_PAYMENTS)} customers", delta_color="inverse")
with col3:
    low_stock = [i for i in INVENTORY if i['stock'] <= 3]
    st.metric("🔔 Low Stock Items", len(low_stock), delta="Need reorder", delta_color="inverse")
with col4:
    st.metric("💳 Paytm Balance", f"₹{MERCHANT['paytm_balance']:,}")

st.markdown("---")

# Two column layout
left, right = st.columns([1.2, 1])

with left:
    # Sales Chart
    st.subheader("📈 Sales Performance")
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Today']
    sales = [3200, 2900, 3600, 4100, 3800, 4500, SALES_TREND['today']]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=days, y=sales,
        marker_color=['#4a9eff']*6 + ['#00BAF2'],
        text=[f'₹{s:,}' for s in sales],
        textposition='outside'
    ))
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=280,
        margin=dict(t=20, b=20),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        font=dict(color='white')
    )
    st.plotly_chart(fig, use_container_width=True)

    # Inventory Table
    st.subheader("📦 Inventory Status")
    inv_data = []
    for item in INVENTORY:
        days_left = item['stock'] / item['daily_sales'] if item['daily_sales'] > 0 else 999
        status = "🔴 Critical" if days_left < 2 else ("🟡 Low" if days_left < 5 else ("🐢 Slow" if item['days_in_stock'] > 30 else "🟢 OK"))
        inv_data.append({
            "Item": item['item'],
            "Stock": item['stock'],
            "Days Left": f"{days_left:.1f}d",
            "Price": f"₹{item['price']}",
            "Status": status
        })
    st.dataframe(pd.DataFrame(inv_data), use_container_width=True, hide_index=True)

with right:
    # Pending Payments
    st.subheader("💸 Pending Payments")
    for p in sorted(PENDING_PAYMENTS, key=lambda x: -x['due_days']):
        urgency = "🔴" if p['due_days'] > 10 else ("🟡" if p['due_days'] > 5 else "🔵")
        with st.container():
            st.markdown(f"""
            <div class='alert-card'>
            {urgency} <b>{p['customer']}</b> — <b>₹{p['amount']}</b><br/>
            Due: {p['due_days']} days ago · {p['items']}<br/>
            <small>{p['phone']}</small>
            </div>""", unsafe_allow_html=True)

    st.markdown("")

    # Best sellers donut
    st.subheader("🔥 Top Sellers Today")
    labels = SALES_TREND['best_selling_today'] + ['Others']
    values = [30, 25, 20, 25]
    fig2 = go.Figure(go.Pie(
        labels=labels, values=values,
        hole=0.5,
        marker_colors=['#00BAF2', '#4a9eff', '#7bc8ff', '#c0e8ff']
    ))
    fig2.update_layout(
        height=220,
        margin=dict(t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        showlegend=True,
        legend=dict(orientation='v', font=dict(size=10))
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# AI Agent Section
st.subheader("🤖 AI Teammate — Autonomous Actions")

if not api_key:
    st.info("🔑 Enter your **Google AI API Key** in the sidebar to activate the AI Teammate. [Get a free key →](https://aistudio.google.com/apikey)")
else:
    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'action_log' not in st.session_state:
        st.session_state.action_log = []

    # Clear chat button
    col_chat, col_clear = st.columns([6, 1])
    with col_clear:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.messages = []
            st.session_state.action_log = []
            st.rerun()

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg['role'], avatar='🤖' if msg['role'] == 'assistant' else '👨‍💼'):
            st.markdown(msg['content'])

    # Autonomous scan
    if run_scan:
        with st.spinner("🤖 Gemini is scanning your business..."):
            try:
                import agent
                import importlib
                importlib.reload(agent)
                result = agent.run_autonomous_scan(api_key)
                output = result.get('output', 'Scan complete.')
                st.session_state.messages.append({'role': 'assistant', 'content': output})
                from tools import get_action_log
                st.session_state.action_log = get_action_log()
                st.rerun()
            except Exception as e:
                st.error(f"Agent error: {e}")

    # Custom query with streaming display
    user_input = st.chat_input("💬 Ask your AI Teammate anything about your business...")
    if user_input:
        st.session_state.messages.append({'role': 'user', 'content': user_input})
        with st.chat_message('user', avatar='👨‍💼'):
            st.markdown(user_input)

        with st.chat_message('assistant', avatar='🤖'):
            with st.spinner("🤖 Gemini is thinking..."):
                try:
                    import agent
                    import importlib
                    importlib.reload(agent)
                    # Pass full chat history for persistent memory
                    history = st.session_state.messages[:-1]  # exclude current msg
                    result = agent.run_custom_query(api_key, user_input, history)
                    output = result.get('output', '')
                    st.markdown(output)
                    st.session_state.messages.append({'role': 'assistant', 'content': output})
                    from tools import get_action_log
                    st.session_state.action_log = get_action_log()
                except Exception as e:
                    err_msg = f"⚠️ Error: {e}"
                    st.error(err_msg)

    # Action Log (Autonomous Proof for Judges)
    if st.session_state.action_log:
        st.markdown("### ⚡ Live Autonomous Action Feed")
        for i, action in enumerate(reversed(st.session_state.action_log[-8:])):
            act_type = action.get('type', 'Action').replace('_', ' ').title()
            details = action.get('details', {})
            
            # Formatted badge color
            badge_icon = "📨" if "payment" in action['type'] else ("⚠️" if "inventory" in action['type'] else ("🎉" if "promo" in action['type'] else ("🔔" if "reorder" in action['type'] else "📊")))
            with st.expander(f"{badge_icon} **{act_type}** — Auto-Executed", expanded=(i == 0)):
                if isinstance(details, dict):
                    for k, v in details.items():
                        st.markdown(f"- **{k.replace('_', ' ').title()}**: `{v}`" if isinstance(v, (int, float, str)) and len(str(v)) < 50 else f"- **{k.replace('_', ' ').title()}**:\n```\n{v}\n```")
                else:
                    st.write(details)

st.markdown("---")
st.markdown("<center><small>Paytm Merchant AI Teammate — Built by <b>Team Cortex Code</b> for HackBriven 2026 · Track 3: Autonomous AI Teammates · Powered by Gemini 3.6 Flash ⚡</small></center>", unsafe_allow_html=True)
