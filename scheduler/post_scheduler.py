#!/usr/bin/env python3
"""
Content Lab — Auto Posting Scheduler
Reads scheduler/schedule.yaml and runs the pipeline automatically
Usage: python3 scheduler/post_scheduler.py
Background: nohup python3 scheduler/post_scheduler.py &
"""

import schedule
import time
import subprocess
import yaml
from datetime import datetime
from rich.console import Console

console = Console()


def load_schedule(path='scheduler/schedule.yaml') -> list:
    with open(path) as f:
        return yaml.safe_load(f).get('posts', [])


def run_job(niche: str, topic: str, fmt: str, platforms: str):
    console.print(f"\n⏰ [{datetime.now().strftime('%H:%M')}] Running: [yellow]{topic}[/yellow]")
    result = subprocess.run([
        'python3', 'pipeline/run_pipeline.py',
        '--niche', niche, '--topic', topic,
        '--format', fmt, '--upload', '--platforms', platforms
    ])
    if result.returncode == 0:
        console.print(f"✅ Done: {topic}")
    else:
        console.print(f"❌ Failed: {topic}")


def start():
    posts = load_schedule()
    console.print(f"📅 Loaded {len(posts)} scheduled posts\n")

    for post in posts:
        niche = post.get('niche', 'finance')
        topic = post.get('topic', 'Make money with AI')
        fmt = post.get('format', 'long')
        platforms = post.get('platforms', 'youtube')
        time_str = post.get('time', '09:00')
        days = post.get('days', ['monday'])

        for day in days:
            fn = lambda n=niche, t=topic, f=fmt, p=platforms: run_job(n, t, f, p)
            getattr(schedule.every(), day).at(time_str).do(fn)
            console.print(f"  📌 {day.capitalize()} {time_str} → [{niche}] {topic[:50]}")

    console.print("\n🚀 Scheduler running. Ctrl+C to stop.\n")
    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == '__main__':
    start()
