import streamlit as st
import pandas as pd
import time

from router.caller import get_answer
from benchmark.evaluate import score_answer

st.set_page_config(page_title="Compare LLMs", page_icon="🔍")
st.title("🔍 Compare LLM Responses")
st.caption("Side-by-side comparison of multiple free LLM runs (provider-level)")

query = st.text_area(
    "Enter a query to compare:",
    height=100,
    placeholder="Try: Explain recursion in simple terms"
)

num_runs = st.slider(
    "Number of runs (free tier, randomized internally)",
    min_value=2,
    max_value=4,
    value=3
)

if st.button("Compare") and query.strip():

    rows = []

    for i in range(num_runs):
        with st.spinner(f"Running model {i+1}..."):
            result = get_answer(query, "openrouter/free")

        if result.get("answer"):
            quality = score_answer(query, result["answer"])
            answer_text = result["answer"]
        else:
            quality = 0.0
            answer_text = "❌ Model failed to generate an answer."

        rows.append({
            "Run": f"Run {i+1}",
            "Provider": "openrouter/free",
            "Latency (ms)": result.get("latency_ms", 0),
            "Quality Score": round(quality, 2),
            "Answer": answer_text
        })

        time.sleep(1)  # reduce rate-limit collisions

    df = pd.DataFrame(rows)

    st.subheader("📊 Comparison Summary")
    st.dataframe(
        df.drop(columns=["Answer"]),
        use_container_width=True
    )

    st.subheader("📝 Detailed Answers")

    for _, row in df.iterrows():
        with st.expander(f"{row['Run']} | Quality: {row['Quality Score']} | Latency: {row['Latency (ms)']} ms"):
            st.markdown(row["Answer"])