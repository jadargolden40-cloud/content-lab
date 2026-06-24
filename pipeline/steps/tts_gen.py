#!/usr/bin/env python3
"""
Step 2 — AI Voiceover Generator
Coqui TTS = local, FREE (default)
ElevenLabs = paid, ultra-realistic (set TTS_ENGINE=elevenlabs in .env)
"""

import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


def read_script(path: str) -> str:
    """Read script file, strip comment header lines."""
    with open(path) as f:
        lines = f.readlines()
    return ' '.join(l for l in lines if not l.startswith('#')).strip()


def generate_voice(script_path: str) -> str:
    """Generate voiceover .wav from script file."""
    text = read_script(script_path)
    engine = os.getenv('TTS_ENGINE', 'coqui')

    os.makedirs('output/audio', exist_ok=True)
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    out = f"output/audio/{ts}_voiceover.wav"

    # ElevenLabs (paid — ultra-realistic)
    if engine == 'elevenlabs' and os.getenv('ELEVENLABS_API_KEY'):
        try:
            from elevenlabs.client import ElevenLabs
            client = ElevenLabs(api_key=os.getenv('ELEVENLABS_API_KEY'))
            audio = client.generate(
                text=text,
                voice=os.getenv('ELEVENLABS_VOICE_ID', 'Adam'),
                model='eleven_multilingual_v2'
            )
            with open(out, 'wb') as f:
                for chunk in audio:
                    f.write(chunk)
            print(f"✅ Voiceover with ElevenLabs: {out}")
            return out
        except Exception as e:
            print(f"⚠️  ElevenLabs failed: {e} — falling back to Coqui")

    # Coqui TTS (local, FREE)
    try:
        from TTS.api import TTS
        tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")
        tts.tts_to_file(text=text, file_path=out)
        print(f"✅ Voiceover with Coqui TTS: {out}")
        return out
    except Exception as e:
        raise RuntimeError(f"❌ TTS failed: {e}")
