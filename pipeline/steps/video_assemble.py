#!/usr/bin/env python3
"""
Step 4 — Video Assembler
Combines stock footage + AI voiceover + title overlay using FFmpeg
"""

import os
import json
import subprocess
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


def get_duration(path: str) -> float:
    """Get audio/video duration in seconds using ffprobe."""
    cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_streams', path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)
    return float(data['streams'][0].get('duration', 60))


def make_placeholder(duration: float, res: str, out: str):
    """Create black background video when no footage available."""
    w, h = res.split('x')
    subprocess.run([
        'ffmpeg', '-y', '-f', 'lavfi',
        '-i', f'color=c=black:size={w}x{h}:rate=30',
        '-t', str(duration), '-c:v', 'libx264', '-pix_fmt', 'yuv420p', out
    ], check=True, capture_output=True)


def concat_footage(clips: list, duration: float, res: str, out: str):
    """Loop and concat footage clips to match audio duration."""
    if not clips:
        make_placeholder(duration, res, out)
        return

    list_path = out.replace('.mp4', '_list.txt')
    repeated = clips * (int(duration // 8) + 3)
    with open(list_path, 'w') as f:
        for c in repeated:
            f.write(f"file '{os.path.abspath(c)}'\n")

    w, h = res.split('x')
    subprocess.run([
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', list_path,
        '-t', str(duration),
        '-vf', f'scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2',
        '-c:v', 'libx264', '-preset', 'fast', '-pix_fmt', 'yuv420p', out
    ], check=True, capture_output=True)
    os.remove(list_path)


def merge_audio(video: str, audio: str, out: str):
    """Merge video track with audio voiceover."""
    subprocess.run([
        'ffmpeg', '-y', '-i', video, '-i', audio,
        '-map', '0:v', '-map', '1:a',
        '-c:v', 'copy', '-c:a', 'aac', '-shortest', out
    ], check=True, capture_output=True)


def add_title(video: str, title: str, out: str):
    """Overlay title text on first 4 seconds of video."""
    safe = title.replace("'", r"\'").replace('"', r'\"')[:60]
    subprocess.run([
        'ffmpeg', '-y', '-i', video,
        '-vf', (
            f"drawtext=text='{safe}':fontsize=52:fontcolor=white"
            f":shadowcolor=black:shadowx=3:shadowy=3"
            f":x=(w-text_w)/2:y=h*0.08:enable='between(t,0,4)'"
        ),
        '-c:v', 'libx264', '-preset', 'fast', '-c:a', 'copy', out
    ], check=True, capture_output=True)


def assemble_video(audio_path: str, footage: list, title: str, fmt: str = 'long') -> str:
    """Full assembly: footage + audio + title → final video file."""

    res = os.getenv('SHORTS_RESOLUTION', '1080x1920') if fmt == 'short' \
        else os.getenv('VIDEO_RESOLUTION', '1920x1080')

    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe = title.replace(' ', '_')[:40]
    out_dir = 'output/shorts' if fmt == 'short' else 'output/video'
    os.makedirs(out_dir, exist_ok=True)

    raw = f"{out_dir}/{ts}_raw.mp4"
    merged = f"{out_dir}/{ts}_merged.mp4"
    final = f"{out_dir}/{ts}_{safe}.mp4"

    print("  🎞️  Getting audio duration...")
    duration = get_duration(audio_path)
    print(f"  🎬 Building {len(footage)}-clip backdrop ({duration:.1f}s)...")
    concat_footage(footage, duration, res, raw)
    print("  🔊 Merging audio...")
    merge_audio(raw, audio_path, merged)
    print("  🏷️  Adding title overlay...")
    add_title(merged, title, final)

    for tmp in [raw, merged]:
        if os.path.exists(tmp):
            os.remove(tmp)

    print(f"  ✅ Final video: {final}")
    return final
