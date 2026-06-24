# 🎬 Content Lab — AI-Powered Video Factory

> Full pipeline: Niche idea → AI Script → AI Voiceover → AI Video → Auto-upload to YouTube, TikTok & Facebook

## 📁 Repo Structure

```
content-lab/
├── setup/          # One-time Ubuntu installation scripts
├── pipeline/       # Core pipeline (script → voice → video → upload)
│   └── steps/      # Each pipeline step as a module
├── tools/          # Auth helpers for each platform
├── scheduler/      # Auto-posting scheduler
├── niches/         # Prompts & 30-day content calendar
│   └── prompts/
├── monetization/   # Revenue tracker & affiliate links
└── docs/           # Step-by-step guides
```

## ⚡ Quick Start (Ubuntu)

```bash
# 1. Clone
git clone https://github.com/jadargolden40-cloud/content-lab.git
cd content-lab

# 2. Install everything automatically
chmod +x setup/install.sh
./setup/install.sh

# 3. Add your API keys
cp .env.example .env
nano .env

# 4. Run your first video
source venv/bin/activate
python3 pipeline/run_pipeline.py --niche finance --topic "5 AI money tips 2026"
```

## 🧠 What Gets Installed

| Tool | Purpose | Cost |
|------|---------|------|
| Ollama + Mistral | Local AI script writing | FREE |
| Coqui TTS | AI voiceover generation | FREE |
| FFmpeg | Video assembly & encoding | FREE |
| yt-dlp | Download reference footage | FREE |
| n8n | Workflow automation | FREE |
| Kdenlive | Video editor GUI | FREE |
| Python 3.11 | Pipeline scripting | FREE |

## 💰 Target Earnings by Platform

| Platform | Niche | RPM |
|----------|-------|-----|
| YouTube | Finance / AI | $10–$25 |
| TikTok | Finance tips | Highest + brand deals |
| Facebook | Business content | $3–$8 |

## 📅 30-Day Content Calendar
See `niches/content_calendar.md`

## 📖 Full Setup Guide
See `docs/getting_started.md`
