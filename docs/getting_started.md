# 🚀 Getting Started — Content Lab on Ubuntu

## Step 1 — Clone & Install

```bash
git clone https://github.com/jadargolden40-cloud/content-lab.git
cd content-lab
chmod +x setup/install.sh
./setup/install.sh
```

This installs: Python 3, FFmpeg, Ollama + Mistral (free AI), Coqui TTS, n8n, yt-dlp, Kdenlive.

---

## Step 2 — Configure Keys

```bash
nano .env
```

Minimum to start (all free):
- `PEXELS_API_KEY` — free at pexels.com/api (stock footage)
- Ollama runs locally, no key needed

To enable uploads see: `docs/platform_setup.md`

---

## Step 3 — Make Your First Video

```bash
source venv/bin/activate

# Generate only (no upload)
python3 pipeline/run_pipeline.py \
  --niche finance \
  --topic "5 ways to make money with AI in 2026"

# Generate + upload to YouTube
python3 pipeline/run_pipeline.py \
  --niche finance \
  --topic "5 ways to make money with AI in 2026" \
  --upload --platforms youtube

# TikTok short (vertical)
python3 pipeline/run_pipeline.py \
  --niche finance \
  --topic "Best money tip 2026" \
  --format short \
  --upload --platforms tiktok,facebook

# All platforms at once
python3 pipeline/run_pipeline.py \
  --niche ai \
  --topic "3 free AI tools that replace a $500 employee" \
  --format long \
  --upload --platforms youtube,tiktok,facebook
```

---

## Step 4 — Auto-Scheduler

```bash
# Edit your posting schedule
nano scheduler/schedule.yaml

# Start scheduler
python3 scheduler/post_scheduler.py

# Run in background (survives terminal close)
nohup python3 scheduler/post_scheduler.py > scheduler.log 2>&1 &
```

---

## Step 5 — Platform Authentication

### YouTube
```bash
# 1. Get OAuth credentials from Google Cloud Console:
#    console.cloud.google.com → APIs → YouTube Data API v3 → OAuth 2.0 credentials
# 2. Download JSON → save as tools/youtube_credentials.json
# 3. Run once:
python3 tools/youtube_auth.py
# Browser opens → approve → token saved automatically
```

### TikTok
1. Go to developers.tiktok.com → Create app
2. Add Client Key + Secret to `.env`
3. Get Access Token via OAuth flow

### Facebook
1. Go to developers.facebook.com → Create app
2. Add Facebook Login + Video API
3. Get Page Access Token → add to `.env`

---

## Output Folders

```
output/
├── scripts/     # AI-generated scripts (.txt)
├── audio/       # Voiceover files (.wav)
├── footage/     # Downloaded B-roll clips
├── video/       # Final long-form (1920×1080)
└── shorts/      # Final short videos (1080×1920)
```

---

## Troubleshooting

```bash
# Ollama not running
ollama serve
ollama list    # check models loaded

# FFmpeg errors
ffmpeg -version
sudo apt install ffmpeg

# Python package issues
source venv/bin/activate
pip install -r setup/requirements.txt --upgrade

# Permission error on install.sh
chmod +x setup/install.sh
```
