"""
Comprehensive 5-Tier Multi-Source Collector for Tamil Nadu 360 Intelligence.
Expanded Tier 5: Direct X / Twitter tracking of Key Party Figures:
- DMK: Stalin, Udhayanidhi Stalin, Kanimozhi, TRB Rajaa, PTR Palanivel Thiagarajan, Dayanidhi Maran, A. Raja, Saravanan Annadurai
- AIADMK: EPS, Jayakumar, C.V. Shanmugam, SP Velumani, RB Udhayakumar, Kovai Sathyan
- TVK: Vijay, Bussy Anand, Arunraj, TVK Official Handles & Spokespersons
- BJP: Annamalai, Vanathi Srinivasan, Nainar Nagendran, H. Raja, Amar Prasad Reddy, CTR Nirmal Kumar
- NTK: Seeman, Kaliyammal, Idumbavanam Karthik, Himler
- VCK: Thirumavalavan, D. Ravikumar, Aloor Shanavas, Vanni Arasu
- PMK: Dr. Ramadoss, Anbumani Ramadoss, GK Mani
- Congress: Selvaperunthagai, Karti Chidambaram, Manickam Tagore, Jothimani
"""

import sys
import os
import re
import urllib.parse
from datetime import datetime
import feedparser
from bs4 import BeautifulSoup

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

