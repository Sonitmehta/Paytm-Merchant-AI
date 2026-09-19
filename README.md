# 🤖 Paytm Merchant AI Teammate

An autonomous AI business teammate and intelligent analytics dashboard designed for Paytm merchants. Powered by **Google Gemini Flash** and **LangChain/LangGraph**, the agent proactively manages daily retail operations—tracking inventory, recovering overdue customer credit via WhatsApp, and generating targeted promotional offers to move slow-selling stock.

---

## ✨ Key Features

- 📊 **Real-Time Merchant Dashboard**: Interactive Streamlit interface visualizing daily sales, inventory levels, GMV, and payment collections using Plotly.
- ⚡ **Autonomous Decision-Making**: Proactively scans store data to identify critical operational risks without requiring manual merchant oversight.
- 💬 **WhatsApp Payment Recovery**: Automatically detects customers with overdue payments and drafts personalized, polite WhatsApp payment reminders.
- 📦 **Dead-Stock & Low-Stock Alerts**: Detects stagnant inventory to prevent capital lock-up and sends reorder alerts for critical fast-moving goods.
- 🎯 **Dynamic Promotional Campaigns**: Automatically creates customized discount campaigns for slow-moving products to drive sales velocity.
- 🗣️ **Interactive Merchant Copilot**: Conversational AI teammate maintaining conversational memory to answer questions regarding business health, revenue, and daily trends.

---

## 🏗️ Project Architecture

`
┌────────────────────────────────────────────────────────┐
│               Streamlit Web Interface                  │
│       (KPI Cards, Charts, Chatbot, Action Log)         │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│            Autonomous LangChain / LangGraph Agent       │
│           (Google Gemini Flash Reasoning Engine)       │
└──────────────────────────┬─────────────────────────────┘
                           │ Tool Invocation
                           ▼
┌────────────────────────────────────────────────────────┐
│                     Agent Tools                        │
│  • get_merchant_data      • send_payment_reminder      │
│  • flag_slow_inventory    • draft_promotional_offer    │
│  • reorder_alert          • generate_daily_summary     │
└──────────────────────────┬─────────────────────────────┘
                           │
                           ▼
┌────────────────────────────────────────────────────────┐
│            Data Layer (Paytm Merchant Store)           │
│    Sales Trends • Inventory Records • Customer Udhaar  │
└────────────────────────────────────────────────────────┘
`

---

## 📁 Repository Structure

`
paytm_merchant_ai/
├── app.py              # Streamlit frontend (dashboard + chat + action logger)
├── agent.py            # LangChain/LangGraph autonomous ReAct agent & fallbacks
├── tools.py            # Autonomous business action tools
├── data.py             # Mock merchant dataset (Paytm-style retail data)
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
└── README.md           # Project documentation
`

---

## 🛠️ Tech Stack

- **LLM Engine:** Google Gemini Flash via Google AI Studio
- **Agent Framework:** LangChain & LangGraph (ReAct Tool-Calling Agent)
- **Frontend & UI:** Streamlit
- **Visualizations:** Plotly
- **Data Handling:** Pandas & Python standard libraries

---

## 🚀 Getting Started

### 1. Clone the Repository
`ash
git clone https://github.com/Sonitmehta/Paytm-Merchant-AI.git
cd Paytm-Merchant-AI
`

### 2. Install Dependencies
`ash
pip install -r requirements.txt
`

### 3. Configure API Key
Create a .env file in the root directory (or use .env.example as a template):
`ash
cp .env.example .env
`
Add your free Google Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey):
`env
GOOGLE_API_KEY=your_gemini_api_key_here
`
*(Alternatively, enter your API key directly in the web UI sidebar at runtime)*

### 4. Run the Application
`ash
streamlit run app.py
`
Visit http://localhost:8501 in your browser to launch the dashboard.

---

---

## 🔮 Future Scope & Paytm Business Integration Architecture

