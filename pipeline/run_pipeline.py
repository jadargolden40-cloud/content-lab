#!/usr/bin/env python3
"""
Content Lab — Full Pipeline Runner
Usage: python3 pipeline/run_pipeline.py --niche finance --topic "5 AI money tips 2026"
Flags:
  --niche     finance | ai | business
  --topic     Video title/topic
  --format    long (YouTube) | short (TikTok/Reels)
  --upload    Auto-upload after rendering
  --platforms youtube,tiktok,facebook
"""

import sys
import os

# Fix import path — add project root so 'pipeline' package is always found
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import click
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

load_dotenv()
console = Console()


@click.command()
@click.option('--niche', required=True, help='Content niche: finance | ai | business')
@click.option('--topic', required=True, help='Video topic / title')
@click.option('--format', 'fmt', default='long',
              type=click.Choice(['long', 'short']),
              help='long=YouTube 10min | short=TikTok 60s')
@click.option('--upload', is_flag=True, default=False,
              help='Auto-upload after rendering')
@click.option('--platforms', default='youtube',
              help='Comma-separated: youtube,tiktok,facebook')
def main(niche, topic, fmt, upload, platforms):
    """🎬 Content Lab — AI Video Factory"""

    console.print(Panel.fit(
        f"[bold green]🎬 Content Lab Pipeline[/bold green]\n"
        f"Niche: [cyan]{niche}[/cyan] | Format: [magenta]{fmt}[/magenta]\n"
        f"Topic: [yellow]{topic}[/yellow]\n"
        f"Upload: [red]{upload}[/red] → [white]{platforms}[/white]",
        title="Starting"
    ))

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:

        # Step 1: Generate Script
        task = progress.add_task("[cyan]Step 1/5 — Generating AI script...", total=None)
        from pipeline.steps.script_gen import generate_script
        script_path = generate_script(niche, topic, fmt)
        progress.update(task, description=f"[green]✅ Script saved: {script_path}")
        progress.stop_task(task)

        # Step 2: Generate Voiceover
        task2 = progress.add_task("[cyan]Step 2/5 — Generating AI voiceover...", total=None)
        from pipeline.steps.tts_gen import generate_voice
        audio_path = generate_voice(script_path)
        progress.update(task2, description=f"[green]✅ Audio saved: {audio_path}")
        progress.stop_task(task2)

        # Step 3: Fetch B-roll footage
        task3 = progress.add_task("[cyan]Step 3/5 — Fetching stock footage...", total=None)
        from pipeline.steps.footage_fetch import fetch_footage
        footage_paths = fetch_footage(topic, fmt)
        progress.update(task3, description=f"[green]✅ Footage: {len(footage_paths)} clips")
        progress.stop_task(task3)

        # Step 4: Assemble Video
        task4 = progress.add_task("[cyan]Step 4/5 — Assembling video with FFmpeg...", total=None)
        from pipeline.steps.video_assemble import assemble_video
        video_path = assemble_video(audio_path, footage_paths, topic, fmt)
        progress.update(task4, description=f"[green]✅ Video ready: {video_path}")
        progress.stop_task(task4)

        # Step 4b: Generate Thumbnail
        from pipeline.steps.thumbnail_gen import generate_thumbnail
        thumbnail_path = generate_thumbnail(topic, niche)
        progress.update(task4, description=f"[green]✅ Video + thumbnail ready")
        progress.stop_task(task4)

        # Step 5: Upload (optional)
        video_id = None
        if upload:
            task5 = progress.add_task("[cyan]Step 5/5 — Uploading to platforms...", total=None)
            from pipeline.steps.uploader import upload_video
            for platform in platforms.split(','):
                vid = upload_video(video_path, topic, niche, platform.strip())
                if vid and platform.strip() == 'youtube':
                    video_id = vid
            # Upload thumbnail to YouTube
            if video_id and thumbnail_path:
                from pipeline.steps.thumbnail_gen import upload_thumbnail
                upload_thumbnail(video_id, thumbnail_path)
            progress.update(task5, description="[green]✅ Uploaded!")
            progress.stop_task(task5)
        else:
            console.print("[yellow]ℹ️  Skipping upload. Add --upload to auto-post.")

    console.print(Panel.fit(
        f"[bold green]🎉 Done![/bold green]\n"
        f"Video: [cyan]{video_path}[/cyan]",
        title="Pipeline Complete"
    ))


if __name__ == '__main__':
    main()
