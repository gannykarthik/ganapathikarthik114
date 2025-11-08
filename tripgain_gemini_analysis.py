# tripgain_gemini_analysis.py
# -------------------------------------------------------------
# TripGain Section C – Gemini Integration and Intelligent Summarization
# (Fixed version — works even when websites block bots)
# -------------------------------------------------------------

import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

# ------------------ CONFIGURATION ------------------
API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_API_KEY_HERE")

MODEL_NAME = "gemini-2.0-flash"
TARGET_URL = "https://en.wikipedia.org/wiki/Artificial_intelligence"
# ----------------------------------------------------


# 🔹 STEP 1 — Fetch and clean webpage content
def clean_html(url: str) -> str:
    """
    Fetches webpage content with browser headers and removes unwanted tags.
    Returns cleaned plain text.
    """
    print(f"🔍 Fetching webpage: {url}")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/118.0.5993.90 Safari/537.36"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        html = response.text
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to fetch webpage: {e}")

    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator=" ", strip=True)
    print("✅ Webpage fetched and cleaned successfully.")
    return text


# 🔹 STEP 2 — Initialize Gemini and send prompt
def summarize_with_gemini(content: str) -> str:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(MODEL_NAME)

    prompt = (
        "Analyze the following webpage content and summarize it in 3–5 concise bullet points "
        "focusing on major technology, business, or ethical trends related to AI. "
        "Then provide ONE short analytical insight line interpreting the overall theme.\n\n"
        "Output strictly in this format:\n"
        "Summary:\n• <point 1>\n• <point 2>\n• <point 3>\n• <point 4>\n• <point 5>\n\n"
        "Insight:\n<single-line insight>\n\n"
        f"Webpage content (start):\n{content[:10000]}"
    )

    print("🧠 Sending prompt to Gemini for analysis ...")
    response = model.generate_content(prompt)
    return response.text.strip()


# 🔹 STEP 3 — Save summary output
def save_summary(result_text: str):
    filename = "summary_output.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(result_text)
    print(f"✅ Saved summary and insight to {filename}")


# 🔹 STEP 4 — Main Execution Flow
if __name__ == "__main__":
    try:
        cleaned_text = clean_html(TARGET_URL)
        summary_result = summarize_with_gemini(cleaned_text)

        print("\n------------------- GEMINI OUTPUT -------------------\n")
        print(summary_result)
        print("\n----------------------------------------------------\n")

        save_summary(summary_result)

    except Exception as e:
        print(f"❌ Error: {e}")
