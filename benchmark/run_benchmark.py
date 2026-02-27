# benchmark/run_benchmark.py
import sys
import os
import json
import time
from collections import defaultdict

# Add project root to Python path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

from router.pipeline import route_query, init_db

# Initialize database
init_db()

# Load benchmark queries
with open("benchmark/queries.json") as f:
    data = json.load(f)

total = len(data)
correct = 0

# Metrics containers
per_task_total = defaultdict(int)
per_task_correct = defaultdict(int)
latencies = defaultdict(list)
confidences = defaultdict(list)

print("\nRunning benchmark (rate-limited, safe mode)...\n")

for idx, item in enumerate(data, start=1):
    print(f"\n[{idx}/{total}] Processing query...")

    result = route_query(item["query"])

    predicted = result["task_type"]
    actual = item["label"]
    latency = result.get("latency_ms", 0)
    confidence = result.get("confidence", 0)

    # Overall accuracy
    if predicted == actual:
        correct += 1
        per_task_correct[actual] += 1

    per_task_total[actual] += 1
    latencies[predicted].append(latency)
    confidences[predicted].append(confidence)

    print(
        f"Query      : {item['query']}\n"
        f"Predicted  : {predicted}\n"
        f"Actual     : {actual}\n"
        f"Latency    : {latency} ms\n"
        f"Confidence : {confidence}"
    )

    # ✅ VERY IMPORTANT: prevent Gemini 429 error
    time.sleep(2)

# ---------------- FINAL RESULTS ----------------

overall_accuracy = correct / total

print("\n================ FINAL RESULTS ================\n")
print(f"Total Queries       : {total}")
print(f"Correct Predictions : {correct}")
print(f"Overall Accuracy    : {overall_accuracy:.2f}\n")

print("Accuracy per Task:")
for task in per_task_total:
    acc = per_task_correct[task] / per_task_total[task]
    print(f"- {task}: {acc:.2f}")

print("\nAverage Latency per Task:")
for task, values in latencies.items():
    avg = sum(values) / len(values)
    print(f"- {task}: {round(avg, 1)} ms")

print("\nAverage Confidence per Task:")
for task, values in confidences.items():
    avg = sum(values) / len(values)
    print(f"- {task}: {round(avg, 2)}")