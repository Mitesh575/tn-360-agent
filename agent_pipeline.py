"""
Daily Orchestrator Pipeline for TN 5-Tier Intelligence Agent.
Orchestrates:
1. Scrape 5 Tiers (Official, Legacy Print, TV/Party, Digital Investigative, Direct High-Command X)
2. Scrape YouTube Prime-Time Political Debates & Livestreams
3. Gemini 5-Tier AI synthesis
4. Save 100% full dataset to data/
5. Generate & Send Tamil Audio Podcast to Telegram
6. Dispatch 100% full-detail multi-message briefing to Telegram
"""

import os
import sys
import json
from datetime import datetime

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

from scrapers.news_collector import fetch_5tier_sources
from scrapers.youtube_debates import collect_daily_youtube_debates
from analyzer.gemini_analyzer import analyze_tn_politics
from alerts.telegram_notifier import dispatch_full_report
from alerts.podcast_generator import generate_and_dispatch_audio

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def run_daily_agent(send_alert=True):
    print("=" * 60)
    print(f"[*] Starting TN 5-Tier 360° AI Agent Pipeline: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 1. Collect across all 5 tiers
    print("[1/5] Gathering news across all 5 tiers...")
    raw_items, tier_counts = fetch_5tier_sources()
    print(f"[OK] Retrieved {len(raw_items)} items across 5 tiers: {tier_counts}")

    # 2. Collect YouTube prime-time debates
    print("[2/5] Monitoring YouTube Tamil news debates & floor discussions...")
    debates = collect_daily_youtube_debates()
    print(f"[OK] Retrieved {len(debates)} prime-time debate programs & floor videos.")

    # 3. Analyze with Gemini
    print("[3/5] Analyzing and synthesizing with Gemini AI across 5 Tiers...")
    report = analyze_tn_politics(raw_items, youtube_debates=debates)
    report["raw_sources_count"] = len(raw_items) + len(debates)
    report["tier_distribution"] = tier_counts
    report["generated_at"] = datetime.now().isoformat()

    # 4. Persist report locally
    os.makedirs(DATA_DIR, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    report_path = os.path.join(DATA_DIR, f"report_{today}.json")
    latest_path = os.path.join(DATA_DIR, "latest_report.json")

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    with open(latest_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"[4/5] [OK] Saved complete 5-tier report to {report_path} and latest_report.json.")

    # 5. Audio Podcast & Telegram Dispatch
    if send_alert:
        print("[5/5] Generating Tamil Audio Podcast and dispatching to Telegram...")
        try:
            generate_and_dispatch_audio(report)
        except Exception as e:
            print(f"[!] Audio generation warning: {e}")

        status = dispatch_full_report(report)
        if status:
            print("[OK] Complete multi-message briefing dispatched to mobile successfully!")
        else:
            print("[!] Dispatch completed.")

    print("=" * 60)
    print("[OK] TN 5-Tier AI Agent Execution Finished!")
    print("=" * 60)
    return report

if __name__ == "__main__":
    run_daily_agent(send_alert=True)