TIER_SOURCES = [
    # =========================================================================
    # TIER 1: OFFICIAL / ZERO SPIN
    # =========================================================================
    {
        "tier": 1,
        "name": "TN Legislative Assembly Secretariat & Floor Bulletins",
        "url": f"https://news.google.com/rss/search?q={urllib.parse.quote('site:assembly.tn.gov.in OR \"சட்டமன்ற நிகழ்வுக்குறிப்பு\" OR \"சட்டப்பேரவை அறிவிப்பு\"')}&hl=ta&gl=IN&ceid=IN:ta",
        "category": "official_assembly"
    },
    {
        "tier": 1,
        "name": "DIPR Tamil Nadu & CMO Official Releases",
        "url": f"https://news.google.com/rss/search?q={urllib.parse.quote('site:dipr.tn.gov.in OR \"செய்தி மக்கள் தொடர்புத்துறை\" OR \"முதலமைச்சர் செய்திக்குறிப்பு\"')}&hl=ta&gl=IN&ceid=IN:ta",
        "category": "official_governance"
    },
    {
        "tier": 1,
        "name": "Guidance Tamil Nadu & Industries Dept MoUs",
        "url": f"https://news.google.com/rss/search?q={urllib.parse.quote('\"Guidance Tamil Nadu\" OR \"SIPCOT\" OR \"தொழில் முதலீட்டு ஊக்குவிப்பு\" புரிந்துணர்வு ஒப்பந்தம்')}&hl=ta&gl=IN&ceid=IN:ta",
        "category": "official_investments"
    },
    {
        "tier": 1,
        "name": "Madras High Court Political & Legislative Verdicts",
        "url": f"https://news.google.com/rss/search?q={urllib.parse.quote('\"சென்னை உயர் நீதிமன்றம்\" OR \"Madras High Court\" (அரசியல் OR தேர்தல் OR இடைக்கால தடை OR மனு தள்ளுபடி)')}&hl=ta&gl=IN&ceid=IN:ta",
        "category": "official_legal"
    },

    # =========================================================================
    # TIER 2: LEGACY PRESS & PRINT
    # =========================================================================
    {
        "tier": 2,
        "name": "Dinamalar Tamil Daily (தினமலர்)",
        "url": f"https://news.google.com/rss/search?q={urllib.parse.quote('site:dinamalar.com (சட்டமன்றம் OR அரசியல் OR தேர்தல் OR குற்றச்சாட்டு)')}&hl=ta&gl=IN&ceid=IN:ta",
        "category": "legacy_print"
    },
    {
        "tier": 2,
        "name": "Dinamani (தினமணி)",
        "url": f"https://news.google.com/rss/search?q={urllib.parse.quote('site:dinamani.com/tamilnadu (அரசியல் OR பேரவை விவாதம் OR அறிக்கை)')}&hl=ta&gl=IN&ceid=IN:ta",
        "category": "legacy_print"
    },
    {
        "tier": 2,
        "name": "Dinakaran (தினகரன்)",
        "url": f"https://news.google.com/rss/search?q={urllib.parse.quote('site:dinakaran.com (அரசியல் OR சட்டப்பேரவை OR அமைச்சரவை)')}&hl=ta&gl=IN&ceid=IN:ta",
        "category": "legacy_print"
    },
    {
        "tier": 2,
        "name": "The Hindu Tamil & English TN Bureau",
        "url": "https://www.thehindu.com/news/national/tamil-nadu/feeder/default.rss",
        "category": "legacy_print"
    },
    {
        "tier": 2,
        "name": "Daily Thanthi (தினத்தந்தி)",
        "url": f"https://news.google.com/rss/search?q={urllib.parse.quote('site:dailythanthi.com (சட்டமன்றம் OR முதலமைச்சர் OR எடப்பாடி OR விஜய்)')}&hl=ta&gl=IN&ceid=IN:ta",
        "category": "legacy_print"
    },

    # =========================================================================
    # TIER 3: TV BROADCASTS & PARTY MOUTHPIECES
    # =========================================================================
    {
        "tier": 3,
        "name": "Puthiyathalaimurai TV (புதிய தலைமுறை)",
        "url": f"https://news.google.com/rss/search?q={urllib.parse.quote('site:puthiyathalaimurai.com OR \"புதியதலைமுறை\" (சட்டமன்ற விவாதம் OR அரசியல் மோதல்)')}&hl=ta&gl=IN&ceid=IN:ta",
        "category": "tv_broadcast"
    },
    {
        "tier": 3,
        "name": "Polimer News & Makkal Kural (பாலிமர் நியூஸ்)",
        "url": f"https://news.google.com/rss/search?q={urllib.parse.quote('site:polimernews.com (அரசியல் கள நிலவரம் OR விவாதம் OR சட்டப்பேரவை அமளி)')}&hl=ta&gl=IN&ceid=IN:ta",
        "category": "tv_broadcast"
    },
    {
        "tier": 3,
        "name": "Thanthi TV (தந்தி டிவி)",
        "url": f"https://news.google.com/rss/search?q={urllib.parse.quote('site:thanthitv.com (ஆயுத எழுத்து OR சட்டசபை நேரலை OR காரசார விவாதம்)')}&hl=ta&gl=IN&ceid=IN:ta",
        "category": "tv_broadcast"
    },
    {
        "tier": 3,
        "name": "Sun News (சன் நியூஸ் - Ruling Voice)",
        "url": f"https://news.google.com/rss/search?q={urllib.parse.quote('site:sunnews.in OR \"சன் நியூஸ்\" (அரசு நலத்திட்டம் OR முதலமைச்சர் உரை OR சட்டமன்றம்)')}&hl=ta&gl=IN&ceid=IN:ta",
        "category": "tv_party_voice"
    },
    {
        "tier": 3,
        "name": "Jaya Plus / News J (ஜெயா பிளஸ் / நியூஸ் ஜெ - Opposition Voice)",
        "url": f"https://news.google.com/rss/search?q={urllib.parse.quote('\"News J\" OR \"Jaya Plus\" OR \"நியூஸ் ஜெ\" (அதிமுக அறிக்கை OR அரசு மீது குற்றச்சாட்டு OR வெளிநடப்பு)')}&hl=ta&gl=IN&ceid=IN:ta",
        "category": "tv_party_voice"
    },

    # =========================================================================
    # TIER 4: INDEPENDENT DIGITAL JOURNALISM
    # =========================================================================
    {
        "tier": 4,
        "name": "Vikatan & Junior Vikatan (விகடன்)",
        "url": f"https://news.google.com/rss/search?q={urllib.parse.quote('site:vikatan.com (அரசியல் ஸ்பெஷல் OR ஜூனியர் விகடன் OR சட்டமன்ற ரகசியம் OR தவெக)')}&hl=ta&gl=IN&ceid=IN:ta",
        "category": "digital_investigative"
    },
    {
        "tier": 4,
        "name": "Oneindia Tamil (ஒன்இந்தியா தமிழ்)",
        "url": f"https://news.google.com/rss/search?q={urllib.parse.quote('site:tamil.oneindia.com (அரசியல் கள நிலவரம் OR கூட்டணி பேச்சுவார்த்தை OR மாவட்ட அரசியல்)')}&hl=ta&gl=IN&ceid=IN:ta",
        "category": "digital_pulse"
    },
    {
        "tier": 4,
        "name": "Behindwoods News & Political Air",
        "url": f"https://news.google.com/rss/search?q={urllib.parse.quote('\"Behindwoods Air\" OR \"பிஹைண்ட்வுட்ஸ்\" (தவெக விஜய் OR அரசியல் கருத்துக்கணிப்பு OR கள ஆய்வு)')}&hl=ta&gl=IN&ceid=IN:ta",
        "category": "digital_youth_pulse"
    },
    {
        "tier": 4,
        "name": "Red Pix 24x7 / Felix Gerald Ground Dispatches",
        "url": f"https://news.google.com/rss/search?q={urllib.parse.quote('\"Red Pix\" OR \"ரெட் பிக்ஸ்\" (அரசியல் பகிரங்க குற்றச்சாட்டு OR நிர்வாக முறைகேடு)')}&hl=ta&gl=IN&ceid=IN:ta",
        "category": "digital_investigative"
    },
    {
        "tier": 4,
        "name": "Aadhan Tamil (ஆதன் தமிழ்)",
        "url": f"https://news.google.com/rss/search?q={urllib.parse.quote('\"ஆதன் தமிழ்\" OR \"Aadhan Tamil\" (அரசியல் நேர்காணல் OR கட்சி செய்தி தொடர்பாளர் காரசாரம்)')}&hl=ta&gl=IN&ceid=IN:ta",
        "category": "digital_interviews"
    },

    # =========================================================================
    # TIER 5: EXPANDED PARTY KEY LEADERS & OFFICIAL SPOKESPERSONS ON X (TWITTER)
    # =========================================================================
    
    # 1. DMK KEY FIGURES & MINISTERS
    {
        "tier": 5,
        "name": "DMK Key Ministers on X (Udhayanidhi, TRB Rajaa, PTR, Kanimozhi, A.Raja)",
        "url": f"https://news.google.com/rss/search?q={urllib.parse.quote('(\"Udhaystalin\" OR \"KanimozhiDMK\" OR \"TRBRajaa\" OR \"ptrmadurai\" OR \"dmk_raja\" OR \"Dayanidhi_Maran\") site:x.com OR site:twitter.com')}&hl=ta&gl=IN&ceid=IN:ta",
        "category": "x_dmk_ministers"
    },
    {
        "tier": 5,
        "name": "MK Stalin & DMK HQ Press Releases (மு.க.ஸ்டாலின் & திமுக தலைமை)",
        "url": f"https://news.google.com/rss/search?q={urllib.parse.quote('(\"mkstalin\" OR \"arivalayam\" OR \"மு.க.ஸ்டாலின் அறிக்கை\") site:x.com OR site:twitter.com')}&hl=ta&gl=IN&ceid=IN:ta",
        "category": "x_dmk_highcmd"
    },

    # 2. AIADMK SENIOR LEADERS & SPOKESPERSONS
    {
        "tier": 5,
        "name": "AIADMK Seniors on X (EPS, D.Jayakumar, C.V.Shanmugam, SP Velumani, Kovai Sathyan)",
        "url": f"https://news.google.com/rss/search?q={urllib.parse.quote('(\"EPSTamilNadu\" OR \"offiofDJ\" OR \"SPVelumanicbe\" OR \"KovaiSathyan\" OR \"சி.வி.சண்முகம் அறிக்கை\") site:x.com OR site:twitter.com')}&hl=ta&gl=IN&ceid=IN:ta",
        "category": "x_aiadmk_seniors"
    },

    # 3. TVK LEADERSHIP & GENERAL SECRETARIES
    {
        "tier": 5,
        "name": "TVK Leadership & HQ on X (Vijay, Bussy Anand, Arunraj, IT Wing)",
        "url": f"https://news.google.com/rss/search?q={urllib.parse.quote('(\"tvkvijayhq\" OR \"tvkvijayoffl\" OR \"BussyAnand\" OR \"தவெக தலைமைச் செய்திக்குறிப்பு\" OR \"புஸ்ஸி ஆனந்த்\") site:x.com OR site:twitter.com')}&hl=ta&gl=IN&ceid=IN:ta",
        "category": "x_tvk_leadership"
    },

    # 4. BJP KEY LEADERS & SPOKESPERSONS
    {
        "tier": 5,
        "name": "BJP State Leaders on X (Annamalai, Vanathi, Nainar Nagendran, H. Raja, CTR Nirmal)",
        "url": f"https://news.google.com/rss/search?q={urllib.parse.quote('(\"annamalai_k\" OR \"VanathiBJP\" OR \"NainarBJP\" OR \"HRajaBJP\" OR \"CTR_Nirmalkumar\") site:x.com OR site:twitter.com')}&hl=ta&gl=IN&ceid=IN:ta",
        "category": "x_bjp_leadership"
    },

    # 5. NTK LEADERSHIP & SPOKESPERSONS
    {
        "tier": 5,
        "name": "NTK Key Figures on X (Seeman, Kaliyammal, Idumbavanam Karthik)",
        "url": f"https://news.google.com/rss/search?q={urllib.parse.quote('(\"SeemanOfficial\" OR \"Kaliyammal_NTK\" OR \"IdumbavanamK\" OR \"நாம் தமிழர் கட்சி தலைமை\") site:x.com OR site:twitter.com')}&hl=ta&gl=IN&ceid=IN:ta",
        "category": "x_ntk_leadership"
    },

    # 6. VCK KEY LEADERS & MPs/MLAs
    {
        "tier": 5,
        "name": "VCK Key Leaders on X (Thirumavalavan, Ravikumar MP, Aloor Shanavas, Vanni Arasu)",
        "url": f"https://news.google.com/rss/search?q={urllib.parse.quote('(\"thirumaofficial\" OR \"WriterRavikumar\" OR \"Aloor_Shanavas\" OR \"VanniArasu_VCK\") site:x.com OR site:twitter.com')}&hl=ta&gl=IN&ceid=IN:ta",
        "category": "x_vck_leadership"
    },

    # 7. PMK & CONGRESS LEADERSHIP
    {
        "tier": 5,
        "name": "PMK & Congress Leaders on X (Anbumani, Ramadoss, Selvaperunthagai, Karti Chidambaram)",
        "url": f"https://news.google.com/rss/search?q={urllib.parse.quote('(\"draramadoss\" OR \"dranbumaniramadoss\" OR \"SPK_TNCC\" OR \"KartiPC\" OR \"manickamtagore\") site:x.com OR site:twitter.com')}&hl=ta&gl=IN&ceid=IN:ta",
        "category": "x_pmk_congress"
    }
]

