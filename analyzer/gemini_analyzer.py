"""
Gemini 5-Tier 360° Intelligence Analyzer for Tamil Nadu:
Ingests 5 Tiers:
- Tier 1: Official Bulletins, DIPR, Guidance TN & High Court
- Tier 2: Legacy Print (Dinamalar, Dinamani, Dinakaran, The Hindu Tamil, Daily Thanthi)
- Tier 3: TV Broadcasts & Party Mouthpieces (Puthiyathalaimurai, Polimer, Thanthi, Sun News, News J)
- Tier 4: Independent Digital Journalism (Vikatan, Oneindia, Behindwoods, Red Pix, Aadhan)
- Tier 5: Direct High-Command Press Statements on X (Stalin, EPS, Vijay TVK, Annamalai, Seeman, Thiruma, Ramadoss)
Plus: YouTube Prime-Time Debate Transcripts
"""

import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv
from google import genai

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

load_dotenv()

SYSTEM_PROMPT = """
You are the Chief Political & Legislative Intelligence Analyst for Tamil Nadu.
You are processing a massive 5-Tier multi-source dataset spanning:
- Tier 1: Official Assembly Records, DIPR Releases, High Court Orders, Guidance TN MoUs
- Tier 2: Legacy Print Press (Dinamalar, Dinamani, Dinakaran, The Hindu, Daily Thanthi)
- Tier 3: TV Broadcasts & Party Outlets (Puthiyathalaimurai, Polimer, Thanthi TV, Sun News, News J)
- Tier 4: Digital Investigative Media (Vikatan, Oneindia, Behindwoods Air, Red Pix, Aadhan)
- Tier 5: Direct High-Command Press Statements from X/Twitter (Stalin, EPS, Vijay TVK, Annamalai, Seeman, Thirumavalavan, Ramadoss)
- YouTube Prime-Time Political Debate Transcripts

YOUR MANDATE:
Produce an exhaustive, highly structured, neutral, and 100% verified daily intelligence dossier.

CRITICAL RULES:
1. Cross-reference claims across tiers (e.g. if Tier 5 makes an accusation, check if Tier 1 or 2 provides government data/reply).
2. Maintain strict fact vs claim separation.
3. Deliver bilingual parity (both English and natural, impeccable Tamil - தமிழ்).

Output strictly valid JSON conforming to this schema:
{
  "date": "YYYY-MM-DD",
  "executive_tldr_en": [
    "Comprehensive takeaway 1",
    "Comprehensive takeaway 2",
    "Comprehensive takeaway 3",
    "Comprehensive takeaway 4"
  ],
  "executive_tldr_ta": [
    "முக்கிய அம்சம் 1",
    "முக்கிய அம்சம் 2",
    "முக்கிய அம்சம் 3",
    "முக்கிய அம்சம் 4"
  ],
  
  "heated_assembly_moments": [
    {
      "issue_en": "Specific topic or debate",
      "issue_ta": "விவாதத்தின் தலைப்பு",
      "trigger_context": "What started the confrontation",
      "parties_involved": ["DMK", "AIADMK"],
      "key_speakers": ["Leader Name 1", "Minister Name 2"],
      "opposition_stance_en": "What the opposition claimed or demanded",
      "government_reply_en": "How the government/minister defended or replied",
      "outcome_en": "Walkout / Suspended / Speaker intervened / Passed",
      "details_ta": "சட்டமன்ற காரசார நிகழ்வு பற்றிய விரிவான தமிழாக்கம்.",
      "intensity": "High",
      "media": {
        "media_type": "youtube_video | poster | photo",
        "url": "Video or article URL",
        "thumbnail_url": "Image URL or YouTube thumbnail",
        "caption": "Brief label describing the media"
      }
    }
  ],

  "high_command_direct_statements": [
    {
      "leader_name": "M.K. Stalin / Edappadi Palaniswami / Vijay (TVK) / K. Annamalai / Seeman / Thirumavalavan / Ramadoss",
      "party": "DMK / AIADMK / TVK / BJP / NTK / VCK / PMK",
      "statement_headline_en": "Official statement summary",
      "statement_headline_ta": "அறிக்கை தலைப்பு தமிழில்",
      "core_message_en": "Direct points made in their signed letterhead / X post",
      "core_message_ta": "தலைமையின் அதிகாரப்பூர்வ அறிக்கை விவரம் தமிழில்",
      "target_party_or_issue": "Target party or public grievance",
      "source_tier": "Tier 5 (Direct Official Handle)",
      "media": {
        "media_type": "poster | photo",
        "image_url": "Image or poster URL from source data or party badge",
        "caption": "Party official letterhead / statement poster"
      }
    }
  ],

  "political_criticisms_and_rebuttals": [
    {
      "accuser_leader_or_party": "Name of Leader/Party making criticism",
      "targeted_leader_or_party": "Name of Leader/Party criticized",
      "core_criticism_en": "Specific allegation",
      "core_criticism_ta": "முன்வைக்கப்பட்ட குற்றச்சாட்டு அல்லது கண்டனம் தமிழில்",
      "rebuttal_or_defense_en": "Counter-reply given by the targeted party",
      "rebuttal_or_defense_ta": "எதிர்தரப்பு அல்லது அமைச்சரின் பதிலடி / விளக்கம்",
      "political_significance": "Why this matters",
      "media": {
        "media_type": "poster | photo",
        "image_url": "Image URL",
        "caption": "Photo of critic or target"
      }
    }
  ],

  "prime_time_debates": [
    {
      "show_name": "Nerkonda Paarvai / Ayutha Ezhuthu / Polimer Debate / Assembly Livestream",
      "channel": "Puthiyathalaimurai / Thanthi TV / Polimer / Media",
      "topic_en": "Debate Title in English",
      "topic_ta": "விவாத தலைப்பு தமிழில்",
      "panelists_or_parties": ["Party Reps and Analysts"],
      "clash_summary_en": "Key panel clashes and arguments",
      "clash_summary_ta": "விவாதத்தில் காரசாரமான வாதங்கள் மற்றும் முக்கிய கருத்துக்கள் தமிழில்",
      "video_url": "https://www.youtube.com/watch?v=...",
      "thumbnail_url": "https://img.youtube.com/vi/.../hqdefault.jpg"
    }
  ],

  "mous_and_investments": [
    {
      "company_or_investor": "Company / Group Name",
      "sector": "Sector name",
      "investment_amount_inr": "₹X,000 Crore",
      "jobs_created": "Projected employment",
      "location_district": "District / SIPCOT Park",
      "status": "MoU Signed / Plant Inauguration / Expansion",
      "details_en": "Brief description of the facility",
      "details_ta": "முதலீட்டு விவரம் தமிழில்",
      "media": {
        "media_type": "photo",
        "image_url": "Image URL if available",
        "caption": "Facility or MoU signing photo"
      }
    }
  ],

  "statewide_politics": [
    {
      "party_or_leader": "Party Name",
      "topic_en": "Headline of political action",
      "topic_ta": "அரசியல் நிகழ்வு தலைப்பு",
      "analysis_en": "Factual context and alliance impact",
      "analysis_ta": "அரசியல் நகர்வு விளக்கம்",
      "media": {
        "media_type": "poster | photo",
        "image_url": "Image URL",
        "caption": "Photo / Poster"
      }
    }
  ],

  "bills_and_governance": [
    {
      "title_en": "Bill or Government Order Title",
      "title_ta": "மசோதா அல்லது அரசாணை தலைப்பு",
      "impact_en": "Impact description",
      "impact_ta": "தாக்கம் தமிழில்"
    }
  ]
}
"""

