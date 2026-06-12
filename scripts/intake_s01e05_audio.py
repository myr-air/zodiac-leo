import os
import shutil
import re

ep_id = "s01e05-apartment-window-longplay"
audio_dir = f"/Users/xiivth/workspaces/zodiac/leo/candidates/{ep_id}/audio"
selected_dir = os.path.join(audio_dir, "selected")
pool_dir = os.path.join(audio_dir, "pool")

# Map of standard title/filename to track index and slug
title_to_track = {
    "Corner Glow": (1, "corner-glow"),
    "Steam Rising": (2, "steam-rising"),
    "Reflections on Glass": (3, "reflections-on-glass"),
    "Gravel and Glow": (4, "gravel-and-glow"),
    "A Folded Corner": (5, "a-folded-corner"),
    "Deep Strings": (6, "deep-strings"),
    "Kitchen Timer": (7, "kitchen-timer"),
    "City Bokeh": (8, "city-bokeh"),
    "Shelved Spines": (9, "shelved-spines"),
    "Shadows on the Wall": (10, "shadows-on-the-wall"),
    "The Keys by the Door": (11, "the-keys-by-the-door"),
    "Warm Fabric": (12, "warm-fabric"),
    "Winding Down": (13, "winding-down")
}

def main():
    if not os.path.exists(audio_dir):
        print(f"Audio directory not found: {audio_dir}")
        return

    os.makedirs(selected_dir, exist_ok=True)
    os.makedirs(pool_dir, exist_ok=True)

    files = [f for f in os.listdir(audio_dir) if f.endswith(".wav") and os.path.isfile(os.path.join(audio_dir, f))]

    print(f"Found {len(files)} raw WAV files in candidate root.")
    
    moved_count = 0
    for filename in files:
        stem = os.path.splitext(filename)[0]
        # Match title and strip all trailing duplicate suffixes like " (1)", " (2)", " (1) (1)"
        clean_stem = stem
        while re.search(r"\s*\(\d+\)$", clean_stem):
            clean_stem = re.sub(r"\s*\(\d+\)$", "", clean_stem).strip()
        
        if clean_stem in title_to_track:
            track_num, slug = title_to_track[clean_stem]
            is_duplicate = (re.search(r"\(\d+\)$", stem) is not None) or (clean_stem != stem)
            
            src_path = os.path.join(audio_dir, filename)
            
            # If it is a duplicate suffix, or if the c01 target already exists in selected/
            c01_dest_path = os.path.join(selected_dir, f"aud-t{track_num:02d}_c01--{slug}.wav")
            if is_duplicate or os.path.exists(c01_dest_path):
                dest_name = f"aud-t{track_num:02d}_c02--{slug}.wav"
                dest_path = os.path.join(pool_dir, dest_name)
                dest_folder = "pool"
            else:
                dest_name = f"aud-t{track_num:02d}_c01--{slug}.wav"
                dest_path = os.path.join(selected_dir, dest_name)
                dest_folder = "selected"
                
            print(f"Moving: '{filename}' -> '{dest_folder}/{dest_name}'")
            shutil.move(src_path, dest_path)
            moved_count += 1
        else:
            print(f"Warning: file '{filename}' does not match any known track title.")

    print(f"\nSuccessfully organized {moved_count} files.")
    
    # Check what is missing in selected and pool
    selected_files = os.listdir(selected_dir) if os.path.exists(selected_dir) else []
    pool_files = os.listdir(pool_dir) if os.path.exists(pool_dir) else []
    
    missing_c01 = []
    missing_c02 = []
    
    for title, (track_num, slug) in title_to_track.items():
        # Check c01
        pattern_c01 = f"aud-t{track_num:02d}_c01"
        found_c01 = any(f.startswith(pattern_c01) for f in selected_files)
        if not found_c01:
            missing_c01.append((track_num, title))
            
        # Check c02
        pattern_c02 = f"aud-t{track_num:02d}_c02"
        found_c02 = any(f.startswith(pattern_c02) for f in pool_files)
        if not found_c02:
            missing_c02.append((track_num, title))
            
    if missing_c01:
        print("\n[!] MISSING SELECTED TRACKS (c01):")
        for num, title in sorted(missing_c01):
            print(f"  Track {num:02d}: {title}")
    else:
        print("\nAll 13 selected tracks (c01) are present!")
        
    if missing_c02:
        print("\n[!] MISSING POOL TRACKS (c02):")
        for num, title in sorted(missing_c02):
            print(f"  Track {num:02d}: {title}")
    else:
        print("\nAll 13 pool tracks (c02) are present!")

if __name__ == "__main__":
    main()
