import google.generativeai as genai
import os
import time
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_KEY"))

VALID_TYPES = ["CODING", "MATH", "FACTUAL_QA", "SUMMARIZATION", "CREATIVE"]

def classify_query(query: str) -> dict:
    model = genai.GenerativeModel("gemini-2.0-flash")

    prompt = f"""
Classify the user query into exactly ONE category:
CODING, MATH, FACTUAL_QA, SUMMARIZATION, CREATIVE

Rules:
- CODING: any request to write, debug, or explain code
- MATH: calculations, equations, proofs, statistics
- FACTUAL_QA: questions about facts, people, places, history
- SUMMARIZATION: requests to summarize, shorten, or condense text
- CREATIVE: writing, poems, stories, brainstorming

Also provide a confidence score between 0 and 1.

Return format ONLY:
CATEGORY | CONFIDENCE

Query:
{query}
"""

    for attempt in range(3):
        try:
            response = model.generate_content(prompt)
            text = response.text.strip()

            category, confidence = text.split("|")
            category = category.strip().upper()
            confidence = float(confidence.strip())

            if category not in VALID_TYPES:
                category = "FACTUAL_QA"

            return {
                "task_type": category,
                "confidence": round(confidence, 2)
            }

        except Exception as e:
            if attempt == 2:
                # FINAL fallback — NEVER crash
                return {
                    "task_type": "FACTUAL_QA",
                    "confidence": 0.0,
                    "error": str(e)
                }
            time.sleep(2)

    return {
        "task_type": "FACTUAL_QA",
        "confidence": 0.0
    }