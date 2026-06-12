#!/usr/bin/env python3
"""Programmatic replacement of singular first-person pronouns (เรา/ของเรา) with feminine ones (ฉัน/ของฉัน) across all 5 Mellow Longplay episodes."""
from __future__ import annotations
import os
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BASE_DIR = PROJECT_ROOT / "channel/episodes"
EPISODES = [
    "s01e01-campus-cafe-longplay",
    "s01e02-classroom-window-longplay",
    "s01e03-rooftop-golden-hour-longplay",
    "s01e04-bookstore-afternoon-longplay",
    "s01e05-apartment-window-longplay",
]

def parse_srt(path: Path) -> list[dict[str, str]]:
    cues = []
    if not path.is_file():
        return cues
    content = path.read_text(encoding="utf-8").strip()
    blocks = content.split("\n\n")
    for block in blocks:
        lines = block.split("\n")
        if len(lines) >= 3:
            num = lines[0]
            time = lines[1]
            text = "\n".join(lines[2:])
            cues.append({"num": num, "time": time, "text": text})
    return cues

def serialize_srt(cues: list[dict[str, str]]) -> str:
    parts = []
    for cue in cues:
        parts.append(f"{cue['num']}\n{cue['time']}\n{cue['text']}")
    return "\n\n".join(parts) + "\n"

def parse_vtt(path: Path) -> tuple[str, list[dict[str, str]]]:
    cues = []
    header = "WEBVTT\n\n"
    if not path.is_file():
        return header, cues
    content = path.read_text(encoding="utf-8").strip()
    
    # Check for WEBVTT header
    if content.startswith("WEBVTT"):
        parts = re.split(r"\n\n", content, 1)
        if len(parts) == 2:
            header = parts[0] + "\n\n"
            content = parts[1]
    
    blocks = content.split("\n\n")
    for block in blocks:
        lines = block.split("\n")
        if len(lines) >= 2:
            # VTT doesn't always have a cue number, check if the first line is a timestamp
            if "-->" in lines[0]:
                num = ""
                time = lines[0]
                text = "\n".join(lines[1:])
            elif len(lines) >= 3 and "-->" in lines[1]:
                num = lines[0]
                time = lines[1]
                text = "\n".join(lines[2:])
            else:
                continue
            cues.append({"num": num, "time": time, "text": text})
    return header, cues

def serialize_vtt(header: str, cues: list[dict[str, str]]) -> str:
    parts = []
    for cue in cues:
        if cue["num"]:
            parts.append(f"{cue['num']}\n{cue['time']}\n{cue['text']}")
        else:
            parts.append(f"{cue['time']}\n{cue['text']}")
    return header + "\n\n".join(parts) + "\n"

def correct_pronouns(en_text: str, th_text: str) -> str:
    en_lower = en_text.lower()
    has_singular = any(re.search(r"\b" + p + r"\b", en_lower) for p in ["i", "my", "me", "mine", "myself"])
    has_plural = any(re.search(r"\b" + p + r"\b", en_lower) for p in ["we", "us", "our", "ours", "ourselves"])
    
    # We only correct if English has singular pronouns and does not have plural pronouns
    if has_singular and not has_plural:
        new_th = th_text
        # Replace 'ของเรา' with 'ของฉัน' (avoiding 'เราสองคน', etc.)
        new_th = re.sub(r"ของเรา(?!สองคน|พวกนี้|ทุกคน|ทั้งคู่)", "ของฉัน", new_th)
        # Replace 'เรา' with 'ฉัน' (avoiding 'พวกเรา', 'เราสองคน', 'เราทั้งคู่', 'เราก็', etc. where we is implied, and avoiding 'เราะ')
        new_th = re.sub(r"(?<!พวก)เรา(?!สองคน|พวกนี้|ทุกคน|ทั้งคู่|กัน|ะ)", "ฉัน", new_th)
        return new_th
    return th_text

def get_start_time(time_str: str) -> float:
    # time_str is like "00:15:16,160 --> 00:15:18,900"
    start_part = time_str.split(" --> ")[0]
    start_part = start_part.replace(",", ".")
    parts = start_part.split(":")
    if len(parts) == 3:
        h, m, s = parts
        return float(h) * 3600 + float(m) * 60 + float(s)
    return 0.0

def find_matching_cue(th_cue: dict[str, str], en_cues: list[dict[str, str]]) -> dict[str, str] | None:
    th_start = get_start_time(th_cue["time"])
    best_match = None
    min_diff = 2.0  # threshold of 2 seconds
    for en_cue in en_cues:
        en_start = get_start_time(en_cue["time"])
        diff = abs(th_start - en_start)
        if diff < min_diff:
            min_diff = diff
            best_match = en_cue
    return best_match

def process_episode(episode_id: str) -> None:
    sub_dir = BASE_DIR / episode_id / "subtitles"
    th_srt_path = sub_dir / f"{episode_id}.th.srt"
    en_srt_path = sub_dir / f"{episode_id}.en.srt"
    th_vtt_path = sub_dir / f"{episode_id}.th.vtt"
    en_vtt_path = sub_dir / f"{episode_id}.en.vtt"
    
    if not th_srt_path.is_file() or not en_srt_path.is_file():
        print(f"Skipping {episode_id}: missing SRT files")
        return
        
    th_srt_cues = parse_srt(th_srt_path)
    en_srt_cues = parse_srt(en_srt_path)
    
    srt_changes = 0
    for th_cue in th_srt_cues:
        matching_en = find_matching_cue(th_cue, en_srt_cues)
        if matching_en:
            orig_text = th_cue["text"]
            new_text = correct_pronouns(matching_en["text"], orig_text)
            if new_text != orig_text:
                th_cue["text"] = new_text
                srt_changes += 1
            
    if srt_changes > 0:
        th_srt_path.write_text(serialize_srt(th_srt_cues), encoding="utf-8")
        print(f"{episode_id} SRT: applied {srt_changes} pronoun fixes")
        
    # Apply to VTT too
    if th_vtt_path.is_file() and en_vtt_path.is_file():
        th_header, th_vtt_cues = parse_vtt(th_vtt_path)
        _, en_vtt_cues = parse_vtt(en_vtt_path)
        
        vtt_changes = 0
        for th_cue in th_vtt_cues:
            matching_en = find_matching_cue(th_cue, en_vtt_cues)
            if matching_en:
                orig_text = th_cue["text"]
                new_text = correct_pronouns(matching_en["text"], orig_text)
                if new_text != orig_text:
                    th_cue["text"] = new_text
                    vtt_changes += 1
                
        if vtt_changes > 0:
            th_vtt_path.write_text(serialize_vtt(th_header, th_vtt_cues), encoding="utf-8")
            print(f"{episode_id} VTT: applied {vtt_changes} pronoun fixes")

def main() -> None:
    for ep in EPISODES:
        process_episode(ep)

if __name__ == "__main__":
    main()
