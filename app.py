import streamlit as st
import sqlite3
import pandas as pd

from router.pipeline import route_query, init_db

# ---------------- INIT ----------------
init_db()

st.set_page_config(page_title="AI Model Router", page_icon="🧠")
st.title("🧠 AI Model Router")
st.caption("Automatically routes your query to the best free LLM")

# ---------------- INPUT ----------------
query = st.text_area(
    "Ask anything:",
    height=100,
    placeholder="Try: 'Write a Python function to sort a list'"
)

# ---------------- RUN ----------------
if st.button("Route & Answer", type="primary") and query.strip():
    with st.spinner("Classifying query and routing to best model..."):
        result = route_query(query)

    col1, col2, col3 = st.columns(3)
    col1.metric("Task Type", result.get("task_type", "-"))
    col2.metric("Model Used", "openrouter/free")
    col3.metric("Latency", f"{result.get('latency_ms', 0)} ms")

    st.subheader("Answer")

    # ✅ PROPER ERROR HANDLING
    if result.get("answer"):
        st.write(result["answer"])
    else:
        st.error("❌ Model failed to generate an answer.")
        st.code(result.get("error", "Unknown error"))

# ---------------- HISTORY ----------------
st.divider()
st.subheader("📊 Routing History")

conn = sqlite3.connect("data/router.db")
df = pd.read_sql(
    """
    SELECT timestamp, query, task_type, model_used, tokens, latency_ms
    FROM logs
    ORDER BY id DESC
    LIMIT 20
    """,
    conn
)
conn.close()

if not df.empty:
    st.dataframe(df, use_container_width=True)
    st.bar_chart(df["task_type"].value_counts())
else:
    st.info("No routing history yet.")