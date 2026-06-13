import os
import re

from pathlib import Path

episodes = [
    "s01e01-campus-cafe-longplay",
    "s01e02-classroom-window-longplay",
    "s01e03-rooftop-golden-hour-longplay",
    "s01e04-bookstore-afternoon-longplay"
]

def clean_text(text, episode):
    # General replacements
    # 1. Pronouns (Keep ฉัน/ของฉัน for female singer; do not replace with เรา/ของเรา)
    text = re.sub(r'ของพวกเรา', 'ของเรา', text)
    text = re.sub(r'พวกเรา', 'เรา', text)
    text = re.sub(r'ของคุณ', 'ของเธอ', text)
    text = re.sub(r'คุณ', 'เธอ', text)

    # 2. Literary and formal terms
    text = re.sub(r'โอ้ จงทอดมอง(.+?)นั่นสิ', r'มอง\1นะ', text)
    text = re.sub(r'จงทอดมอง(.+?)นั่นสิ', r'มอง\1นะ', text)
    text = re.sub(r'จงทอดมอง', 'มอง', text)
    text = re.sub(r'จงดู', 'ดู', text)
    text = re.sub(r'จงอยู่', 'อยู่', text)
    text = re.sub(r'จง', '', text) # remove any remaining 'จง'
    
    text = re.sub(r'ดั่ง', 'เหมือน', text)
    text = re.sub(r'ดังเช่น', 'เหมือนกับ', text)
    text = re.sub(r'เพียงใด', 'แค่ไหน', text)
    
    text = re.sub(r'ศีรษะ', 'หัว', text)
    text = re.sub(r'ศิลา', 'หิน', text)
    text = re.sub(r'อันแสน', 'ที่แสน', text)
    text = re.sub(r'อย่างแสน', 'อย่าง', text)
    text = re.sub(r'ผู้สัญจรผ่านไปมา', 'คนเดินผ่าน', text)

    # Episode-specific replacements
    if episode == "s01e01-campus-cafe-longplay":
        text = re.sub(r'พรุ่งหลังเลิกเรียน', 'พรุ่งนี้หลังเลิกเรียน', text)
        text = re.sub(r'เหนี่ยวรั้ง', 'รั้ง', text)
        text = re.sub(r'เครื่องหมายจุลภาค', 'เครื่องหมายคอมมา', text)
        text = re.sub(r'กระดาษเช็ดมือ', 'ทิชชู่', text)
        text = re.sub(r'การแห่ฉลอง', 'การฉลองใหญ่โต', text)
        text = re.sub(r'ที่นั่งริมตู้', 'ที่นั่งแบบบูธ', text)
        text = re.sub(r'เบรกดังฟู่', 'วิ่งผ่าน', text)
        text = re.sub(r'กล่องสี่เหลี่ยม', 'กรอบสี่เหลี่ยม', text)
    elif episode == "s01e02-classroom-window-longplay":
        text = re.sub(r'วาดกล่อง', 'วาดกรอบ', text)
        text = re.sub(r'กล่องดินสอ', 'กล่องดินสอ', text) # Keep as is
    elif episode == "s01e04-bookstore-afternoon-longplay":
        text = re.sub(r'ช่องทางเดิน', 'ทางเดิน', text)

    return text

def process_file(filepath, episode):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    new_lines = []
    changes = []

    for i, line in enumerate(lines):
        # We only clean if the line is not empty, not just a number, and not a timestamp line
        if line.strip() and not re.match(r'^\d+$', line) and '-->' not in line:
            cleaned = clean_text(line, episode)
            if cleaned != line:
                changes.append((i + 1, line, cleaned))
                new_lines.append(cleaned)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    new_content = '\n'.join(new_lines)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"\nProcessed {episode}: {len(changes)} changes made.")
    for line_num, old, new in changes[:15]: # Show first 15 changes as example
        print(f"  Line {line_num}: {old} -> {new}")
    if len(changes) > 15:
        print(f"  ... and {len(changes) - 15} more changes.")

def main():
    base_dir = str(Path(__file__).resolve().parents[1] / "channel" / "episodes")
    for ep in episodes:
        filepath = os.path.join(base_dir, ep, "subtitles", f"{ep}.th.srt")
        process_file(filepath, ep)

if __name__ == "__main__":
    main()
