"""
Two-Way Interactive Telegram Bot for Tamil Nadu Politics Intelligence.
Allows the user to query their AI Agent anytime from Telegram:
- e.g. "What did EPS say today?"
- "Show all MoUs in Hosur"
- "What happened in the Assembly about law & order?"
Run as a background listener or on-demand.
"""

import os
import sys
import json
import time
import requests
from dotenv import load_dotenv
from google import genai

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ALLOWED_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

def get_latest_context():
    try:
        with open("data/latest_report.json", "r", encoding="utf-8") as f:
            return json.dumps(json.load(f), ensure_ascii=False)
    except Exception:
        return "No recent briefing data available."

def answer_query(user_query):
    context = get_latest_context()
    client = genai.Client(api_key=GEMINI_KEY)

    system_prompt = """
You are the dedicated Tamil Nadu Politics, Assembly & Economic AI Assistant.
The user is asking you a question on Telegram about Tamil Nadu's latest political developments, assembly debates, or industrial investments.
Use the provided JSON context of today's ground reports to give an accurate, crisp, neutral, and helpful response.
Provide your response in both English and clear Tamil where helpful.
"""
    prompt = f"Today's Intelligence Context:\n{context}\n\nUser Question: {user_query}"

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[system_prompt, prompt]
        )
        return response.text
    except Exception as e:
        return f"Sorry, could not process your query: {e}"

def send_reply(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        requests.post(url, json=payload, timeout=15)
    except Exception as e:
        print(f"[!] Error sending reply: {e}")

def run_bot_listener(poll_seconds=60):
    print("[*] Telegram Interactive Bot Listener active. Waiting for your queries...")
    last_update_id = None

    start_time = time.time()
    while (poll_seconds is None) or (time.time() - start_time < poll_seconds):
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
            if last_update_id:
                url += f"?offset={last_update_id + 1}"
            
            resp = requests.get(url, timeout=10).json()
            for update in resp.get("result", []):
                last_update_id = update["update_id"]
                msg = update.get("message", {})
                chat_id = str(msg.get("chat", {}).get("id", ""))
                text = msg.get("text", "").strip()

                if text and text != "/start":
                    print(f"[*] Received question from Telegram: {text}")
                    reply = answer_query(text)
                    send_reply(chat_id, reply)
                    print("[✓] Replied to user successfully!")
        except Exception as e:
            print(f"[!] Polling error: {e}")
        time.sleep(2)

if __name__ == "__main__":
    run_bot_listener(poll_seconds=None)
