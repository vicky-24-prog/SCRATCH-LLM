# router/selector.py

ROUTING_TABLE = {
    "CODING":        "openrouter/free",
    "MATH":          "openrouter/free",
    "FACTUAL_QA":    "openrouter/free",
    "SUMMARIZATION": "mistralai/mistral-small-3.1-24b-instruct:free",
    "CREATIVE":      "openrouter/free",
}

FALLBACK_MODEL = "meta-llama/llama-3.3-70b-instruct:free"

def select_model(task_type: str, confidence: float) -> str:
    if confidence < 0.6:
        return FALLBACK_MODEL
    return ROUTING_TABLE.get(task_type, FALLBACK_MODEL)