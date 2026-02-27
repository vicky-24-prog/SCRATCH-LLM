# router/caller.py
import requests, os, time
from dotenv import load_dotenv

load_dotenv()

def get_answer(query: str, model: str) -> dict:
    start = time.time()

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.getenv('OPENROUTER_KEY')}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": query}],
                "max_tokens": 800,
            },
            timeout=30
        )
    except Exception as e:
        return {
            "answer": None,
            "error": str(e),
            "latency_ms": round((time.time() - start) * 1000),
        }

    latency_ms = round((time.time() - start) * 1000)

    if response.status_code != 200:
        return {
            "answer": None,
            "error": response.text,
            "latency_ms": latency_ms,
        }

    data = response.json()

    return {
        "answer": data["choices"][0]["message"]["content"],
        "model": data.get("model", model),
        "tokens": data["usage"]["total_tokens"],
        "latency_ms": latency_ms,
    }