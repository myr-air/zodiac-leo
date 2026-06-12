#!/usr/bin/env python3
"""Automated script to delete old Thai caption tracks and upload updated ones across all 5 Mellow Longplay episodes."""
from __future__ import annotations
import sys
from pathlib import Path

# Add scripts directory to path to import helpers
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import youtube_api_video_upload as v

SECRETS = Path("/Users/xiivth/.config/mellow-longplay/.secret/google-oauth-client-desktop.json")
TOKEN = Path("/Users/xiivth/.config/mellow-longplay/.secret/youtube-token.json")
EXPECTED_CHANNEL_ID = "UC4qQwe3oiykEGhL_WyVFtMg"

EPISODES = [
    {"id": "s01e01-campus-cafe-longplay", "video_id": "4pOLXPMQO5g"},
    {"id": "s01e02-classroom-window-longplay", "video_id": "KZNjs0Z7-Pw"},
    {"id": "s01e03-rooftop-golden-hour-longplay", "video_id": "2P6fPs7NB0E"},
    {"id": "s01e04-bookstore-afternoon-longplay", "video_id": "OMjvEEAIFSU"},
    {"id": "s01e05-apartment-window-longplay", "video_id": "ShWN-wK-ZNY"},
]

def main() -> None:
    youtube, modules = v.get_authenticated_service(SECRETS, TOKEN)
    actual_channel_id = v.authenticated_channel_id(youtube)
    v.assert_expected_channel(actual_channel_id=actual_channel_id, expected_channel_id=EXPECTED_CHANNEL_ID)
    
    for ep in EPISODES:
        ep_id = ep["id"]
        video_id = ep["video_id"]
        srt_path = PROJECT_ROOT / "channel/episodes" / ep_id / "subtitles" / f"{ep_id}.th.srt"
        
        if not srt_path.is_file():
            print(f"[{ep_id}] Subtitle file not found: {srt_path.name}")
            continue
            
        print(f"\n--- Processing {ep_id} (Video ID: {video_id}) ---")
        
        # 1. List current captions
        response = youtube.captions().list(part="snippet", videoId=video_id).execute()
        existing_th_id = None
        for item in response.get("items", []):
            if item["snippet"]["language"] == "th" and item["snippet"]["name"] == "Thai (Cozy Translation)":
                existing_th_id = item["id"]
                break
            # Fallback if name is empty or different but language is Thai
            if item["snippet"]["language"] == "th" and not existing_th_id:
                existing_th_id = item["id"]
                
        # 2. Delete old track if found
        if existing_th_id:
            print(f"Deleting existing Thai caption track: {existing_th_id}")
            youtube.captions().delete(id=existing_th_id).execute()
            print("Successfully deleted old track.")
        else:
            print("No existing Thai caption track found.")
            
        # 3. Upload new track
        print(f"Uploading new spoken Thai caption track: {srt_path.name}")
        media = modules["MediaFileUpload"](
            str(srt_path),
            mimetype="*/*",
            chunksize=-1,
            resumable=True
        )
        
        up_response = youtube.captions().insert(
            part="snippet",
            body={
                "snippet": {
                    "videoId": video_id,
                    "language": "th",
                    "name": "Thai (Cozy Translation)",
                    "isDraft": False
                }
            },
            media_body=media
        ).execute()
        
        print(f"Successfully uploaded: Caption ID = {up_response['id']} (status = {up_response['snippet']['status']})")

if __name__ == "__main__":
    main()
