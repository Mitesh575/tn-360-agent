"""
Streamlit 5-Tier 360° Web Intelligence Dashboard for Tamil Nadu Politics, Assembly & Economy.
Includes:
- Tier Distribution Overview
- 7 Dedicated Intelligence Tabs:
  1. Assembly Floor & Heated Debates
  2. Tier 5: Direct High-Command Press Statements (From X / Twitter)
  3. Prime-Time TV Debates
  4. Criticisms & Rebuttals
  5. MoUs & Investments
  6. District Industrial Map
  7. Statewide Politics & Bills
Run with: streamlit run web/app.py
"""

import streamlit as st
import json
import os
import sys
import glob
import pandas as pd
import plotly.express as px
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

ASSETS_DIR = os.path.join(PROJECT_ROOT, "web", "assets")

def resolve_card_image(party, media):
    # 1. Direct valid image from media
    if isinstance(media, dict) and media.get("image_url"):
        url = media["image_url"]
        if "wikimedia.org" not in url:
            return url
    # 2. Local party badge asset
    party_clean = (party or "").upper()
    for k in ["TVK", "DMK", "AIADMK", "BJP", "NTK", "VCK", "PMK"]:
        if k in party_clean:
            local_path = os.path.join(ASSETS_DIR, f"{k.lower()}_badge.png")
            if os.path.exists(local_path):
                return local_path
    govt_path = os.path.join(ASSETS_DIR, "govt_badge.png")
    return govt_path if os.path.exists(govt_path) else None

