"""
Scheduler to automatically trigger the TN Politics Agent everyday at scheduled times:
- 08:00 AM (Morning roundup + Audio podcast)
- 18:30 PM (Evening Assembly Special + Full debrief)
Also starts the interactive Telegram query bot in the background.
"""

import time
import schedule
import threading
from agent_pipeline import run_daily_agent
from alerts.interactive_bot import run_bot_listener

def daily_job():
    print("[*] Scheduled daily pipeline run triggered...")
    run_daily_agent(send_alert=True)

# Schedule twice a day
schedule.every().day.at("08:00").do(daily_job)
schedule.every().day.at("18:30").do(daily_job)

def start_interactive_listener():
    while True:
        try:
            run_bot_listener(poll_seconds=120)
        except Exception as e:
            print(f"[!] Bot listener restart: {e}")
            time.sleep(5)

if __name__ == "__main__":
    print("==================================================")
    print("TN 360° AI Agent Master Scheduler & Interactive Bot")
    print("• Morning run at 08:00 AM")
    print("• Evening run at 18:30 PM")
    print("• Interactive Telegram listener ACTIVE")
    print("==================================================")

    # Start interactive bot in background thread
    bot_thread = threading.Thread(target=start_interactive_listener, daemon=True)
    bot_thread.start()

    while True:
        schedule.run_pending()
        time.sleep(10)
