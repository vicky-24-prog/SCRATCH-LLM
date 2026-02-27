# router/pipeline.py

import sqlite3
import os

from .classifier import classify_query
from .selector import select_model
from .caller import get_answer

# ---------------- DATABASE CONFIG ----------------

DB_DIR = "data"
DB_PATH = os.path.join(DB_DIR, "router.db")


def init_db():
    """
    Initialize SQLite database and logs table.
    """
    os.makedirs(DB_DIR, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            query TEXT,
            task_type TEXT,
            confidence REAL,
            model_used TEXT,
            tokens INTEGER,
            latency_ms INTEGER,
            answer TEXT
        )
        """
    )
    conn.commit()
    conn.close()


# ---------------- MAIN PIPELINE ----------------

def route_query(user_query: str) -> dict:
    """
    Full routing pipeline:
    1. Classify query using Gemini (safe + retry)
    2. Select best model based on task + confidence
    3. Get answer from OpenRouter
    4. Log success to SQLite
    5. Never crash — always return a response dict
    """

    # 1️⃣ CLASSIFY (Gemini — SAFE)
    cls = classify_query(user_query)

    task_type = cls.get("task_type", "FACTUAL_QA")
    confidence = cls.get("confidence", 0.0)

    # 2️⃣ SELECT MODEL
    model = select_model(task_type, confidence)

    # 3️⃣ GET ANSWER (OpenRouter)
    result = get_answer(user_query, model)

    # 4️⃣ HANDLE OPENROUTER FAILURE (NO CRASH)
    if result.get("answer") is None:
        return {
            "query": user_query,
            "task_type": task_type,
            "confidence": confidence,
            "model": model,
            "latency_ms": result.get("latency_ms", 0),
            "error": result.get("error", "Unknown error")
        }

    # 5️⃣ LOG SUCCESS TO SQLITE
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        INSERT INTO logs
        (query, task_type, confidence, model_used, tokens, latency_ms, answer)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_query,
            task_type,
            confidence,
            model,
            result.get("tokens", 0),
            result.get("latency_ms", 0),
            result["answer"]
        )
    )
    conn.commit()
    conn.close()

    # 6️⃣ RETURN FINAL RESPONSE
    return {
        "query": user_query,
        "task_type": task_type,
        "confidence": confidence,
        "model": model,
        **result
    }