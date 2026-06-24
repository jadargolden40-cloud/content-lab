#!/bin/bash
# ============================================
# CONTENT LAB — Ubuntu Full Setup Script
# Works on Python 3.12 / 3.13 / 3.14
# Usage: chmod +x setup/install.sh && ./setup/install.sh
# ============================================
set -e
echo "🚀 Starting Content Lab setup..."
echo "   Python: $(python3 --version)"
echo "   Ubuntu: $(lsb_release -d | cut -f2)"
echo ""

# -----------------------------------------------
# 1. SYSTEM PACKAGES
# -----------------------------------------------
echo "📦 Installing system packages..."
sudo apt update -y

# Core tools
sudo apt install -y \
  python3 python3-pip python3-venv python3-dev \
  ffmpeg git curl wget \
  nodejs npm \
  imagemagick \
  espeak-ng espeak-ng-data \
  libsndfile1 libsndfile1-dev \
  build-essential pkg-config \
  kdenlive

# Pillow build dependencies (JPEG, PNG, TIFF, WebP, etc.)
echo "🖼️  Installing Pillow system dependencies..."
sudo apt install -y \
  libjpeg-dev \
  libpng-dev \
  libtiff-dev \
  libwebp-dev \
  libopenjp2-7-dev \
  zlib1g-dev \
  libfreetype6-dev \
  liblcms2-dev \
  libffi-dev \
  libbz2-dev

# pyttsx3 / audio dependencies
echo "🔊 Installing audio system dependencies..."
sudo apt install -y \
  python3-espeak \
  libespeak1 \
  portaudio19-dev \
  python3-pyaudio \
  ffmpeg \
  sox || true   # sox not critical, ignore if missing

echo "✅ System packages installed"

# -----------------------------------------------
# 2. YT-DLP
# -----------------------------------------------
echo "📥 Installing yt-dlp..."
sudo curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp \
  -o /usr/local/bin/yt-dlp
sudo chmod a+rx /usr/local/bin/yt-dlp
echo "✅ yt-dlp installed"

# -----------------------------------------------
# 3. PYTHON VIRTUAL ENVIRONMENT
# -----------------------------------------------
echo "🐍 Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
echo "✅ venv ready"

# -----------------------------------------------
# 4. PYTHON PACKAGES
# Install in stages so one failure doesn't kill everything
# -----------------------------------------------
echo "📦 Installing Python packages (stage 1/3 — core)..."
pip install requests python-dotenv click rich pyyaml schedule

echo "📦 Installing Python packages (stage 2/3 — AI & TTS)..."
pip install openai anthropic ollama
pip install edge-tts
pip install pyttsx3 || echo "⚠️  pyttsx3 optional — skipping if it fails"

echo "📦 Installing Python packages (stage 3/3 — video & APIs)..."
pip install Pillow moviepy pydub
pip install google-auth google-auth-oauthlib google-api-python-client
pip install apscheduler

echo "✅ All Python packages installed"

# -----------------------------------------------
# 5. OLLAMA (local AI — FREE)
# -----------------------------------------------
echo "🧠 Installing Ollama (local AI engine)..."
curl -fsSL https://ollama.ai/install.sh | sh
echo "⬇️  Pulling Mistral model (takes a few minutes on first run)..."
ollama pull mistral
echo "✅ Ollama + Mistral ready"

# -----------------------------------------------
# 6. N8N AUTOMATION
# -----------------------------------------------
echo "⚙️  Installing n8n workflow automation..."
sudo npm install -g n8n
echo "✅ n8n installed — start with: n8n start"

# -----------------------------------------------
# 7. OUTPUT FOLDERS
# -----------------------------------------------
mkdir -p output/scripts output/audio output/footage \
         output/video output/shorts output/thumbnails
echo "📁 Output folders created"

# -----------------------------------------------
# 8. ENV FILE
# -----------------------------------------------
if [ ! -f .env ]; then
  cp .env.example .env
  echo "⚠️  .env file created — add your API keys: nano .env"
fi

# -----------------------------------------------
# DONE
# -----------------------------------------------
echo ""
echo "============================================"
echo "✅  CONTENT LAB SETUP COMPLETE!"
echo "============================================"
echo ""
echo "Next steps:"
echo "  1. Add your API keys:    nano .env"
echo "  2. Activate the venv:    source venv/bin/activate"
echo "  3. Make your first video:"
echo ""
echo "     python3 pipeline/run_pipeline.py \\"
echo "       --niche finance \\"
echo "       --topic \"5 AI money tips 2026\""
echo ""
echo "  4. To auto-post on schedule:"
echo "     python3 scheduler/post_scheduler.py"
echo ""
