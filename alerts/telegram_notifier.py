"""
Telegram Full-Fidelity Dispatcher for Tamil Nadu 5-Tier Intelligence.
Delivers 100% of all gathered details without truncation across all 5 tiers:
- Tier 1: Official Assembly Bulletins & Government Orders
- Tier 2: Legacy Print Media
- Tier 3: TV Broadcasts & Party Channels
- Tier 4: Independent Digital Media
- Tier 5: Direct High-Command Signed Statements on X (Stalin, EPS, Vijay, Annamalai, Seeman, etc.)
- Plus: MoUs, Investments, Prime-time Debates & Criticisms
"""

import os
import sys
import time
import requests
from dotenv import load_dotenv

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

load_dotenv()

def send_telegram_chunk(text):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not bot_token or not chat_id:
        return False, "Credentials missing"

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }

    try:
        res = requests.post(url, json=payload, timeout=15)
        data = res.json()
        if not data.get("ok") and "can't parse entities" in data.get('description', '').lower():
            payload["parse_mode"] = None
            res = requests.post(url, json=payload, timeout=15)
            data = res.json()
        return data.get("ok", False), data.get("description", "OK")
    except Exception as e:
        return False, str(e)

def split_into_safe_chunks(full_text, max_len=3600):
    if len(full_text) <= max_len:
        return [full_text]
    
    chunks = []
    current_chunk = ""
    lines = full_text.split("\n")

    for line in lines:
        if len(current_chunk) + len(line) + 1 > max_len:
            chunks.append(current_chunk.strip())
            current_chunk = line + "\n"
        else:
            current_chunk += line + "\n"
            
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
        
    return chunks

