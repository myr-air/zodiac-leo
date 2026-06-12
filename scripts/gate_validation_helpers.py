#!/usr/bin/env python3
"""Shared gate validation helpers for audio silence detection and subtitle alignment timing checks."""

import os
import re
import sys
import json
import wave
import subprocess
from pathlib import Path

def run_audio_silence_check(episode_id: str, workspace_root: Path = Path(".")) -> list[str]:
    """Scan all selected and pool audio files for silence glitches using ffmpeg."""
    errors = []
    candidate_dir = workspace_root / "candidates" / episode_id / "audio"
    if not candidate_dir.exists():
        return [f"Audio candidate directory does not exist: {candidate_dir}"]

    # We want to scan all .wav files in both selected/ and pool/
    audio_files = sorted(list(candidate_dir.glob("selected/*.wav")) + list(candidate_dir.glob("pool/*.wav")))
    if not audio_files:
        return [f"No wav files found under {candidate_dir}"]

    for path in audio_files:
        try:
            # First, check duration via wave
            with wave.open(str(path), "rb") as wav:
                duration = wav.getnframes() / wav.getframerate()
        except Exception as exc:
            errors.append(f"Failed to read WAV header for {path.name}: {exc}")
            continue

        # Run ffmpeg silencedetect
        cmd = [
            "ffmpeg",
            "-i", str(path),
            "-af", "silencedetect=noise=-50dB:d=5",
            "-f", "null",
            "-"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        # Parse stderr for silence alerts
        for line in res.stderr.splitlines():
            if "silencedetect" in line and "silence_duration" in line:
                # Format: [Parsed_silencedetect_0 @ 0x...] silence_end: 415.216917 | silence_duration: 197.641
                match_dur = re.search(r"silence_duration:\s*([\d\.]+)", line)
                match_start = re.search(r"silence_start:\s*([\d\.]+)", line)
                if match_dur:
                    dur_val = float(match_dur.group(1))
                    start_val = float(match_start.group(1)) if match_start else 0.0
                    if dur_val >= 5.0:
                        errors.append(
                            f"Silence glitch detected in {path.relative_to(workspace_root)}: "
                            f"silent gap of {dur_val:.2f}s starting at {start_val:.2f}s (duration: {duration:.2f}s)"
                        )
    return errors

def parse_srt_time(value: str) -> float:
    match = re.fullmatch(r"(\d{2}):(\d{2}):(\d{2})[,\.](\d{3})", value.strip())
    if not match:
        raise ValueError(f"invalid SRT timestamp: {value!r}")
    hours, minutes, seconds, millis = map(int, match.groups())
    return hours * 3600 + minutes * 60 + seconds + millis / 1000.0

def parse_srt_cues(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8-sig")
    cues = []
    # Split by double newline or similar spacing
    for block in re.split(r"\n\s*\n", text.strip()):
        lines = [line.rstrip() for line in block.splitlines() if line.strip()]
        if len(lines) < 3:
            continue
        timing = lines[1]
        if "-->" not in timing:
            continue
        start_text, end_text = [part.strip() for part in timing.split("-->", 1)]
        try:
            start_sec = parse_srt_time(start_text)
            end_sec = parse_srt_time(end_text)
        except Exception as exc:
            raise ValueError(f"Failed to parse timing block {timing} in {path.name}: {exc}")
        cues.append({
            "start": start_sec,
            "end": end_sec,
            "text": "\n".join(lines[2:])
        })
    return cues

def normalize_text_simple(text: str) -> str:
    # Remove punctuation and whitespace for comparison
    return re.sub(r"[^\w]+", "", text.lower())

def run_subtitle_alignment_check(episode_id: str, workspace_root: Path = Path(".")) -> list[str]:
    """Check if the absolute timings of the promoted SRT files match the selected audio timeline and track alignment JSONs."""
    errors = []
    subtitles_dir = workspace_root / "channel" / "episodes" / episode_id / "subtitles"
    if not subtitles_dir.is_dir():
        return []

    srt_files = list(subtitles_dir.glob(f"{episode_id}.*.srt"))
    if not srt_files:
        # Fallback to check default en.srt
        default_srt = subtitles_dir / f"{episode_id}.en.srt"
        if default_srt.is_file():
            srt_files = [default_srt]
        else:
            return []

    # Get selected audio files to calculate expected timeline
    selected_dir = workspace_root / "candidates" / episode_id / "audio" / "selected"
    if not selected_dir.is_dir():
        return [f"Selected audio directory does not exist: {selected_dir}"]

    audio_files = sorted(list(selected_dir.glob("aud-t*.wav")))
    if not audio_files:
        return [f"No selected audio files found under {selected_dir}"]

    # Parse tracks and calculate timeline
    timeline = []
    current_time = 0.0
    gap_seconds = 1.0 # default gap is 1.0s

    for path in audio_files:
        match = re.search(r"aud-t(\d{2})", path.name)
        if not match:
            errors.append(f"Filename does not match pattern aud-tXX: {path.name}")
            continue
        track_num = int(match.group(1))
        try:
            with wave.open(str(path), "rb") as wav:
                dur = wav.getnframes() / wav.getframerate()
        except Exception as exc:
            errors.append(f"Failed to read WAV duration for {path.name}: {exc}")
            continue
        start = current_time
        end = start + dur
        timeline.append({
            "track_number": track_num,
            "start": round(start, 3),
            "end": round(end, 3),
            "duration": round(dur, 3),
            "path": path
        })
        current_time = end + gap_seconds

    for srt_path in srt_files:
        # Parse SRT file
        try:
            srt_cues = parse_srt_cues(srt_path)
        except Exception as exc:
            errors.append(f"Failed to parse promoted SRT {srt_path.name}: {exc}")
            continue

        if not srt_cues:
            errors.append(f"Promoted SRT file is empty: {srt_path.name}")
            continue

        # Group SRT cues by timeline slot window
        srt_cues_by_track = {t["track_number"]: [] for t in timeline}
        for cue in srt_cues:
            assigned = False
            for t in timeline:
                # Check if cue overlaps with this track's window.
                # Allow a tiny margin of 0.05 seconds for edge cases.
                if cue["start"] >= t["start"] - 0.05 and cue["end"] <= t["end"] + 0.05:
                    srt_cues_by_track[t["track_number"]].append(cue)
                    assigned = True
                    break
            if not assigned:
                errors.append(
                    f"[{srt_path.name}] SRT cue leaks outside any track window or lands in a gap: "
                    f"{cue['start']:.3f}s -> {cue['end']:.3f}s: {cue['text']!r}"
                )

        # Verify each track's assigned cues against the original alignment JSON
        align_pack_dir = workspace_root / "candidates" / episode_id / "subtitles" / "proofs" / "longplay" / "align-pack"
        for t in timeline:
            track_num = t["track_number"]
            track_srt_cues = srt_cues_by_track[track_num]

            is_english = srt_path.name.endswith(".en.srt")

            # Find alignment JSON
            json_pattern = f"track-{track_num:02d}/*-track-{track_num:02d}-subtitle-alignment-draft-01.json"
            json_matches = list(align_pack_dir.glob(json_pattern))
            if not json_matches:
                # Fallback to no-draft-01 suffix
                json_pattern_alt = f"track-{track_num:02d}/*-track-{track_num:02d}-subtitle-alignment.json"
                json_matches = list(align_pack_dir.glob(json_pattern_alt))

            if not json_matches:
                # If no JSON exists, we can't verify individual cues but we know SRT cues exist
                continue

            json_path = json_matches[0]
            try:
                json_data = json.loads(json_path.read_text(encoding="utf-8"))
            except Exception as exc:
                errors.append(f"Failed to read local alignment JSON {json_path.name}: {exc}")
                continue

            # Get display cues or cues
            local_cues = json_data.get("display_cues")
            if local_cues is None:
                local_cues = json_data.get("raw_cues")
            if local_cues is None:
                local_cues = json_data.get("cues") or []

            if is_english and len(track_srt_cues) != len(local_cues):
                errors.append(
                    f"[{srt_path.name}] Track {track_num:02d} subtitle cue count mismatch: "
                    f"promoted SRT has {len(track_srt_cues)} cues, but local alignment JSON has {len(local_cues)} cues. "
                    f"Subtitle timings are out-of-sync! Did you swap a song candidate without re-promoting sidecars?"
                )
                continue

            # Compare each cue's time shifted to absolute timeline
            for idx, (srt_cue, local_cue) in enumerate(zip(track_srt_cues, local_cues)):
                expected_start = t["start"] + float(local_cue["start"])
                expected_end = t["start"] + float(local_cue["end"])

                # Verify time matches (with 0.05s tolerance)
                start_diff = abs(srt_cue["start"] - expected_start)
                end_diff = abs(srt_cue["end"] - expected_end)

                if start_diff > 0.05 or end_diff > 0.05:
                    errors.append(
                        f"[{srt_path.name}] Track {track_num:02d} subtitle timing misalignment at cue {idx+1}: "
                        f"promoted SRT cue has {srt_cue['start']:.3f}s -> {srt_cue['end']:.3f}s, "
                        f"but expected {expected_start:.3f}s -> {expected_end:.3f}s (based on track start {t['start']:.3f}s and local cue). "
                        f"Text: {srt_cue['text']!r}. Subtitle timings are out-of-sync! Did you swap a song candidate without re-promoting sidecars?"
                    )
                    break # Show only first mismatch per track to keep output clean

                # Optional: Verify text matches roughly (only for English)
                if is_english:
                    srt_norm = normalize_text_simple(srt_cue["text"])
                    local_norm = normalize_text_simple(local_cue["text"])
                    if srt_norm != local_norm:
                        # Text mismatch (allow if minor, but warn/error if completely different)
                        if len(srt_norm) > 0 and len(local_norm) > 0:
                            errors.append(
                                f"[{srt_path.name}] Track {track_num:02d} subtitle text mismatch at cue {idx+1}: "
                                f"promoted SRT has {srt_cue['text']!r}, local JSON has {local_cue['text']!r}"
                            )
                            break

    return errors

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 gate_validation_helpers.py [audio|subtitle] [episode_id]")
        sys.exit(1)
    mode = sys.argv[1]
    ep_id = sys.argv[2]
    if mode == "audio":
        errs = run_audio_silence_check(ep_id)
    elif mode == "subtitle":
        errs = run_subtitle_alignment_check(ep_id)
    else:
        print(f"Unknown mode: {mode}")
        sys.exit(1)

    if errs:
        for err in errs:
            print(f"FAIL: {err}", file=sys.stderr)
        sys.exit(1)
    else:
        print("PASS")
        sys.exit(0)