The **Paytm Merchant AI Teammate** is designed from the ground up as a native extension of the Paytm Business ecosystem. In production, it does not live in an external dashboard—it operates directly inside the **Paytm for Business** mobile application and POS hardware installed across millions of Indian merchants.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PAYTM FOR BUSINESS ECOSYSTEM ARCHITECTURE                │
├───────────────────────────────┬─────────────────────────────────────────────┤
│   MERCHANT HARDWARE & APPS    │              AI TEAMMATE ENGINE             │
│  • Paytm for Business App     │  • Autonomous LangGraph ReAct Decision Loop │
│  • Paytm Soundbox (Voice TTS) │  • Google Gemini Flash (Vertex AI / GCP)    │
│  • Paytm Smart POS Terminal   │  • Zero-Failure Deterministic Fallback      │
├───────────────────────────────┴─────────────────────────────────────────────┤
│                            INTEGRATION CAPABILITIES                         │
│  1. In-App Native Integration  ·  2. Soundbox Voice Alerts                  │
│  3. WhatsApp Cloud Webhooks    ·  4. Autonomous Supplier Reordering         │
│  5. Dynamic Price Decay Engine ·  6. Real-Time Settlement Reconciliation    │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 📱 1. Native Paytm for Business In-App Experience
- **Zero Configuration / Keyless Onboarding:** Merchants never handle API keys. Authentication and model provisioning are abstracted entirely behind Paytm's enterprise Vertex AI / GCP backend through existing merchant Single Sign-On (SSO / JWT).
- **3-Tap Merchant Journey:**
  1. *Discovery:* Merchant opens the Paytm for Business app; a native hero banner prompts: `🤖 Meet your Autonomous AI Teammate`.
  2. *Audit:* Upon a single tap on `Enable Teammate`, the agent scans the past 30 days of settlements, Khata ledger, and product turnover in the background.
  3. *Immediate Action:* Within 10 seconds, the agent presents its first high-impact recovery card: *"You have ₹18,400 uncollected in pending customer credit. Want me to send polite WhatsApp reminders?"*

---

### 🔊 2. Paytm Soundbox Voice Integration (Screenless Operation)
For retail merchants who don't have time to stare at smartphone screens during busy store hours, the AI teammate connects directly to the **Paytm Soundbox**:
- **Proactive Audio Briefings:** Every morning upon Soundbox power-on: *"Good morning! Yesterday's sales were ₹24,500. 3 high-velocity items need restock today."*
- **Real-Time Debt Recovery Announcements:** When an overdue customer pays through the automated WhatsApp UPI link: *"Paytm par ₹850 prapt hue — Ramesh Verma ka udhaar clear ho gaya."*

---

### 💬 3. WhatsApp Business Cloud Webhook Architecture
- **Interactive Action Buttons:** Replaces static text reminders with interactive WhatsApp Cloud messages containing direct, pre-filled **"Pay via Paytm UPI"** deep-link buttons.
- **Delivery & Settlement State Tracking:** Tracks WhatsApp delivery, read receipts, and maps successful incoming UPI callbacks (`PAYMENT_SUCCESS`) to automatically clear debtor balances in the merchant's Khata.

---

### 📦 4. Autonomous B2B Supplier Ordering (Closed-Loop Inventory)
- **Predictive Run-Rate Analysis:** Automatically monitors SKU turnover velocities to forecast exact out-of-stock timelines.
- **Distributor Purchase Order Dispatch:** When inventory drops below safety thresholds, the agent automatically drafts a standardized Purchase Order (PO) and transmits it via WhatsApp or B2B EDI to authorized wholesale distributors.

---

### 🏷️ 5. Algorithmic Price Decay Engine (Dead-Stock Liquidation)
- **Automatic Capital Unlocking:** Inventory sitting idle for >30 days ties up working capital. The agent monitors aging stock and dynamically executes a staged discount decay curve:
  - *Day 30:* 5% promotional broadcast to frequent store customers.
  - *Day 40:* 15% flash clearance offer broadcast via WhatsApp and Paytm POS shelf tags.
  - *Result:* Liquidates dead stock into cash without merchant calculation or intervention.

---

### 🗺️ 3-Phase Strategic Rollout Roadmap

| Phase | Timeline | Key Deliverables & Milestones |
| :--- | :--- | :--- |
| **Phase 1: Core Integration** | 0 – 6 Months | Native Paytm for Business Android integration; live Khata database synchronization; automated WhatsApp reminders with UPI deep-links; Soundbox voice alerts; multi-lingual voice support (*Hindi, Tamil, Telugu, Gujarati*). |
| **Phase 2: Intelligence Layer** | 6 – 18 Months | Seasonal demand forecasting (*Diwali, Eid, Holi demand spikes*); automated supplier PO generation; dynamic shelf price decay engine; GST-compliant auto-reconciliation; customer creditworthiness scoring for micro-loans. |
| **Phase 3: Ecosystem Scale** | 18+ Months | B2B wholesale marketplace integration; automated collateral-free Paytm Business credit line provisioning; multi-store franchise management; ONDC marketplace automated inventory cataloging. |

---

## 👥 Team Cortex Code

- **Track:** Track 3 — Autonomous AI Teammates
- **Event:** HackBriven 2026
- **Live Demo:** [https://paytm-merchant-ai-2kzmjgpc4z5egbdfefgyjd.streamlit.app](https://paytm-merchant-ai-2kzmjgpc4z5egbdfefgyjd.streamlit.app)