st.set_page_config(
    page_title="TN 5-Tier Intelligence Radar",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.1rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 2px;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 22px;
    }
    .tldr-card {
        background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%);
        border-left: 5px solid #4F46E5;
        padding: 16px 20px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    .high-cmd-card {
        background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
        border-left: 5px solid #16A34A;
        padding: 16px 20px;
        border-radius: 8px;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .debate-card {
        background: linear-gradient(135deg, #FFF7ED 0%, #FFEDD5 100%);
        border-left: 5px solid #EA580C;
        padding: 16px 20px;
        border-radius: 8px;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .criticism-card {
        background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
        border-left: 5px solid #D97706;
        padding: 16px 20px;
        border-radius: 8px;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .heated-card {
        background: linear-gradient(135deg, #FEF2F2 0%, #FFF1F2 100%);
        border-left: 5px solid #EF4444;
        padding: 16px 20px;
        border-radius: 8px;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .mou-card {
        background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
        border-left: 5px solid #059669;
        padding: 16px 20px;
        border-radius: 8px;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .political-card {
        background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
        border-left: 5px solid #2563EB;
        padding: 16px 20px;
        border-radius: 8px;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .badge-high {
        background-color: #EF4444;
        color: white;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .badge-medium {
        background-color: #F59E0B;
        color: white;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .badge-channel {
        background-color: #C2410C;
        color: white;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .badge-cmd {
        background-color: #15803D;
        color: white;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: bold;
    }
    .badge-money {
        background-color: #047857;
        color: white;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .badge-party {
        background-color: #1E293B;
        color: white;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.75rem;
        margin-right: 4px;
    }
</style>
""", unsafe_allow_html=True)

DATA_DIR = os.path.join(PROJECT_ROOT, "data")

def load_reports():
    files = glob.glob(os.path.join(DATA_DIR, "report_*.json"))
    reports = {}
    for fpath in sorted(files, reverse=True):
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
                reports[data.get("date", os.path.basename(fpath))] = data
        except Exception:
            pass
    return reports

def load_latest():
    latest_file = os.path.join(DATA_DIR, "latest_report.json")
    if os.path.exists(latest_file):
        with open(latest_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# Sidebar
st.sidebar.title("🏛️ TN 5-Tier Radar")
st.sidebar.markdown("**5-Tier Ground Intelligence System**")

all_reports = load_reports()
selected_date = None
if all_reports:
    selected_date = st.sidebar.selectbox("📅 Select Date", list(all_reports.keys()))
    report_data = all_reports[selected_date]
else:
    report_data = load_latest()

lang_choice = st.sidebar.radio("🌐 Language / மொழி", ["Bilingual (English + தமிழ்)", "English Only", "தமிழ் மட்டும்"])

st.sidebar.divider()
st.sidebar.subheader("🎙️ Daily Tamil Audio Podcast")
if os.path.exists(os.path.join(DATA_DIR, "daily_briefing.mp3")):
    st.sidebar.audio(os.path.join(DATA_DIR, "daily_briefing.mp3"), format="audio/mp3")

st.sidebar.divider()
st.sidebar.subheader("⚡ Agent Trigger")
if st.sidebar.button("🔄 Trigger Fresh 5-Tier Scan"):
    with st.spinner("Scraping 5 Tiers + YouTube Debates + Gemini 2.5 synthesis..."):
        from agent_pipeline import run_daily_agent
        report_data = run_daily_agent(send_alert=True)
        st.sidebar.success("Updated & dispatched to Telegram!")
        st.rerun()

st.sidebar.markdown("""
---
**5-Tier Spectrum:**
- **Tier 1**: Official Assembly & DIPR Bulletins
- **Tier 2**: Legacy Print (Dinamalar, Dinamani, The Hindu)
- **Tier 3**: TV Broadcasts & Party Mouthpieces
- **Tier 4**: Independent Digital (Vikatan, Red Pix, Oneindia)
- **Tier 5**: Direct High-Command Handles (X / Twitter)
""")

# Header
st.markdown('<div class="main-header">🏛️ Tamil Nadu 5-Tier 360° Daily Intelligence Dossier</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-header">Zero-Blindspot Legislative, Political High-Command & Economic Intelligence — <b>{report_data.get("date", "Today")}</b></div>', unsafe_allow_html=True)

# 60-Second Executive TLDR
st.markdown("""
<div class="tldr-card">
    <h3 style="margin:0 0 8px 0; color:#312E81;">⚡ 60-Second Executive Digest / முக்கிய அம்சங்கள்</h3>
""", unsafe_allow_html=True)
tldr_col1, tldr_col2 = st.columns(2)
if lang_choice in ["Bilingual (English + தமிழ்)", "English Only"]:
    with tldr_col1:
        tldr_en = report_data.get('executive_tldr_en', report_data.get('summary_english', ''))
        if isinstance(tldr_en, list):
            for b in tldr_en:
                st.markdown(f"• {b}")
        else:
            st.markdown(tldr_en)

if lang_choice in ["Bilingual (English + தமிழ்)", "தமிழ் மட்டும்"]:
    with (tldr_col2 if lang_choice == "Bilingual (English + தமிழ்)" else tldr_col1):
        tldr_ta = report_data.get('executive_tldr_ta', report_data.get('summary_tamil', ''))
        if isinstance(tldr_ta, list):
            for b in tldr_ta:
                st.markdown(f"• *{b}*")
        else:
            st.markdown(f"*{tldr_ta}*")
st.markdown("</div>", unsafe_allow_html=True)

# Tabs
tab_assembly, tab_highcmd, tab_debates, tab_criticisms, tab_investments, tab_map, tab_politics = st.tabs([
    "🔥 Assembly Floor",
    "📢 Tier 5: High-Command X Statements",
    "📹 Prime-Time TV Debates",
    "⚔️ Criticisms & Rebuttals",
    "💼 MoUs & Investments",
    "🗺️ District Map",
    "🗳️ Statewide Politics & Bills"
])

# TAB 1: ASSEMBLY
with tab_assembly:
    st.subheader("🔥 Assembly Heated Debates, Walkouts & Confrontations")
    heated_list = report_data.get("heated_assembly_moments", [])
    if not heated_list:
        st.info("No major heated confrontations or walkouts recorded for this session.")
    else:
        for item in heated_list:
            intensity = item.get("intensity", item.get("intensity_level", "Medium"))
            badge_cls = "badge-high" if str(intensity).lower() == "high" else "badge-medium"
            parties = "".join([f'<span class="badge-party">{p}</span>' for p in item.get("parties_involved", [])])
            speakers = ", ".join(item.get("key_speakers", [])) if item.get("key_speakers") else "Floor Legislators"

            st.markdown(f"""
            <div class="heated-card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <span class="{badge_cls}">Intensity: {intensity}</span>
                    <div>{parties}</div>
                </div>
                <h4 style="margin:0 0 4px 0; color:#991B1B;">⚡ {item.get('issue_en', item.get('headline_en', ''))}</h4>
                <h5 style="margin:0 0 10px 0; color:#B91C1C; font-weight:normal;"><i>{item.get('issue_ta', item.get('headline_ta', ''))}</i></h5>
                <p style="margin-bottom:4px;"><b>Key Leaders/Speakers:</b> {speakers}</p>
                {"<p style='margin-bottom:4px; color:#1F2937;'><b>Trigger:</b> " + item.get('trigger_context') + "</p>" if item.get('trigger_context') else ""}
                {"<p style='margin-bottom:4px; color:#991B1B;'><b>Opposition Demand:</b> " + item.get('opposition_stance_en') + "</p>" if item.get('opposition_stance_en') else ""}
                {"<p style='margin-bottom:4px; color:#065F46;'><b>Government Response:</b> " + item.get('government_reply_en') + "</p>" if item.get('government_reply_en') else ""}
                {"<p style='margin-bottom:4px; color:#4B5563;'><b>Outcome:</b> " + item.get('outcome_en') + "</p>" if item.get('outcome_en') else ""}
                <p style="margin-bottom:0px; color:#374151; font-style:italic; margin-top:8px;">{item.get('details_ta', '')}</p>
            </div>
            """, unsafe_allow_html=True)

# TAB 2: TIER 5 HIGH-COMMAND DIRECT STATEMENTS (NEW!)
with tab_highcmd:
    st.subheader("📢 Tier 5: Direct Party Chiefs & High-Command Statements (From X / Twitter)")
    high_cmds = report_data.get("high_command_direct_statements", [])
    if not high_cmds:
        st.info("No signed high-command statements logged for this run.")
    else:
        for stmt in high_cmds:
            leader = stmt.get("leader_name", "Party Leader")
            party = stmt.get("party", "")
            target = stmt.get("target_party_or_issue", "General Public")
            media = stmt.get("media", {})
            card_img = resolve_card_image(party, media)

            c1, c2 = st.columns([1, 4]) if card_img else (None, None)
            if card_img:
                with c1:
                    st.image(card_img, caption=media.get("caption", leader), use_container_width=True)
                with c2:
                    st.markdown(f"""
                    <div class="high-cmd-card">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                            <span class="badge-cmd">🏛️ {leader} [{party}]</span>
                            <span style="font-size:0.8rem; color:#15803D; font-weight:600;">Target / Focus: {target}</span>
                        </div>
                        <h4 style="margin:0 0 4px 0; color:#166534;">📜 {stmt.get('statement_headline_en', '')}</h4>
                        <h5 style="margin:0 0 10px 0; color:#15803D; font-weight:normal;"><i>{stmt.get('statement_headline_ta', '')}</i></h5>
                        <p style="margin-bottom:6px; color:#1F2937;"><b>Official Statement Points:</b> {stmt.get('core_message_en', '')}</p>
                        <p style="margin-bottom:0; color:#14532D; font-style:italic;">{stmt.get('core_message_ta', '')}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="high-cmd-card">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                        <span class="badge-cmd">🏛️ {leader} [{party}]</span>
                        <span style="font-size:0.8rem; color:#15803D; font-weight:600;">Target / Focus: {target}</span>
                    </div>
                    <h4 style="margin:0 0 4px 0; color:#166534;">📜 {stmt.get('statement_headline_en', '')}</h4>
                    <h5 style="margin:0 0 10px 0; color:#15803D; font-weight:normal;"><i>{stmt.get('statement_headline_ta', '')}</i></h5>
                    <p style="margin-bottom:6px; color:#1F2937;"><b>Official Statement Points:</b> {stmt.get('core_message_en', '')}</p>
                    <p style="margin-bottom:0; color:#14532D; font-style:italic;">{stmt.get('core_message_ta', '')}</p>
                </div>
                """, unsafe_allow_html=True)

# TAB 3: PRIME-TIME YOUTUBE DEBATES
with tab_debates:
    st.subheader("📹 Prime-Time Tamil TV News Debates & Livestream Clashes")
    debates_list = report_data.get("prime_time_debates", [])
    if not debates_list:
        st.info("No prime-time TV debates logged for this date.")
    else:
        for deb in debates_list:
            panelists = ", ".join(deb.get("panelists_or_parties", []))
            vid_url = deb.get("video_url", "")
            
            st.markdown(f"""
            <div class="debate-card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <span class="badge-channel">📺 {deb.get('channel', 'Tamil TV')} • {deb.get('show_name', 'Debate')}</span>
                    <a href="{vid_url or '#'}" target="_blank" style="text-decoration:none; font-weight:bold; color:#C2410C;">▶️ Watch Program</a>
                </div>
                <h4 style="margin:0 0 4px 0; color:#C2410C;">🎙️ {deb.get('topic_en', '')}</h4>
                <h5 style="margin:0 0 10px 0; color:#EA580C; font-weight:normal;"><i>{deb.get('topic_ta', '')}</i></h5>
                <p style="margin-bottom:6px;"><b>Panelists / Represented Parties:</b> {panelists}</p>
                <p style="margin-bottom:6px; color:#1F2937;"><b>Clash & Arguments Summary:</b> {deb.get('clash_summary_en', '')}</p>
                <p style="margin-bottom:0; color:#431407; font-style:italic;">{deb.get('clash_summary_ta', '')}</p>
            </div>
            """, unsafe_allow_html=True)
            if vid_url and "youtube.com" in vid_url:
                try:
                    st.video(vid_url)
                except Exception:
                    pass

# TAB 4: CRITICISMS & REBUTTALS
with tab_criticisms:
    st.subheader("⚔️ Political Criticisms, Allegations & Rebuttals / குற்றச்சாட்டுகளும் பதிலடிகளும்")
    criticisms = report_data.get("political_criticisms_and_rebuttals", [])
    if not criticisms:
        st.info("No major party accusations or ministerial rebuttals logged for this date.")
    else:
        for crit in criticisms:
            accuser = crit.get("accuser_leader_or_party", "Critic")
            target = crit.get("targeted_leader_or_party", "Target")
            media = crit.get("media", {})
            card_img = resolve_card_image(accuser, media)

            c1, c2 = st.columns([1, 4]) if card_img else (None, None)
            if card_img:
                with c1:
                    st.image(card_img, caption=f"{accuser}", use_container_width=True)
                with c2:
                    st.markdown(f"""
                    <div class="criticism-card">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                            <span style="font-weight:700; color:#B45309;">{accuser} ➔ {target}</span>
                        </div>
                        <h4 style="margin:0 0 4px 0; color:#92400E;">⚠️ {crit.get('core_criticism_en', '')}</h4>
                        <h5 style="margin:0 0 8px 0; color:#B45309; font-weight:normal;"><i>{crit.get('core_criticism_ta', '')}</i></h5>
                        {"<p style='margin-bottom:6px; color:#065F46;'><b>🛡️ Rebuttal / Defense:</b> " + crit.get('rebuttal_or_defense_en') + "</p>" if crit.get('rebuttal_or_defense_en') else ""}
                        {"<p style='margin-bottom:6px; color:#047857; font-style:italic;'><i>" + crit.get('rebuttal_or_defense_ta') + "</i></p>" if crit.get('rebuttal_or_defense_ta') else ""}
                        {"<p style='margin-bottom:0; color:#6B7280; font-size:0.85rem;'><b>Context & Significance:</b> " + crit.get('political_significance') + "</p>" if crit.get('political_significance') else ""}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="criticism-card">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                        <span style="font-weight:700; color:#B45309;">{accuser} ➔ {target}</span>
                    </div>
                    <h4 style="margin:0 0 4px 0; color:#92400E;">⚠️ {crit.get('core_criticism_en', '')}</h4>
                    <h5 style="margin:0 0 8px 0; color:#B45309; font-weight:normal;"><i>{crit.get('core_criticism_ta', '')}</i></h5>
                    {"<p style='margin-bottom:6px; color:#065F46;'><b>🛡️ Rebuttal / Defense:</b> " + crit.get('rebuttal_or_defense_en') + "</p>" if crit.get('rebuttal_or_defense_en') else ""}
                    {"<p style='margin-bottom:6px; color:#047857; font-style:italic;'><i>" + crit.get('rebuttal_or_defense_ta') + "</i></p>" if crit.get('rebuttal_or_defense_ta') else ""}
                    {"<p style='margin-bottom:0; color:#6B7280; font-size:0.85rem;'><b>Context & Significance:</b> " + crit.get('political_significance') + "</p>" if crit.get('political_significance') else ""}
                </div>
                """, unsafe_allow_html=True)

# TAB 5: MoUs & INVESTMENTS
with tab_investments:
    st.subheader("💼 Industrial MoUs, Capital Inflows & Job Creation")
    mous = report_data.get("mous_and_investments", [])
    if not mous:
        st.info("No new major MoUs or industrial announcements filed today.")
    else:
        for mou in mous:
            amt = mou.get("investment_amount_inr", "Undisclosed")
            loc = mou.get("location_district", "Tamil Nadu")
            jobs = mou.get("jobs_created", "TBD")
            sector = mou.get("sector", "Industrial")
            status = mou.get("status", "MoU Signed")

            st.markdown(f"""
            <div class="mou-card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <span class="badge-money">💰 {amt}</span>
                    <span style="font-weight:600; color:#065F46;">Status: {status}</span>
                </div>
                <h4 style="margin:0 0 4px 0; color:#065F46;">🏢 {mou.get('company_or_investor')} — <span style="font-weight:normal; font-size:1rem;">{sector}</span></h4>
                <p style="margin-bottom:4px;">📍 <b>Location:</b> {loc} &nbsp;|&nbsp; 👷 <b>Projected Employment:</b> {jobs}</p>
                <p style="margin-bottom:6px; color:#1F2937;">{mou.get('details_en', '')}</p>
                <p style="margin-bottom:0; color:#374151; font-style:italic;">{mou.get('details_ta', '')}</p>
            </div>
            """, unsafe_allow_html=True)

# TAB 6: DISTRICT INDUSTRIAL MAP
with tab_map:
    st.subheader("🗺️ Tamil Nadu Industrial & Investment Distribution Map")
    district_data = pd.DataFrame([
        {"District": "Kanchipuram / Sriperumbudur", "Lat": 12.98, "Lon": 79.94, "Sector": "Electronics / Auto", "Investments": 14500},
        {"District": "Krishnagiri / Hosur", "Lat": 12.52, "Lon": 77.82, "Sector": "EV / Precision Engineering", "Investments": 18200},
        {"District": "Coimbatore", "Lat": 11.01, "Lon": 76.95, "Sector": "IT / Tech / Manufacturing", "Investments": 9400},
        {"District": "Tuticorin / Thoothukudi", "Lat": 8.76, "Lon": 78.13, "Sector": "Green Hydrogen / Port Infra", "Investments": 22000},
        {"District": "Madurai", "Lat": 9.92, "Lon": 78.11, "Sector": "TIDEL IT Park", "Investments": 4200},
        {"District": "Tiruchirappalli", "Lat": 10.79, "Lon": 78.70, "Sector": "Engineering / Heavy Industries", "Investments": 5300},
    ])
    fig = px.scatter_geo(
        district_data,
        lat="Lat",
        lon="Lon",
        hover_name="District",
        size="Investments",
        color="Sector",
        title="Key Industrial Investment Hubs & SIPCOT Parks (Tamil Nadu)",
        scope="asia",
        center={"lat": 11.0, "lon": 78.5},
        size_max=35
    )
    fig.update_geos(fitbounds="locations", visible=True)
    fig.update_layout(height=520, margin={"r":0,"t":40,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)

# TAB 7: STATEWIDE POLITICS & BILLS
with tab_politics:
    st.subheader("🗳️ Statewide Political Developments & Legislative Bills")
    politics = report_data.get("statewide_politics", report_data.get("key_political_developments", []))
    for pol in politics:
        party = pol.get("party_or_leader", "TN Politics")
        st.markdown(f"""
        <div class="political-card">
            <div style="margin-bottom:6px;"><span class="badge-party">{party}</span></div>
            <h4 style="margin:0 0 4px 0; color:#1E40AF;">📢 {pol.get('topic_en', '')}</h4>
            <h5 style="margin:0 0 8px 0; color:#2563EB; font-weight:normal;"><i>{pol.get('topic_ta', '')}</i></h5>
            <p style="margin-bottom:6px; color:#1F2937;">{pol.get('analysis_en', '')}</p>
            <p style="margin-bottom:0; color:#4B5563; font-style:italic;">{pol.get('analysis_ta', '')}</p>
        </div>
        """, unsafe_allow_html=True)

st.caption("Tamil Nadu 5-Tier AI Intelligence Radar • Multi-source verification • Powered by Gemini 2.5 Flash")
