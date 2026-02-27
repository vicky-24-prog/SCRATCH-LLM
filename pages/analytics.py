# pages/analytics.py

import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Analytics", page_icon="📊")
st.title("📊 AI Model Router — Analytics Dashboard")
st.caption("System-level observability for routing, quality, and latency")

DB_PATH = "data/router.db"

# ---------------- LOAD DATA ----------------

conn = sqlite3.connect(DB_PATH)
df = pd.read_sql("SELECT * FROM logs", conn)
conn.close()

if df.empty:
    st.warning("No data available yet. Run some queries first.")
    st.stop()

# ---------------- TOP KPIs ----------------

st.subheader("🔢 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Queries", len(df))
col2.metric("Unique Models", df["model_used"].nunique())
col3.metric("Avg Latency", f"{int(df['latency_ms'].mean())} ms")
col4.metric("Avg Quality", round(df["quality_score"].mean(), 2))

st.divider()

# ---------------- ROUTING DISTRIBUTION ----------------

st.subheader("🧭 Routing Distribution (by Task Type)")
task_counts = df["task_type"].value_counts()
st.bar_chart(task_counts)

# ---------------- MODEL USAGE ----------------

st.subheader("🤖 Model Usage Frequency")
model_counts = df["model_used"].value_counts()
st.bar_chart(model_counts)

# ---------------- LATENCY ANALYSIS ----------------

st.subheader("⏱️ Average Latency per Model")
latency_by_model = df.groupby("model_used")["latency_ms"].mean().sort_values()
st.bar_chart(latency_by_model)

# ---------------- QUALITY ANALYSIS ----------------

st.subheader("⭐ Average Quality Score per Model")
quality_by_model = (
    df.groupby("model_used")["quality_score"]
    .mean()
    .sort_values(ascending=False)
)
st.bar_chart(quality_by_model)

# ---------------- TASK QUALITY ----------------

st.subheader("📚 Quality Score per Task Type")
quality_by_task = df.groupby("task_type")["quality_score"].mean()
st.bar_chart(quality_by_task)

# ---------------- RAW DATA ----------------

with st.expander("🗂️ View Raw Logs"):
    st.dataframe(df, use_container_width=True)