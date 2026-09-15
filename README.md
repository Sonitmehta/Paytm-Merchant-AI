# 🤖 Paytm Merchant AI Teammate
### HackBriven 2026 — Track 3: Autonomous AI Teammates

---

## 🚀 Setup & Run (5 minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Add your Google AI API key (Free!)
cp .env.example .env
# Edit .env and paste your key from https://aistudio.google.com/apikey

# 3. Run the app
streamlit run app.py
```

Then open http://localhost:8501 in your browser.

---

## 🏗️ Project Structure

```
paytm_merchant_ai/
├── app.py          # Streamlit frontend (dashboard + chat)
├── agent.py        # LangChain agent with Google Gemini Flash
├── tools.py        # 6 autonomous action tools
├── data.py         # Mock merchant data (Paytm-style)
├── requirements.txt
└── README.md
```

## 🤖 What the Agent Does (Autonomously)

1. **Fetches** merchant sales, inventory & payment data
2. **Sends** WhatsApp payment reminders to overdue customers
3. **Flags** slow-moving inventory items
4. **Drafts** promotional offers for dead stock
5. **Alerts** for low-stock items needing reorder
6. **Generates** a full daily business summary

## 🛠️ Tech Stack
- **LLM:** Google Gemini Flash via Google AI Studio (Free Tier)
- **Agent Framework:** LangChain (Tool Calling Agent)
- **Frontend:** Streamlit
- **Charts:** Plotly
- **Data:** Mock Paytm merchant dataset

## 🎯 Demo Flow for Judges
1. Open the dashboard — show real-time merchant metrics
2. Enter your free Google AI API key → click **"Run Full AI Scan"**
3. Watch the agent autonomously:
   - Send payment reminders
   - Flag slow inventory
   - Draft a promo offer
   - Generate daily summary
4. Ask it a custom question in the chat (maintains multi-turn conversation memory)
5. Show the Action Log — proof of autonomous execution
