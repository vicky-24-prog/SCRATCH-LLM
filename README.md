# SCRATCH-LLM 🧠  
**AI Model Router with Benchmarking, Compare Mode & Observability Dashboard**

An end-to-end AI system that intelligently classifies user queries, routes them to the most suitable free LLM, evaluates response quality using an LLM-as-a-Judge, and provides full observability via analytics and comparison dashboards.

> This project is built to demonstrate **real AI engineering practices** — routing, evaluation, benchmarking, and system observability — not just prompt demos.

---

## 🚀 What This Project Does

- 🔍 **Classifies queries** into task types (Coding, Math, Factual QA, Summarization, Creative) using **Gemini Flash**
- ⚡ **Routes queries** to the optimal free LLM via **OpenRouter**
- 🧪 **Benchmarks routing accuracy** on a labeled dataset
- ⭐ **Evaluates answer quality** using Gemini as an automated judge (LLM-as-Judge)
- 🔍 **Compare Mode** to visually compare multiple LLM outputs side-by-side
- 📊 **Analytics Dashboard** for latency, quality, routing distribution, and usage insights
- 🗄️ **SQLite logging** for full system observability

---

## 🧠 System Architecture (High Level)
```
User Query
│
▼
Gemini Flash (Classifier)
│ → Task Type + Confidence
▼
Routing Logic
│
▼
OpenRouter (free models)
│
▼
Answer + Latency + Tokens
│
▼
SQLite Logs
│
├─ Benchmarking
├─ Quality Scoring (Gemini Judge)
└─ Streamlit Dashboards
```
---

## 🧩 Tech Stack

- **Python**
- **Gemini 2.0 Flash** (classification + quality scoring)
- **OpenRouter** (free LLM inference)
- **Streamlit** (UI + dashboards)
- **SQLite** (logging & analytics)
- **Pandas** (analysis)

---

## 📁 Project Structure
```
SCRATCH-LLM/
│
├── app.py # Main Streamlit app (Router UI)
├── test_router.py # Smoke test for routing
│
├── router/
│ ├── classifier.py # Gemini-based task classifier
│ ├── selector.py # Routing logic
│ ├── caller.py # OpenRouter API calls
│ └── pipeline.py # End-to-end routing pipeline
│
├── benchmark/
│ ├── queries.json # 50 labeled benchmark queries
│ ├── run_benchmark.py # Routing accuracy evaluation
│ └── evaluate.py # Gemini-as-judge quality scoring
│
├── pages/
│ ├── compare.py # Compare Mode (side-by-side LLM outputs)
│ └── analytics.py # Observability dashboard
│
├── data/
│ └── router.db # SQLite database (ignored by git)
│
├── requirements.txt
└── .gitignore

```

## ⚙️ Setup & Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/vicky-24-prog/SCRATCH-LLM.git
cd SCRATCH-LLM
python -m venv venv
venv\Scripts\activate
python -m venv venv
venv\Scripts\activate
GEMINI_KEY=your_gemini_api_key
OPENROUTER_KEY=your_openrouter_api_key
