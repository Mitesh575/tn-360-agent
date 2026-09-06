"""
Audio Podcast Generator for Tamil Nadu 360 Intelligence.
Synthesizes a 90-120 second radio-bulletin audio dispatch in Tamil and English,
and sends it directly to Telegram as a playable voice note/audio file.
"""

import os
import sys
import asyncio
from gtts import gTTS
import requests

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

def generate_podcast_script(report):
    date = report.get("date", "Today")
    tldr_en = report.get("executive_tldr_en", [])
    tldr_ta = report.get("executive_tldr_ta", [])
    heated = report.get("heated_assembly_moments", [])
    mous = report.get("mous_and_investments", [])

    # Natural Tamil broadcast script
    ta_script = f"வணக்கம். இது இன்றைய தமிழ்நாடு 360 அரசியல் மற்றும் சட்டமன்ற சிறப்புச் செய்தி அறிக்கை. நாள்: {date}.\n"
    if isinstance(tldr_ta, list) and tldr_ta:
        ta_script += "இன்றைய முக்கிய அம்சங்கள்: " + " ".join(tldr_ta) + ".\n"
    if heated:
        first_heated = heated[0]
        ta_script += f"சட்டமன்றத்தில் இன்று காரசார விவாதம்: {first_heated.get('issue_ta', '')}. {first_heated.get('details_ta', '')}.\n"
    if mous:
        first_mou = mous[0]
        ta_script += f"தொழில் முதலீடுகள்: {first_mou.get('company_or_investor', '')} நிறுவனம் {first_mou.get('investment_amount_inr', '')} முதலீட்டில் {first_mou.get('location_district', '')} பகுதியில் புதிய திட்டத்தை தொடங்கியுள்ளது.\n"
    ta_script += "முழு விவரங்களை தெரிந்துகொள்ள உங்களது இணைய டாஷ்போர்டை பாருங்கள். நன்றி."

    return ta_script

def create_audio_file(text, output_path="data/daily_briefing.mp3"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    tts = gTTS(text=text, lang='ta', slow=False)
    tts.save(output_path)
    return output_path

def send_telegram_audio(audio_path, caption="🎙️ <b>TN 360° Daily Tamil Audio Briefing</b>"):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not bot_token or not chat_id or not os.path.exists(audio_path):
        return False, "Missing credentials or audio file"

    url = f"https://api.telegram.org/bot{bot_token}/sendVoice"
    try:
        with open(audio_path, "rb") as f:
            files = {"voice": f}
            data = {"chat_id": chat_id, "caption": caption, "parse_mode": "HTML"}
            res = requests.post(url, data=data, files=files, timeout=30)
            json_res = res.json()
            if json_res.get("ok"):
                print("[✓] Audio voice note delivered to Telegram!")
                return True, "Delivered"
            else:
                # Fallback to sendAudio
                url_audio = f"https://api.telegram.org/bot{bot_token}/sendAudio"
                f.seek(0)
                res2 = requests.post(url_audio, data=data, files={"audio": f}, timeout=30)
                return res2.json().get("ok", False), str(res2.json())
    except Exception as e:
        print(f"[!] Error sending audio: {e}")
        return False, str(e)

def generate_and_dispatch_audio(report):
    script = generate_podcast_script(report)
    audio_path = create_audio_file(script)
    ok, err = send_telegram_audio(audio_path, f"🎙️ <b>தமிழ்நாடு 360° ஆடியோ செய்தி அறிக்கை ({report.get('date', 'Today')})</b>\n<i>Play to listen to today's summary in Tamil</i>")
    return ok

if __name__ == "__main__":
    import json
    with open("data/latest_report.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    generate_and_dispatch_audio(data)
