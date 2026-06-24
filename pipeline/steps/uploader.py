#!/usr/bin/env python3
"""
Step 5 — Multi-Platform Uploader
Supports: YouTube, TikTok, Facebook
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()


def upload_youtube(video_path: str, title: str, niche: str):
    """Upload to YouTube via Data API v3. Run tools/youtube_auth.py first."""
    try:
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        from google.oauth2.credentials import Credentials

        token = 'tools/youtube_token.json'
        if not os.path.exists(token):
            print("⚠️  YouTube not authenticated. Run: python3 tools/youtube_auth.py")
            return

        creds = Credentials.from_authorized_user_file(token)
        yt = build('youtube', 'v3', credentials=creds)

        tags = {
            'finance': ['money', 'finance', 'investing', 'passive income', 'side hustle', '2026'],
            'ai':      ['ai', 'artificial intelligence', 'automation', 'chatgpt', 'tech', '2026'],
            'business':['business', 'entrepreneur', 'startup', 'make money online', '2026'],
        }.get(niche, ['2026', 'content', 'viral'])

        body = {
            'snippet': {
                'title': title,
                'description': f'{title}\n\n#finance #ai #money #2026\n\nFor educational purposes only.',
                'tags': tags,
                'categoryId': '27'  # Education
            },
            'status': {'privacyStatus': 'public'}
        }
        media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
        req = yt.videos().insert(part='snippet,status', body=body, media_body=media)
        resp = req.execute()
        print(f"✅ YouTube upload: https://youtube.com/watch?v={resp.get('id')}")

    except Exception as e:
        print(f"❌ YouTube upload failed: {e}")


def upload_facebook(video_path: str, title: str):
    """Upload video to Facebook Page via Graph API."""
    page_id = os.getenv('FACEBOOK_PAGE_ID')
    token = os.getenv('FACEBOOK_ACCESS_TOKEN')
    if not page_id or not token:
        print("⚠️  FACEBOOK_PAGE_ID / FACEBOOK_ACCESS_TOKEN missing in .env")
        return
    try:
        url = f"https://graph-video.facebook.com/v19.0/{page_id}/videos"
        with open(video_path, 'rb') as f:
            r = requests.post(url,
                data={'title': title,
                      'description': f'{title} #finance #money #ai',
                      'access_token': token},
                files={'source': f})
        if r.status_code == 200:
            print(f"✅ Facebook upload success")
        else:
            print(f"❌ Facebook failed: {r.text}")
    except Exception as e:
        print(f"❌ Facebook error: {e}")


def upload_tiktok(video_path: str, title: str):
    """Upload to TikTok via Content Posting API v2."""
    token = os.getenv('TIKTOK_ACCESS_TOKEN')
    if not token:
        print("⚠️  TIKTOK_ACCESS_TOKEN missing. Get it at: developers.tiktok.com")
        return
    try:
        size = os.path.getsize(video_path)
        headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

        # Init upload
        init = requests.post(
            "https://open.tiktokapis.com/v2/post/publish/video/init/",
            headers=headers,
            json={
                'post_info': {
                    'title': title[:150],
                    'privacy_level': 'PUBLIC_TO_EVERYONE',
                    'disable_duet': False,
                    'disable_comment': False,
                    'disable_stitch': False,
                },
                'source_info': {
                    'source': 'FILE_UPLOAD',
                    'video_size': size,
                    'chunk_size': size,
                    'total_chunk_count': 1
                }
            }
        )
        upload_url = init.json().get('data', {}).get('upload_url')
        if not upload_url:
            print(f"❌ TikTok init failed: {init.text}")
            return

        # Upload file
        with open(video_path, 'rb') as f:
            r = requests.put(upload_url, data=f,
                headers={'Content-Type': 'video/mp4', 'Content-Length': str(size)})

        if r.status_code in [200, 201]:
            print("✅ TikTok upload success!")
        else:
            print(f"❌ TikTok upload failed: {r.text}")

    except Exception as e:
        print(f"❌ TikTok error: {e}")


def upload_video(video_path: str, title: str, niche: str, platform: str):
    """Route upload to the correct platform."""
    p = platform.lower().strip()
    print(f"  📤 Uploading to {p.upper()}...")
    if p == 'youtube':
        upload_youtube(video_path, title, niche)
    elif p == 'facebook':
        upload_facebook(video_path, title)
    elif p == 'tiktok':
        upload_tiktok(video_path, title)
    else:
        print(f"❌ Unknown platform: {platform}")
