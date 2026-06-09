import os
import re
import json

def parse_track_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract Title
    title_match = re.search(r'\*\*Song Title:\*\*?\s*(.*)', content)
    title = title_match.group(1).strip() if title_match else ""
    if not title:
        # Fallback to header
        header_match = re.search(r'#\s+S\d+E\d+\s+Track\s+\d+\s+Suno\s+Source\s+Pack\s+—\s+(.*)', content)
        title = header_match.group(1).strip() if header_match else ""
    if not title:
        # Another fallback
        header_match_generic = re.search(r'#\s+.*Track\s+\d+\s+—\s+(.*)', content)
        title = header_match_generic.group(1).strip() if header_match_generic else "Unknown Title"

    # Extract Styles
    styles_match = re.search(r'\*\*Styles:\*\*?\s*(.*)', content)
    styles = styles_match.group(1).strip() if styles_match else ""

    # Extract Exclude Styles
    exclude_match = re.search(r'\*\*Exclude Styles:\*\*?\s*(.*)', content)
    exclude = exclude_match.group(1).strip() if exclude_match else ""

    # Extract Weirdness
    weirdness_match = re.search(r'\*\*Weirdness:\*\*?\s*(\d+%)', content)
    weirdness = weirdness_match.group(1).strip() if weirdness_match else "12%"

    # Extract Style Influence
    influence_match = re.search(r'\*\*Style Influence:\*\*?\s*(\d+%)', content)
    influence = influence_match.group(1).strip() if influence_match else "82%"

    # Extract Lyrics
    lyrics = ""
    lyrics_block_match = re.search(r'\*\*Lyrics:\*\*?\s*\n*\n*```(?:text)?\n([\s\S]*?)```', content)
    if lyrics_block_match:
        lyrics = lyrics_block_match.group(1).strip()
    else:
        lyrics_section = re.search(r'\*\*Lyrics:\*\*?\s*\n([\s\S]*?)(?=\*\*|$)', content)
        if lyrics_section:
            lyrics = lyrics_section.group(1).strip()

    # Determine BPM from Styles
    bpm_match = re.search(r'(\d+)\s*BPM', styles, re.IGNORECASE)
    bpm = bpm_match.group(1) if bpm_match else "84"

    return {
        "title": title,
        "styles": styles,
        "exclude": exclude,
        "lyrics": lyrics,
        "weirdness": weirdness,
        "influence": influence,
        "bpm": bpm
    }

def main():
    episodes_dir = "/Users/xiivth/workspaces/zodiac/leo/channel/episodes"
    output_path = "/Users/xiivth/workspaces/zodiac/leo/scripts/suno-copilot-extension/tracks.json"

    if not os.path.exists(episodes_dir):
        print(f"Episodes directory not found: {episodes_dir}")
        return

    compiled_data = {}

    for ep_id in sorted(os.listdir(episodes_dir)):
        ep_path = os.path.join(episodes_dir, ep_id)
        if not os.path.isdir(ep_path):
            continue

        manifest_path = os.path.join(ep_path, "manifest.json")
        working_title = ep_id.replace("-longplay", "").replace("-", " ").title()
        if os.path.exists(manifest_path):
            try:
                with open(manifest_path, 'r', encoding='utf-8') as mf:
                    manifest = json.load(mf)
                    working_title = manifest.get("working_longplay", working_title)
                    # Clean "Longplay" suffix if present
                    if working_title.lower().endswith("longplay"):
                        working_title = working_title[:-8].strip()
            except Exception as e:
                print(f"Error parsing manifest for {ep_id}: {e}")

        # Format human name like: "S01E03: Rooftop Golden Hour"
        match = re.match(r's(\d+)e(\d+)', ep_id)
        if match:
            season = match.group(1)
            episode = match.group(2)
            pretty_name = f"S{season}E{episode}: {working_title}"
        else:
            pretty_name = working_title

        tracks_dir = os.path.join(ep_path, "source", "suno-tracks")
        if not os.path.exists(tracks_dir):
            print(f"No suno-tracks folder in {ep_id}, skipping.")
            continue

        tracks = {}
        for filename in sorted(os.listdir(tracks_dir)):
            if filename.endswith(".md"):
                num_match = re.match(r'(\d+)', filename)
                if num_match:
                    track_num = int(num_match.group(1))
                    file_path = os.path.join(tracks_dir, filename)
                    track_data = parse_track_file(file_path)
                    tracks[str(track_num)] = track_data

        if tracks:
            print(f"Parsed {len(tracks)} tracks for {pretty_name}")
            compiled_data[ep_id] = {
                "name": pretty_name,
                "tracks": tracks
            }

    # Write out JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(compiled_data, f, indent=2, ensure_ascii=False)
    print(f"Successfully compiled {len(compiled_data)} episodes to {output_path}")

if __name__ == "__main__":
    main()
