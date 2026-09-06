# 🏛️ Tamil Nadu Politics & Legislative Assembly AI Intelligence Agent

An automated intelligence agent that continuously collects, monitors, and synthesizes Tamil Nadu political developments, legislative assembly floor debates, heated moments, walkouts, and policy bills.

---

## 🌟 Key Features

1. **💻 Laptop Web Dashboard (Streamlit)**:
   - Visual executive briefings with bilingual toggle (**English + தமிழ்**).
   - High-priority cards for **Heated Assembly Moments & Walkouts** (with speaker attribution, party badges, and intensity indicators).
   - Dedicated sections for **Political Fronts (DMK, AIADMK, BJP, TVK, VCK, PMK, NTK)** and **Assembly Bills/Policies**.
   - One-click trigger button to force an instant fresh scan.

2. **📱 Mobile Updates (Telegram Bot)**:
   - Compact, rich-text bilingual digest pushed directly to your Telegram chat.
   - Highlights heated exchanges and top political news in seconds.

3. **🤖 Google Gemini AI Engine**:
   - Analyzes raw multi-source news (Tamil & English RSS, Google News feeds, Assembly coverage).
   - Generates structured, high-accuracy bilingual briefings.

4. **⏰ Automated Scheduling**:
   - Runs unattended twice a day (Morning 8:00 AM & Evening 6:30 PM post-Assembly floor adjournment).

---

## 🚀 Quick Setup & Usage

### 1. Configure Environment Variables
Copy `.env.example` to `.env` and fill in your keys:
```bash
cp .env.example .env
```
Inside `.env`:
```ini
GEMINI_API_KEY=your_gemini_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here
```

> **How to get keys:**
> - **Gemini API**: Get a free key at [Google AI Studio](https://aistudio.google.com/).
> - **Telegram Bot**: Open Telegram, search `@BotFather`, type `/newbot` to get your `TELEGRAM_BOT_TOKEN`. Then message `@userinfobot` to get your numeric `TELEGRAM_CHAT_ID`.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch Web Dashboard (Laptop)
```bash
streamlit run web/app.py
```
Open `http://localhost:8501` in your browser.

### 4. Run Daily Agent Once (Manual execution)
```bash
python agent_pipeline.py
```

### 5. Run Continuous Background Scheduler
```bash
python scheduler.py
```