def clean_html(raw_html):
    if not raw_html:
        return ""
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text().strip()

def fetch_5tier_sources():
    collected_items = []
    seen_titles = set()
    tier_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

    for src in TIER_SOURCES:
        try:
            feed = feedparser.parse(src["url"])
            for entry in feed.entries[:10]:
                title = clean_html(entry.get("title", ""))
                norm_title = re.sub(r'[^a-zA-Z0-9\u0B80-\u0BFF]', '', title).lower()
                if not norm_title or norm_title in seen_titles:
                    continue
                seen_titles.add(norm_title)

                summary = clean_html(entry.get("summary", entry.get("description", "")))
                link = entry.get("link", "")
                pub_date = entry.get("published", datetime.now().isoformat())

                item = {
                    "id": f"tier{src['tier']}_{len(collected_items) + 1}",
                    "tier": src["tier"],
                    "source_name": src["name"],
                    "category": src["category"],
                    "title": title,
                    "summary": summary,
                    "url": link,
                    "published_at": pub_date,
                    "fetched_at": datetime.now().isoformat()
                }
                collected_items.append(item)
                tier_counts[src["tier"]] += 1
        except Exception as e:
            print(f"[!] Error reading {src['name']}: {e}")

    return collected_items, tier_counts

if __name__ == "__main__":
    items, counts = fetch_5tier_sources()
    print(f"[OK] Full Multi-Party Figure X Data Ingestion Complete! Total: {len(items)}")
    for t, c in counts.items():
        print(f"  • Tier {t} Items: {c}")
