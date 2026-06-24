#!/usr/bin/env python3
"""
Step 2 — AI Voiceover Generator
Python 3.12 compatible — Coqui TTS removed (no Python 3.12 support)

TTS Engine priority (set TTS_ENGINE in .env):
  edge    = Microsoft Edge TTS — FREE, online, realistic, 400+ voices (DEFAULT)
  pyttsx3 = Fully offline, no internet, basic quality
  elevenlabs = Paid, ultra-realistic

Usage in .env:
  TTS_ENGINE=edge          # default — free & good quality
  TTS_ENGINE=pyttsx3       # fully offline fallback
  TTS_ENGINE=elevenlabs    # paid premium
"""

import os
import asyncio
import subprocess
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


def read_script(path: str) -> str:
    """Read script file, skip comment header lines."""
    with open(path) as f:
        lines = f.readlines()
    return ' '.join(l.strip() for l in lines if not l.startswith('#')).strip()


def generate_voice_edge(text: str, out_path: str) -> str:
    """
    Microsoft Edge TTS — FREE, online, very realistic.
    400+ voices including: en-US-GuyNeural, en-US-JennyNeural, en-GB-RyanNeural
    Set EDGE_TTS_VOICE in .env to change voice.
    """
    try:
        import edge_tts

        voice = os.getenv('EDGE_TTS_VOICE', 'en-US-GuyNeural')
        mp3_path = out_path.replace('.wav', '.mp3')

        async def _run():
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(mp3_path)

        asyncio.run(_run())

        # Convert mp3 → wav using ffmpeg
        subprocess.run([
            'ffmpeg', '-y', '-i', mp3_path,
            '-acodec', 'pcm_s16le', '-ar', '22050', out_path
        ], check=True, capture_output=True)
        os.remove(mp3_path)

        print(f"✅ Voiceover with Edge TTS ({voice}): {out_path}")
        return out_path

    except Exception as e:
        raise RuntimeError(f"❌ Edge TTS failed: {e}")


def generate_voice_pyttsx3(text: str, out_path: str) -> str:
    """
    pyttsx3 — fully OFFLINE, no internet, basic robotic quality.
    Good fallback when you have no internet connection.
    """
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty('rate', 175)    # speaking speed
        engine.setProperty('volume', 1.0)
        engine.save_to_file(text, out_path)
        engine.runAndWait()
        print(f"✅ Voiceover with pyttsx3 (offline): {out_path}")
        return out_path
    except Exception as e:
        raise RuntimeError(f"❌ pyttsx3 failed: {e}")


def generate_voice_elevenlabs(text: str, out_path: str) -> str:
    """ElevenLabs — paid, ultra-realistic, multilingual."""
    try:
        from elevenlabs.client import ElevenLabs
        client = ElevenLabs(api_key=os.getenv('ELEVENLABS_API_KEY'))
        audio = client.generate(
            text=text,
            voice=os.getenv('ELEVENLABS_VOICE_ID', 'Adam'),
            model='eleven_multilingual_v2'
        )
        with open(out_path, 'wb') as f:
            for chunk in audio:
                f.write(chunk)
        print(f"✅ Voiceover with ElevenLabs: {out_path}")
        return out_path
    except Exception as e:
        raise RuntimeError(f"❌ ElevenLabs failed: {e}")


def generate_voice(script_path: str) -> str:
    """Generate voiceover audio from script. Engine selected via TTS_ENGINE in .env"""

    text = read_script(script_path)
    engine = os.getenv('TTS_ENGINE', 'edge').lower()

    os.makedirs('output/audio', exist_ok=True)
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    out = f"output/audio/{ts}_voiceover.wav"

    print(f"  🎙️  Generating voiceover with engine: {engine}")

    if engine == 'elevenlabs' and os.getenv('ELEVENLABS_API_KEY'):
        try:
            return generate_voice_elevenlabs(text, out)
        except Exception as e:
            print(f"  ⚠️  ElevenLabs failed: {e} — falling back to edge-tts")
            engine = 'edge'

    if engine == 'pyttsx3':
        try:
            return generate_voice_pyttsx3(text, out)
        except Exception as e:
            print(f"  ⚠️  pyttsx3 failed: {e} — falling back to edge-tts")
            engine = 'edge'

    # Default / fallback: edge-tts (FREE, online, best free quality)
    return generate_voice_edge(text, out)
