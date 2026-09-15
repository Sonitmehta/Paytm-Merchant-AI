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

## 🔮 Future Roadmap

- [ ] **Live Paytm POS & Soundbox Integration**: Direct webhook integration with Paytm Merchant APIs.
- [ ] **WhatsApp Business Cloud API**: Automated message delivery to customer phones with payment deep-links.
- [ ] **Multi-Lingual Voice Agent**: Voice interaction in Hindi, Tamil, Telugu, and other regional languages for local shop owners.
