#!/bin/bash
# ============================================
# CONTENT LAB — Ubuntu Full Setup Script
# Usage: chmod +x setup/install.sh && ./setup/install.sh
# ============================================
set -e
echo "🚀 Starting Content Lab setup on Ubuntu..."

# --- System packages ---
echo "📦 Installing system packages..."
sudo apt update && sudo apt upgrade -y
sudo apt install -y \
  python3 python3-pip python3-venv \
  ffmpeg git curl wget \
  nodejs npm \
  imagemagick espeak-ng \
  libsndfile1 build-essential \
  kdenlive

# --- yt-dlp ---
echo "📥 Installing yt-dlp..."
sudo curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp \
  -o /usr/local/bin/yt-dlp
sudo chmod a+rx /usr/local/bin/yt-dlp
echo "✅ yt-dlp installed"

# --- Python venv ---
echo "🐍 Setting up Python environment..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r setup/requirements.txt
echo "✅ Python environment ready"

# --- Ollama (local AI — FREE) ---
echo "🧠 Installing Ollama (local AI)..."
curl -fsSL https://ollama.ai/install.sh | sh
echo "⬇️  Pulling Mistral model (a few minutes)..."
ollama pull mistral
echo "✅ Ollama + Mistral ready"

# --- Coqui TTS (local voice — FREE) ---
echo "🎙️  Installing Coqui TTS..."
pip install TTS
echo "✅ Coqui TTS installed"

# --- n8n automation ---
echo "⚙️  Installing n8n..."
sudo npm install -g n8n
echo "✅ n8n installed — run with: n8n start"

# --- Output folders ---
mkdir -p output/scripts output/audio output/footage \
         output/video output/shorts output/thumbnails
echo "📁 Output folders created"

# --- Env file ---
if [ ! -f .env ]; then
  cp .env.example .env
  echo "⚠️  .env created — fill in your keys: nano .env"
fi

echo ""
echo "============================================"
echo "✅ CONTENT LAB SETUP COMPLETE!"
echo "============================================"
echo ""
echo "Next steps:"
echo "  1. Add API keys:     nano .env"
echo "  2. Activate venv:    source venv/bin/activate"
echo "  3. First video:"
echo "     python3 pipeline/run_pipeline.py \\"
echo "       --niche finance \\"
echo "       --topic \"5 AI money tips 2026\""
echo ""