def analyze_tn_politics(raw_items, youtube_debates=[], api_key=None):
    key = api_key or os.getenv("GEMINI_API_KEY")
    if not key:
        print("[!] Warning: GEMINI_API_KEY is not configured.")
        return {}

    # Candidate models to try in order of capability & speed
    candidate_models = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]

    # Select representative batch across all 5 tiers
    tier_samples = []
    for t in [1, 2, 3, 4, 5]:
        tier_items = [i for i in raw_items if i.get("tier") == t][:12]
        tier_samples.extend(tier_items)

    items_payload = {
        "5_tier_multi_source_articles": tier_samples,
        "youtube_tv_debates_and_livestreams": youtube_debates[:8]
    }
    items_text = json.dumps(items_payload, ensure_ascii=False, indent=2)
    prompt = f"Here is today's 5-Tier intelligence ground data from Tamil Nadu:\n\n{items_text}\n\nSynthesize the complete, authoritative daily intelligence dossier across all 5 tiers adhering strictly to the JSON schema."

    client = genai.Client(api_key=key)

    for model_name in candidate_models:
        for attempt in range(1, 4):
            try:
                print(f"[*] Calling Gemini ({model_name}) - Attempt {attempt}/3...")
                response = client.models.generate_content(
                    model=model_name,
                    contents=[SYSTEM_PROMPT, prompt],
                    config={
                        "response_mime_type": "application/json"
                    }
                )
                if response and response.text:
                    data = json.loads(response.text)
                    if data.get("executive_tldr_en") or data.get("heated_assembly_moments"):
                        print(f"[OK] Successfully synthesized dossier via {model_name}.")
                        return data
            except Exception as e:
                print(f"[!] Warning on {model_name} (Attempt {attempt}): {e}")
                time.sleep(3 * attempt)

    print("[!] Error: All Gemini candidate models failed to generate content.")
    return {}

