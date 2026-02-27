import sys, os, sqlite3
import google.generativeai as genai
from dotenv import load_dotenv

# ---------------- SETUP ----------------

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_KEY"))

DB_PATH = "data/router.db"
model = genai.GenerativeModel("gemini-2.0-flash")

# ---------------- REUSABLE FUNCTION (FOR COMPARE MODE) ----------------

def score_answer(query: str, answer: str) -> float:
    """
    Gemini-as-judge scoring function.
    Used by Compare Mode and Analytics.
    """
    prompt = f"""
Rate this answer from 1 to 10 for accuracy and helpfulness.

Query: {query}
Answer: {answer}

Return ONLY a number.
"""
    try:
        response = model.generate_content(prompt)
        return float(response.text.strip())
    except:
        return 5.0

# ---------------- BATCH SCORING (BENCHMARK MODE) ----------------

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Add column if not exists (safe)
try:
    cur.execute("ALTER TABLE logs ADD COLUMN quality_score REAL")
    conn.commit()
except:
    pass  # column already exists

rows = cur.execute(
    "SELECT id, query, answer FROM logs WHERE quality_score IS NULL"
).fetchall()

for row_id, query, answer in rows:
    score = score_answer(query, answer)

    cur.execute(
        "UPDATE logs SET quality_score=? WHERE id=?",
        (score, row_id)
    )
    conn.commit()

conn.close()
print("✅ Quality scoring complete.")