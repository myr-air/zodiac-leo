import asyncio
import json
import os
import subprocess
import shutil
import sys

# Configs
HOST = "localhost"
PORT = 8080
TRACKS_JSON = "/Users/xiivth/workspaces/zodiac/leo/scripts/suno-copilot-extension/tracks.json"
CANDIDATES_BASE = "/Users/xiivth/workspaces/zodiac/leo/candidates"
DOWNLOADS_DIR = os.path.expanduser("~/Downloads")
TRACKS_BUILD_SCRIPT = "/Users/xiivth/workspaces/zodiac/leo/scripts/suno-build-tracks.py"


def rebuild_tracks_database():
    """
    Regenerate tracks.json from channel/episodes before serving data.
    """
    if not os.path.exists(TRACKS_BUILD_SCRIPT):
        print(f"[Local OS Server] Build script not found: {TRACKS_BUILD_SCRIPT}")
        return

    try:
        result = subprocess.run(
            [sys.executable, TRACKS_BUILD_SCRIPT],
            check=False,
            capture_output=True,
            text=True,
            timeout=45
        )
        if result.returncode != 0:
            print("[Local OS Server] Track build script returned error:")
            if result.stderr:
                print(result.stderr.strip())
    except Exception as err:
        print(f"[Local OS Server] Failed to rebuild tracks.json: {err}")

# Load compiled tracks database
def load_tracks(rebuild=False):
    if rebuild:
        rebuild_tracks_database()

    if os.path.exists(TRACKS_JSON):
        with open(TRACKS_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# WebSocket Server Handler
async def handle_connection(websocket, path=None):
    print(f"\n[Local OS Server] Chrome Extension connected from {websocket.remote_address}!")

    try:
        tracks = load_tracks(rebuild=True)

        # 1. Inform client of connection success
        await websocket.send(json.dumps({
            "status": "connected",
            "message": "Local Mellow OS Server active and connected!",
            "totalEpisodes": len(tracks),
            "tracks": tracks
        }))

        # 2. Command listening loop
        async for message in websocket:
            data = json.loads(message)
            action = data.get("action")

            if action == "request_catalog":
                tracks = load_tracks(rebuild=True)
                await websocket.send(json.dumps({
                    "status": "catalog",
                    "message": "Track database refreshed",
                    "totalEpisodes": len(tracks),
                    "tracks": tracks
                }))

            if action == "request_track":
                episode_id = data.get("episodeId")
                track_id = str(data.get("trackId"))
                print(f"[Local OS Server] Client requested Track #{track_id} for Episode '{episode_id}'")

                # Reload tracks database in case it was recompiled while running
                tracks = load_tracks(rebuild=True)

                if episode_id in tracks and track_id in tracks[episode_id]["tracks"]:
                    track_data = tracks[episode_id]["tracks"][track_id]
                    # Send track details over WebSocket
                    await websocket.send(json.dumps({
                        "status": "inject_track",
                        "episodeId": episode_id,
                        "trackId": track_id,
                        "data": track_data
                    }))
                else:
                    tracks = load_tracks(rebuild=True)
                    if episode_id in tracks and track_id in tracks[episode_id]["tracks"]:
                        track_data = tracks[episode_id]["tracks"][track_id]
                        # Send track details over WebSocket
                        await websocket.send(json.dumps({
                            "status": "inject_track",
                            "episodeId": episode_id,
                            "trackId": track_id,
                            "data": track_data
                        }))
                        continue

                    await websocket.send(json.dumps({
                        "status": "error",
                        "message": f"Track #{track_id} for Episode {episode_id} not found in database."
                    }))

            elif action == "track_completed":
                episode_id = data.get("episodeId")
                track_id = data.get("trackId")
                title = data.get("title")
                print(f"[Local OS Server] 🎉 Track #{track_id} '{title}' of Episode '{episode_id}' successfully generated on Suno!")

                # Check Downloads folder in background
                asyncio.create_task(poll_and_move_downloaded_wav(title, episode_id))

            elif action == "batch_download_completed":
                episode_id = data.get("episodeId")
                title = data.get("title")
                print(f"[Local OS Server] 📥 Batch song download completed for '{title}' of Episode '{episode_id}'")

                # Check Downloads folder in background
                asyncio.create_task(poll_and_move_downloaded_wav(title, episode_id))

    except Exception as e:
        print(f"[Local OS Server] Connection error or client disconnected: {e}")

async def poll_and_move_downloaded_wav(song_title, episode_id, max_wait_sec=90):
    """
    Scans ~/Downloads for WAV files matching the song title.
    Polls every second for up to max_wait_sec WITHOUT early-return so
    both Suno variations (Title.wav and Title (1).wav) are both moved.
    """
    clean_title = "".join(c for c in song_title if c.isalnum() or c in "._- ").strip()

    candidates_dir = os.path.join(CANDIDATES_BASE, episode_id, "audio")
    os.makedirs(candidates_dir, exist_ok=True)

    print(f"[Local OS Server] Polling ~/Downloads for: '{clean_title}' WAVs (Max {max_wait_sec}s)...")

    moved_total = 0
    last_moved_at = None

    for attempt in range(max_wait_sec):
        moved_this_pass = 0

        for filename in os.listdir(DOWNLOADS_DIR):
            # Match files whose name contains the title and ends with .wav
            if clean_title.lower() in filename.lower() and filename.lower().endswith(".wav"):
                src_path = os.path.join(DOWNLOADS_DIR, filename)
                dst_path = os.path.join(candidates_dir, filename)

                # Skip if already moved to candidates
                if not os.path.exists(src_path):
                    continue

                # If destination already exists, generate a unique filename with a counter suffix (e.g. "Title (1).wav")
                if os.path.exists(dst_path):
                    base, ext = os.path.splitext(filename)
                    counter = 1
                    while True:
                        new_filename = f"{base} ({counter}){ext}"
                        new_dst_path = os.path.join(candidates_dir, new_filename)
                        if not os.path.exists(new_dst_path):
                            dst_path = new_dst_path
                            filename = new_filename
                            break
                        counter += 1

                try:
                    # Wait for file size to stabilise (browser still writing)
                    size1 = os.path.getsize(src_path)
                    await asyncio.sleep(0.4)
                    if not os.path.exists(src_path):
                        continue
                    size2 = os.path.getsize(src_path)
                    if size1 != size2:
                        # Still downloading — skip this pass, retry next second
                        continue

                    shutil.move(src_path, dst_path)
                    print(f"[Local OS Server] ✅ Moved '{filename}' → {candidates_dir}")
                    moved_total += 1
                    moved_this_pass += 1
                    last_moved_at = attempt

                except Exception as e:
                    print(f"[Local OS Server] ⚠️  Failed to move '{filename}': {e}")

        # After we've moved at least one file, wait a little longer for the second
        # variation to finish downloading, but don't exit early — keep polling.
        await asyncio.sleep(1.0)

    if moved_total > 0:
        print(f"[Local OS Server] Done — moved {moved_total} file(s) for '{clean_title}'.")
        return True

    print(f"[Local OS Server] Timeout: No WAV found for '{clean_title}' after {max_wait_sec}s.")
    return False


async def main():
    # We load websockets dynamically, or instruct user to install
    try:
        import websockets
    except ImportError:
        print("[Local OS Server] 'websockets' library missing. Please install it using:")
        print("bash scripts/dev-python.sh -m pip install websockets")
        return

    print(f"[Local OS Server] Starting WebSocket server on ws://{HOST}:{PORT}...")
    async with websockets.serve(handle_connection, HOST, PORT):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