def build_full_mobile_sections(report):
    date = report.get("date", "")
    sections = []

    # 1. Header & Executive TLDR
    s1 = f"🏛️ <b>TAMIL NADU 5-TIER 360° INTELLIGENCE DOSSIER</b> ({date})\n"
    s1 += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    s1 += "⚡ <b>EXECUTIVE OVERVIEW / முக்கிய அம்சங்கள்</b>\n\n"
    tldr_en = report.get("executive_tldr_en", [])
    if isinstance(tldr_en, list):
        s1 += "<b>📌 English Summary:</b>\n"
        for b in tldr_en:
            s1 += f"• {b}\n"
    elif tldr_en:
        s1 += f"<b>📌 English Summary:</b>\n{tldr_en}\n"

    tldr_ta = report.get("executive_tldr_ta", [])
    if isinstance(tldr_ta, list):
        s1 += "\n<b>📌 தமிழ்ச் சுருக்கம்:</b>\n"
        for b in tldr_ta:
            s1 += f"• <i>{b}</i>\n"
    elif tldr_ta:
        s1 += f"\n<b>📌 தமிழ்ச் சுருக்கம்:</b>\n<i>{tldr_ta}</i>\n"
    sections.append(s1)

    # 2. Assembly Floor & Heated Moments
    heated = report.get("heated_assembly_moments", [])
    if heated:
        s2 = f"🔥 <b>ASSEMBLY FLOOR & HEATED DEBATES ({len(heated)} Issues)</b>\n"
        s2 += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        for i, item in enumerate(heated, 1):
            parties = ", ".join(item.get("parties_involved", []))
            speakers = ", ".join(item.get("key_speakers", [])) if item.get("key_speakers") else "Floor Legislators"
            
            s2 += f"\n<b>{i}. {item.get('issue_en', item.get('headline_en', ''))}</b>\n"
            s2 += f"👉 <i>{item.get('issue_ta', item.get('headline_ta', ''))}</i>\n"
            if parties:
                s2 += f"⚡ <b>Parties:</b> {parties} | <b>Intensity:</b> {item.get('intensity', 'Medium')}\n"
            s2 += f"🗣️ <b>Speakers:</b> {speakers}\n"
            if item.get("trigger_context"):
                s2 += f"📍 <b>Trigger:</b> {item.get('trigger_context')}\n"
            if item.get("opposition_stance_en"):
                s2 += f"🛑 <b>Opposition Grievance:</b> {item.get('opposition_stance_en')}\n"
            if item.get("government_reply_en"):
                s2 += f"🛡️ <b>Govt Defense:</b> {item.get('government_reply_en')}\n"
            if item.get("outcome_en"):
                s2 += f"⚖️ <b>Outcome:</b> {item.get('outcome_en')}\n"
            if item.get("details_ta"):
                s2 += f"<i>{item.get('details_ta')}</i>\n"
            s2 += "───────────────\n"
        sections.append(s2)

    # 3. Tier 5: Direct High-Command Press Statements (From X / Twitter)
    high_cmds = report.get("high_command_direct_statements", [])
    if high_cmds:
        s_hc = f"📢 <b>TIER 5: HIGH-COMMAND DIRECT STATEMENTS ({len(high_cmds)} Releases)</b>\n"
        s_hc += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        for i, stmt in enumerate(high_cmds, 1):
            leader = stmt.get("leader_name", "Leader")
            party = stmt.get("party", "")
            s_hc += f"\n<b>{i}. {leader} [{party}]</b>\n"
            s_hc += f"📰 <b>Statement:</b> {stmt.get('statement_headline_en', '')}\n"
            if stmt.get("statement_headline_ta"):
                s_hc += f"👉 <i>\"{stmt.get('statement_headline_ta')}\"</i>\n"
            if stmt.get("core_message_en"):
                s_hc += f"• <b>Points:</b> {stmt.get('core_message_en')}\n"
            if stmt.get("core_message_ta"):
                s_hc += f"• <i>{stmt.get('core_message_ta')}</i>\n"
            if stmt.get("target_party_or_issue"):
                s_hc += f"🎯 <b>Addressed To:</b> {stmt.get('target_party_or_issue')}\n"
            s_hc += "───────────────\n"
        sections.append(s_hc)

    # 4. Prime-Time TV Debates (YouTube / Live programs)
    debates = report.get("prime_time_debates", [])
    if debates:
        s_deb = f"📹 <b>PRIME-TIME TV DEBATES & CLASHES ({len(debates)} Shows)</b>\n"
        s_deb += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        for i, deb in enumerate(debates, 1):
            panelists = ", ".join(deb.get("panelists_or_parties", []))
            s_deb += f"\n<b>{i}. {deb.get('channel', 'Tamil TV')} • {deb.get('show_name', 'Debate')}</b>\n"
            s_deb += f"🎙️ <b>Topic:</b> {deb.get('topic_en')}\n"
            s_deb += f"👉 <i>{deb.get('topic_ta', '')}</i>\n"
            if panelists:
                s_deb += f"👥 <b>Panelists:</b> {panelists}\n"
            if deb.get("clash_summary_en"):
                s_deb += f"🔥 <b>Clashes & Conclusions:</b> {deb.get('clash_summary_en')}\n"
            if deb.get("clash_summary_ta"):
                s_deb += f"<i>{deb.get('clash_summary_ta')}</i>\n"
            if deb.get("video_url"):
                s_deb += f"🔗 <b>Watch:</b> {deb.get('video_url')}\n"
            s_deb += "───────────────\n"
        sections.append(s_deb)

    # 5. Political Criticisms & Rebuttals
    criticisms = report.get("political_criticisms_and_rebuttals", [])
    if criticisms:
        s3 = f"⚔️ <b>POLITICAL CRITICISMS & REBUTTALS ({len(criticisms)} Allegations)</b>\n"
        s3 += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        for i, crit in enumerate(criticisms, 1):
            accuser = crit.get("accuser_leader_or_party", "Leader")
            target = crit.get("targeted_leader_or_party", "Target")
            s3 += f"\n<b>{i}. {accuser} ➔ {target}</b>\n"
            s3 += f"⚠️ <b>Allegation:</b> {crit.get('core_criticism_en')}\n"
            if crit.get("core_criticism_ta"):
                s3 += f"<i>\"{crit.get('core_criticism_ta')}\"</i>\n"
            if crit.get("rebuttal_or_defense_en"):
                s3 += f"🛡️ <b>Counter / Rebuttal:</b> {crit.get('rebuttal_or_defense_en')}\n"
            if crit.get("rebuttal_or_defense_ta"):
                s3 += f"<i>\"{crit.get('rebuttal_or_defense_ta')}\"</i>\n"
            if crit.get("political_significance"):
                s3 += f"📊 <b>Significance:</b> {crit.get('political_significance')}\n"
            s3 += "───────────────\n"
        sections.append(s3)

    # 6. MoUs, Investments & Economy
    mous = report.get("mous_and_investments", [])
    if mous:
        s4 = f"💼 <b>INDUSTRIAL MoUs & INVESTMENTS ({len(mous)} Projects)</b>\n"
        s4 += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        for i, mou in enumerate(mous, 1):
            amt = mou.get("investment_amount_inr", "Undisclosed")
            loc = mou.get("location_district", "Tamil Nadu")
            jobs = mou.get("jobs_created", "TBD")
            sector = mou.get("sector", "Industrial")
            status = mou.get("status", "MoU Signed")

            s4 += f"\n<b>{i}. {mou.get('company_or_investor')}</b> ({sector})\n"
            s4 += f"💰 <b>Capital:</b> {amt} | <b>Status:</b> {status}\n"
            s4 += f"📍 <b>Location:</b> {loc} | 👷 <b>Jobs:</b> {jobs}\n"
            if mou.get("details_en"):
                s4 += f"• {mou.get('details_en')}\n"
            if mou.get("details_ta"):
                s4 += f"• <i>{mou.get('details_ta')}</i>\n"
            s4 += "───────────────\n"
        sections.append(s4)

    # 7. Statewide Politics & Bills
    s5 = "🗳️ <b>STATEWIDE POLITICAL PULSE & BILLS</b>\n"
    s5 += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    politics = report.get("statewide_politics", [])
    if politics:
        for i, pol in enumerate(politics, 1):
            s5 += f"\n<b>{i}. [{pol.get('party_or_leader', 'TN')}]</b> {pol.get('topic_en')}\n"
            if pol.get("topic_ta"):
                s5 += f"<i>{pol.get('topic_ta')}</i>\n"
            if pol.get("analysis_en"):
                s5 += f"• {pol.get('analysis_en')}\n"
            if pol.get("analysis_ta"):
                s5 += f"• <i>{pol.get('analysis_ta')}</i>\n"
            s5 += "───────────────\n"

    bills = report.get("bills_and_governance", [])
    if bills:
        s5 += "\n📜 <b>BILLS & GOVERNMENT ORDERS:</b>\n"
        for b in bills:
            s5 += f"\n• <b>{b.get('title_en')}</b>\n"
            if b.get("impact_en"):
                s5 += f"  {b.get('impact_en')}\n"

    sections.append(s5)
    return sections

def dispatch_full_report(report):
    raw_sections = build_full_mobile_sections(report)
    all_chunks = []
    for sec in raw_sections:
        all_chunks.extend(split_into_safe_chunks(sec, max_len=3800))

    total = len(all_chunks)
    print(f"[*] Delivering 100% complete 5-tier report across {total} messages to Telegram...")
    delivered = 0

    for idx, chunk in enumerate(all_chunks, 1):
        header = f"📱 <b>[Message {idx}/{total}]</b>\n"
        full_msg = header + chunk
        ok, err = send_telegram_chunk(full_msg)
        if ok:
            delivered += 1
            print(f"[✓] Delivered message {idx}/{total}")
        else:
            print(f"[!] Error on message {idx}: {err}")
        time.sleep(0.5)

    return delivered == total

if __name__ == "__main__":
    import json
    with open("data/latest_report.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    dispatch_full_report(data)
