# test_router.py
import time
import random
import json

from router.pipeline import route_query, init_db

# Initialize database
init_db()

# --------------------------------------------------
# PART 1: SMOKE TEST (Fixed queries)
# --------------------------------------------------
smoke_queries = [
    "Write a Python function to calculate the factorial of a number",
    "Solve 2x + 5 = 15",
    "Summarize this article about AI",
    "Who is Elon Musk?",
    "Write a poem about Mumbai rain"
]

print("\n=== SMOKE TEST (Fixed Queries) ===")

for q in smoke_queries:
    result = route_query(q)

    print("\n---")
    print("Query      :", q)
    print("Task Type  :", result["task_type"])
    print("Confidence :", result["confidence"])
    print("Model Used :", result["model"])
    print("Latency    :", result.get("latency_ms"), "ms")

    # ✅ IMPORTANT: prevent Gemini rate-limit
    time.sleep(1.2)

# --------------------------------------------------
# PART 2: RANDOM SAMPLE FROM BENCHMARK
# --------------------------------------------------
print("\n=== RANDOM TEST FROM BENCHMARK ===")

with open("benchmark/queries.json") as f:
    benchmark_data = json.load(f)

# Take small random sample to save API quota
sample = random.sample(benchmark_data, k=3)

for item in sample:
    q = item["query"]
    expected = item["label"]

    result = route_query(q)

    print("\n---")
    print("Query      :", q)
    print("Expected   :", expected)
    print("Predicted  :", result["task_type"])
    print("Confidence :", result["confidence"])
    print("Model Used :", result["model"])
    print("Latency    :", result.get("latency_ms"), "ms")

    # ✅ IMPORTANT: prevent Gemini rate-limit
    time.sleep(1.2)

print("\n✅ test_router.py completed successfully.")