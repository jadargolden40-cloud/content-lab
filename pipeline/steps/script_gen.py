#!/usr/bin/env python3
"""
Step 1 — AI Script Generator
Uses Ollama/Mistral locally (FREE) by default.
Falls back to OpenAI or Anthropic if configured in .env
"""

import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Niche-specific prompt templates
PROMPTS = {
    "finance": """You are a viral finance content creator on YouTube and TikTok.
Write a complete video script titled: "{topic}"
Format: {fmt} video

Rules:
- Hook in first 3 seconds (shocking stat, bold claim, or question)
- Use simple everyday language — no jargon
- Include 5 specific actionable tips with real numbers
- Call to action at the end (like, follow, subscribe)
- SHORT format = 60 seconds (~150 words)
- LONG format = 8-10 minutes (~1,400 words) with timestamps

Write the full script now:""",

    "ai": """You are a viral AI/tech content creator.
Write a complete video script titled: "{topic}"
Format: {fmt} video

Rules:
- Hook: start with a mind-blowing AI fact or demo result
- Show exact steps to use the tool
- Include timestamps for long format
- Strong CTA at the end
- SHORT = 60s (~150 words) | LONG = 8-10min (~1,400 words)

Write the full script now:""",

    "business": """You are a viral business and entrepreneurship content creator.
Write a complete video script titled: "{topic}"
Format: {fmt} video

Rules:
- Open with a bold income claim or real story
- Break down the strategy step by step
- Use real examples and dollar amounts
- Strong CTA at end
- SHORT = 60s (~150 words) | LONG = 8-10min (~1,400 words)

Write the full script now:""",
}

DEFAULT_PROMPT = """You are a viral content creator. Write a video script titled: "{topic}"
Niche: {niche} | Format: {fmt}
Include a hook, 5 main points with examples, and a CTA.
Write the full script now:"""


def generate_script(niche: str, topic: str, fmt: str = 'long') -> str:
    """Generate AI script and save to output/scripts/"""

    template = PROMPTS.get(niche, DEFAULT_PROMPT)
    prompt = template.format(topic=topic, niche=niche, fmt=fmt)
    script_text = None

    # Try 1: Ollama (local, FREE)
    try:
        resp = requests.post(
            f"{os.getenv('OLLAMA_URL', 'http://localhost:11434')}/api/generate",
            json={"model": os.getenv('OLLAMA_MODEL', 'mistral'),
                  "prompt": prompt, "stream": False},
            timeout=120
        )
        if resp.status_code == 200:
            script_text = resp.json().get('response', '')
            print("✅ Script generated with Ollama (local, free)")
    except Exception as e:
        print(f"⚠️  Ollama unavailable: {e}")

    # Try 2: OpenAI fallback
    if not script_text and os.getenv('OPENAI_API_KEY'):
        try:
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000
            )
            script_text = resp.choices[0].message.content
            print("✅ Script generated with OpenAI GPT-4o-mini")
        except Exception as e:
            print(f"⚠️  OpenAI failed: {e}")

    # Try 3: Anthropic Claude fallback
    if not script_text and os.getenv('ANTHROPIC_API_KEY'):
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
            msg = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            script_text = msg.content[0].text
            print("✅ Script generated with Claude")
        except Exception as e:
            print(f"⚠️  Anthropic failed: {e}")

    if not script_text:
        raise RuntimeError("❌ All AI engines failed. Check your .env settings.")

    # Save script to file
    os.makedirs('output/scripts', exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe = topic.replace(' ', '_').replace('/', '-')[:50]
    path = f"output/scripts/{timestamp}_{safe}.txt"

    with open(path, 'w') as f:
        f.write(f"# NICHE: {niche}\n# TOPIC: {topic}\n# FORMAT: {fmt}\n")
        f.write(f"# GENERATED: {datetime.now().isoformat()}\n\n")
        f.write(script_text)

    return path
