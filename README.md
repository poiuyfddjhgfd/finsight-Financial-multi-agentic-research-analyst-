# 🔍 FinSight — Multi-Agent Financial Research Analyst

> An AI-powered full-stack stock research platform built with a hierarchical multi-agent architecture. Enter any company name and get a comprehensive financial report in seconds.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![React](https://img.shields.io/badge/React-18.x-61dafb?style=flat-square&logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi)
![Vercel](https://img.shields.io/badge/Frontend-Vercel-black?style=flat-square&logo=vercel)
![Railway](https://img.shields.io/badge/Backend-Railway-purple?style=flat-square)

---

## 🌐 Live Demo

| Layer | URL |
|-------|-----|
| 🎨 React Frontend | [finsight-financial-multi-agentic-research-analyst-472juvvpk.vercel.app](https://finsight-financial-multi-agentic-research-analyst-472juvvpk.vercel.app/) |
| ⚙️ FastAPI Backend | [Railway Deployment](https://finsight-financial-multi-agentic-research-analys-production.up.railway.app) |
| 📖 API Docs | [/docs](https://finsight-financial-multi-agentic-research-analys-production.up.railway.app/docs) |

---

## 📸 Screenshots

### 📈 Technical Analysis
![Technical Analysis](assets/Technical.png)

### 📊 Fundamental Analysis
![Fundamental Analysis](assets/fundamental.png)

### 📰 Sentiment Analysis
![Sentiment Analysis](assets/sentiments.png)

---

## 🧠 What is FinSight?

FinSight is a **Full-Stack Multi-Agent Financial Research System** that orchestrates 4 specialized AI agents to produce a comprehensive stock analysis report — covering technical indicators, fundamental health, and news sentiment — for any publicly traded company worldwide.

---

## ⚙️ Architecture

```
User Input: "Apple" or "AAPL"
        ↓
React Frontend (Vercel)
        ↓ POST /analyze
FastAPI Backend (Railway)
        ↓
  Name Resolver (yfinance Search)
        ↓
  Orchestrator Agent
  ┌─────────┬──────────────┬──────────────┐
  ↓         ↓              ↓              ↓
Data     Technical    Fundamental    Sentiment
Collector  Analyst      Analyst        Agent
(yfinance) (RSI/SMA/   (Market Cap/  (VADER NLP)
           MACD)        Revenue)
  └─────────┴──────────────┴──────────────┘
                    ↓
            JSON Response → React UI
```

---

## 🚀 Features

| Feature | Description |
|--------|-------------|
| 🏢 Company Name Search | Enter full name like "Reliance Industries" — auto-resolves to ticker |
| 📈 Technical Analysis | RSI (14), SMA (20), MACD with buy/sell signals |
| 📊 Fundamental Analysis | Market Cap, Revenue Growth YoY, 52-Week Range |
| 📰 Sentiment Analysis | VADER NLP on user-provided headlines with score visualization |
| 💱 Multi-Currency | Automatically detects USD, INR, EUR, GBP |
| 🌍 Global Stocks | Works with NSE (India), NASDAQ, NYSE, LSE and more |
| ⚡ REST API | FastAPI backend with Swagger docs |
| 🎨 Modern UI | React.js dark theme with tabbed analysis |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | `React.js` |
| Backend | `FastAPI` |
| Data | `yfinance` |
| NLP Sentiment | `vaderSentiment` |
| Frontend Deploy | `Vercel` |
| Backend Deploy | `Railway.app` |
| Language | `Python 3.10+`, `JavaScript` |

---

## 📁 Project Structure

```
finsight/
├── agents/
│   ├── data_collector.py      # yfinance wrapper
│   ├── technical.py           # RSI, SMA, MACD indicators
│   ├── fundamental.py         # Market cap, revenue, 52-week range
│   ├── sentiment.py           # VADER sentiment analysis
│   └── orchestrator.py        # Coordinates all agents
├── tools/
│   ├── indicators.py          # RSI, SMA, MACD calculation logic
│   └── name_resolver.py       # Company name → ticker symbol
├── frontend/
│   └── src/
│       └── App.js             # React frontend
├── assets/
│   ├── Technical.png
│   ├── fundamental.png
│   └── sentiments.png
├── app.py                     # Gradio UI (alternative)
├── main.py                    # FastAPI backend
├── requirements.txt
└── README.md
```

---

## 🔧 Local Setup

### Backend

```bash
git clone https://github.com/poiuyfddjhgfd/finsight-Financial-multi-agentic-research-analyst-.git
cd finsight-Financial-multi-agentic-research-analyst-

python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt
```

Create `.env` file:
```
GROQ_API_KEY=your_groq_api_key_here
```

Run FastAPI:
```bash
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm start
```

Open `http://localhost:3000`

---

## 📊 How to Use

1. Enter a **company name** (e.g., `Apple`, `Reliance Industries`, `Tesla`) or ticker (`AAPL`, `RELIANCE.NS`)
2. Paste **recent news headlines** (one per line) for sentiment analysis
3. Click **"Run Analysis →"**
4. View results across 3 tabs:
   - **Technical** — Price, RSI, SMA, MACD
   - **Fundamental** — Market Cap, Revenue Growth, 52-Week Range
   - **Sentiment** — Overall market tone with score visualization

---

## 💡 Example Output

**Input:** `Apple` + headline: *"Apple reports record breaking revenue this quarter"*

```
Technical Analysis (AAPL)
├── Current Price: $327.50
├── RSI (14): 70.23 → Overbought (Sell)
├── SMA (20): 301.93 → Bullish (Buy)
└── MACD: Line 6.56 | Signal 3.78 → Bullish Momentum (Buy)

Fundamental Analysis
├── Market Cap: $4,810.11 Billion
├── Revenue Growth (YoY): +6.43%
└── 52-Week Range: $201.50 — $328.73

Sentiment Analysis
├── Overall: NEGATIVE
└── Score: -0.113 / 1.0
```

---

## 👨‍💻 Author

**Rahul Kumar Yadav**
- Integrated M.Sc. Mathematics & Computing — BIT Mesra
- BS Data Science — IIT Madras
- Associate Vice President, Data Science Club — BIT Mesra

[![GitHub](https://img.shields.io/badge/GitHub-poiuyfddjhgfd-black?style=flat-square&logo=github)](https://github.com/poiuyfddjhgfd)

---

## 📄 License

MIT License — feel free to fork and build upon this project.