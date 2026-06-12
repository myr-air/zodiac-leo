#!/usr/bin/env python3
"""Replace incorrect singular first-person pronouns (เรา/ของเรา) with feminine ones (ฉัน/ของฉัน) in EP5 Thai subtitles."""
from __future__ import annotations
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
EPISODE_ID = "s01e05-apartment-window-longplay"
SUBTITLE_DIR = PROJECT_ROOT / "channel/episodes" / EPISODE_ID / "subtitles"

REPLACEMENTS = [
    ("ความเงียบสงบยังคงอยู่ โดยที่เราเองก็ไม่รู้ว่าเพราะอะไร", "ความเงียบสงบยังคงอยู่ โดยที่ฉันเองก็ไม่รู้ว่าเพราะอะไร"),
    ("เรามองเห็นเธอยืนอยู่ใกล้ๆ", "ฉันมองเห็นเธอยืนอยู่ใกล้ๆ"),
    ("บรรจุสิ่งที่เราเก็บรักษาเอาไว้ให้เธอ", "บรรจุสิ่งที่ฉันเก็บรักษาเอาไว้ให้เธอ"),
    ("เราจะวางหนังสือเล่มนี้ให้อยู่ในสายตา", "ฉันจะวางหนังสือเล่มนี้ให้อยู่ในสายตา"),
    ("สำหรับเรื่องราวในใจของเธอกับเรา", "สำหรับเรื่องราวในใจของเธอกับฉัน"),
    ("ถักทอเข้าด้วยกันระหว่างเรื่องของเธอกับเรา", "ถักทอเข้าด้วยกันระหว่างเรื่องของเธอกับฉัน"),
    ("เราสัมผัสได้ถึงเรื่องราวในอดีต", "ฉันสัมผัสได้ถึงเรื่องราวในอดีต"),
    ("สำหรับความรู้สึกในใจของเธอกับเรา", "สำหรับความรู้สึกในใจของเธอกับฉัน"),
    ("ลงบนผนังห้องนอนห้องนี้ของเรา", "ลงบนผนังห้องนอนห้องนี้ของฉัน"),
]

def fix_file(path: Path) -> None:
    if not path.is_file():
        print(f"File not found: {path}")
        return
    
    content = path.read_text(encoding="utf-8")
    original = content
    
    for old, new in REPLACEMENTS:
        content = content.replace(old, new)
    
    if content == original:
        print(f"No changes made to {path.name} (already updated or no matches found).")
    else:
        path.write_text(content, encoding="utf-8")
        print(f"Successfully updated {path.name}")

def main() -> None:
    srt_path = SUBTITLE_DIR / f"{EPISODE_ID}.th.srt"
    vtt_path = SUBTITLE_DIR / f"{EPISODE_ID}.th.vtt"
    
    fix_file(srt_path)
    fix_file(vtt_path)

if __name__ == "__main__":
    main()
