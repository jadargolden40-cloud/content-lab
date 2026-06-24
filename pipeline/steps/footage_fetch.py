#!/usr/bin/env python3
"""
Step 3 — Stock Footage Fetcher
Downloads free B-roll from Pexels API (FREE)
Get your free key at: pexels.com/api
"""

import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


def fetch_pexels(query: str, count: int = 5, vertical: bool = False) -> list:
    """Search Pexels for video clips, return list of download URLs."""
    key = os.getenv('PEXELS_API_KEY', '')
    if not key:
        print("⚠️  No PEXELS_API_KEY in .env — get a free key at pexels.com/api")
        return []

    orientation = 'portrait' if vertical else 'landscape'
    try:
        r = requests.get(
            f"https://api.pexels.com/videos/search",
            params={"query": query, "per_page": count, "orientation": orientation},
            headers={"Authorization": key}, timeout=15
        )
        urls = []
        for v in r.json().get('videos', []):
            for f in v.get('video_files', []):
                if f.get('quality') in ['hd', 'sd']:
                    urls.append(f['link'])
                    break
        return urls
    except Exception as e:
        print(f"⚠️  Pexels error: {e}")
        return []


def download_clip(url: str, path: str) -> str:
    """Download a single clip to disk."""
    try:
        r = requests.get(url, stream=True, timeout=30)
        with open(path, 'wb') as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
        return path
    except Exception as e:
        print(f"⚠️  Download failed: {e}")
        return None


def fetch_footage(topic: str, fmt: str = 'long') -> list:
    """Fetch and download stock footage clips for the video."""
    vertical = (fmt == 'short')
    clip_count = 3 if fmt == 'short' else 6

    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    out_dir = f"output/footage/{ts}"
    os.makedirs(out_dir, exist_ok=True)

    # Build search queries from topic keywords
    words = [w for w in topic.lower().split() if len(w) > 3][:3]
    queries = words + ['business', 'technology', 'money']

    all_urls = []
    for q in queries:
        all_urls.extend(fetch_pexels(q, count=2, vertical=vertical))
        if len(all_urls) >= clip_count:
            break

    downloaded = []
    for i, url in enumerate(all_urls[:clip_count]):
        path = f"{out_dir}/clip_{i+1:02d}.mp4"
        result = download_clip(url, path)
        if result:
            downloaded.append(result)
            print(f"  📥 Clip {i+1}/{clip_count} downloaded")

    if not downloaded:
        print("⚠️  No footage downloaded — video will use black background")

    return downloaded
