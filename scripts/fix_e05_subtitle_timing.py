#!/usr/bin/env python3
"""Fix EP5 subtitles in-place:
1. Remove (Humming low) / (ฮัมเพลงเสียงต่ำ) from EN and TH SRT/VTT
2. Patch track-01 Outro timing in EN SRT/VTT (cues that were severely off)
   using corrected timings from the new stable-ts re-alignment

Run: bash scripts/dev-python.sh scripts/fix_e05_subtitle_timing.py
Local-only. Does not upload or call any provider APIs.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
EPISODE_ID = "s01e05-apartment-window-longplay"
SUBTITLE_DIR = PROJECT_ROOT / "channel/episodes" / EPISODE_ID / "subtitles"

HUMMING_EN = "(Humming low)"
HUMMING_TH = "(ฮัมเพลงเสียงต่ำ)"

# Corrected track-01 timings from the new stable-ts re-alignment (s01e05.json).
# Maps (old_text) -> (new_start_sec, new_end_sec)
# Track-01 is at offset 0.0 in the longplay.
# Only the cues that changed significantly are listed here.
# (Cues not in this dict are kept as-is after humming removal.)
TRACK01_TIMING_CORRECTIONS = {
    "While the city voices slip away": (183.740, 188.840),
    "Steady shade of orange-gold": (189.840, 195.180),
    "Resting on the wooden tray": (196.880, 200.980),
    # Verse 3 - was missing from original, not in correction scope since
    # they were placed after Instrumental Break correctly in old alignment.
    # But these Outro cues were severely wrong (47s+ durations), so fix them.
}

# Also these were off (cue 17 was 20.7s, conf=0.066):
# "While the city voices slip away" old: 118.96 -> 139.64 (wrong), new: 183.74 -> 188.84


def srt_to_seconds(ts: str) -> float:
    ts = ts.replace(",", ".")
    h, m, rest = ts.split(":")
    s, ms = rest.split(".")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0


def seconds_to_srt(s: float) -> str:
    ms = round((s % 1) * 1000)
    total_s = int(s)
    h = total_s // 3600
    m = (total_s % 3600) // 60
    sec = total_s % 60
    return f"{h:02d}:{m:02d}:{sec:02d},{ms:03d}"


def seconds_to_vtt(s: float) -> str:
    return seconds_to_srt(s).replace(",", ".")


def parse_srt_blocks(content: str) -> list[dict]:
    """Parse SRT content into list of block dicts."""
    blocks = re.split(r"\r?\n\r?\n", content.strip())
    result = []
    for block in blocks:
        lines = block.strip().splitlines()
        if len(lines) < 3:
            continue
        try:
            idx = int(lines[0].strip())
        except ValueError:
            continue
        ts_match = re.match(r"(.+?)\s+-->\s+(.+)", lines[1])
        if not ts_match:
            continue
        result.append({
            "index": idx,
            "start_str": ts_match.group(1).strip(),
            "end_str": ts_match.group(2).strip(),
            "text": "\n".join(lines[2:]),
        })
    return result


def serialize_srt(blocks: list[dict]) -> str:
    parts = []
    for i, b in enumerate(blocks, 1):
        parts.append(f"{i}\n{b['start_str']} --> {b['end_str']}\n{b['text']}")
    return "\n\n".join(parts) + "\n"


# ─────────────────────────────────────────────────────────────────────────────

def fix_en_srt() -> None:
    path = SUBTITLE_DIR / f"{EPISODE_ID}.en.srt"
    print(f"\nFixing: {path.name}")
    blocks = parse_srt_blocks(path.read_text(encoding="utf-8"))
    out = []
    removed = 0
    patched = 0
    for b in blocks:
        text = b["text"].strip()
        # Remove humming cue
        if text == HUMMING_EN:
            print(f"  Removed: [{b['index']}] {repr(text)}")
            removed += 1
            continue
        # Patch timing corrections
        if text in TRACK01_TIMING_CORRECTIONS:
            new_s, new_e = TRACK01_TIMING_CORRECTIONS[text]
            old_start = b["start_str"]
            old_end = b["end_str"]
            b["start_str"] = seconds_to_srt(new_s)
            b["end_str"] = seconds_to_srt(new_e)
            print(f"  Patched: [{b['index']}] {repr(text[:40])}")
            print(f"    old: {old_start} --> {old_end}")
            print(f"    new: {b['start_str']} --> {b['end_str']}")
            patched += 1
        out.append(b)
    result = serialize_srt(out)
    path.write_text(result, encoding="utf-8")
    print(f"  Done: removed={removed}, patched={patched}, total cues={len(out)}")


def fix_en_vtt() -> None:
    srt_path = SUBTITLE_DIR / f"{EPISODE_ID}.en.srt"
    vtt_path = SUBTITLE_DIR / f"{EPISODE_ID}.en.vtt"
    print(f"\nRebuilding: {vtt_path.name} from fixed SRT")

    # Read the fixed SRT and convert to VTT
    blocks = parse_srt_blocks(srt_path.read_text(encoding="utf-8"))
    lines = ["WEBVTT", ""]
    for i, b in enumerate(blocks, 1):
        start_vtt = b["start_str"].replace(",", ".")
        end_vtt = b["end_str"].replace(",", ".")
        lines.append(str(i))
        lines.append(f"{start_vtt} --> {end_vtt}")
        lines.append(b["text"])
        lines.append("")
    vtt_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Done: {len(blocks)} cues")


def fix_th_srt() -> None:
    path = SUBTITLE_DIR / f"{EPISODE_ID}.th.srt"
    print(f"\nFixing: {path.name}")
    blocks = parse_srt_blocks(path.read_text(encoding="utf-8"))
    out = []
    removed = 0
    for b in blocks:
        text = b["text"].strip()
        if text == HUMMING_TH:
            print(f"  Removed: [{b['index']}] {repr(text)}")
            removed += 1
            continue
        out.append(b)
    result = serialize_srt(out)
    path.write_text(result, encoding="utf-8")
    print(f"  Done: removed={removed}, total cues={len(out)}")


def fix_th_vtt() -> None:
    srt_path = SUBTITLE_DIR / f"{EPISODE_ID}.th.srt"
    vtt_path = SUBTITLE_DIR / f"{EPISODE_ID}.th.vtt"
    print(f"\nRebuilding: {vtt_path.name} from fixed TH SRT")

    blocks = parse_srt_blocks(srt_path.read_text(encoding="utf-8"))
    lines = ["WEBVTT", ""]
    for i, b in enumerate(blocks, 1):
        start_vtt = b["start_str"].replace(",", ".")
        end_vtt = b["end_str"].replace(",", ".")
        lines.append(str(i))
        lines.append(f"{start_vtt} --> {end_vtt}")
        lines.append(b["text"])
        lines.append("")
    vtt_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Done: {len(blocks)} cues")


def verify_no_humming() -> None:
    print("\nVerification: checking for remaining humming cues...")
    for fname in [
        f"{EPISODE_ID}.en.srt",
        f"{EPISODE_ID}.en.vtt",
        f"{EPISODE_ID}.th.srt",
        f"{EPISODE_ID}.th.vtt",
    ]:
        p = SUBTITLE_DIR / fname
        content = p.read_text(encoding="utf-8")
        found = HUMMING_EN in content or HUMMING_TH in content
        status = "FAIL - humming still present!" if found else "OK"
        print(f"  {fname}: {status}")


def verify_timing_patch() -> None:
    print("\nVerification: checking patched timing in EN SRT...")
    path = SUBTITLE_DIR / f"{EPISODE_ID}.en.srt"
    blocks = parse_srt_blocks(path.read_text(encoding="utf-8"))
    for b in blocks:
        if b["text"].strip() in TRACK01_TIMING_CORRECTIONS:
            new_s, new_e = TRACK01_TIMING_CORRECTIONS[b["text"].strip()]
            actual_s = srt_to_seconds(b["start_str"])
            actual_e = srt_to_seconds(b["end_str"])
            ok = abs(actual_s - new_s) < 0.01 and abs(actual_e - new_e) < 0.01
            status = "OK" if ok else f"MISMATCH (expected {new_s:.3f}→{new_e:.3f})"
            print(f"  {repr(b['text'][:40])}: {b['start_str']} --> {b['end_str']} [{status}]")


def main() -> None:
    print("=" * 70)
    print("EP5 Subtitle Fix")
    print("=" * 70)

    fix_en_srt()
    fix_en_vtt()
    fix_th_srt()
    fix_th_vtt()

    verify_no_humming()
    verify_timing_patch()

    print("\nAll done. Run bash scripts/verify-standalone.sh to validate.")


if __name__ == "__main__":
    main()
