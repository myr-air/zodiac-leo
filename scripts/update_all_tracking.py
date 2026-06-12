#!/usr/bin/env python3
"""Append subtitle update records to the status.csv tracking files for EP1-EP4."""
from __future__ import annotations
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
EPISODES = [
    "s01e01-campus-cafe-longplay",
    "s01e02-classroom-window-longplay",
    "s01e03-rooftop-golden-hour-longplay",
    "s01e04-bookstore-afternoon-longplay",
]

def update_status_csv(ep_id: str) -> None:
    csv_path = PROJECT_ROOT / "channel/episodes" / ep_id / "tracking" / "status.csv"
    if not csv_path.is_file():
        print(f"[{ep_id}] status.csv not found: {csv_path}")
        return
        
    row = f'2026-06-12,{ep_id},post_release_subtitle_fix,subtitles,applied,channel/episodes/{ep_id}/subtitles/{ep_id}.th.srt,"Replaced incorrect \'เรา\'/\'ของเรา\' with feminine \'ฉัน\'/\'ของฉัน\' when referring to the singer individually, and rewrote to natural spoken style. Re-uploaded corrected Thai caption track to YouTube."\n'
    
    content = csv_path.read_text(encoding="utf-8")
    if not content.endswith("\n"):
        content += "\n"
        
    csv_path.write_text(content + row, encoding="utf-8")
    print(f"[{ep_id}] Appended update row to status.csv")

def main() -> None:
    for ep in EPISODES:
        update_status_csv(ep)

if __name__ == "__main__":
    main()
