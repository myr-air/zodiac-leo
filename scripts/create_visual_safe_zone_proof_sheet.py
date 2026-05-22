#!/usr/bin/env python3
"""Create local safe-zone proof sheets for the S01E01 V6 visual proof.

This script only annotates existing local proof snapshots. It does not call any
provider, browser, API, render/export pipeline, or account surface.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
EPISODE = "s01e01-campus-cafe-longplay"
PROOF_DIR = ROOT / "candidates" / EPISODE / "visual" / "proofs" / "animated-v6"
SNAPSHOTS = [
    "s01e01-vis-c01-v6-cute-smooth-motion-proof-30s-01-snapshot-02s.png",
    "s01e01-vis-c01-v6-cute-smooth-motion-proof-30s-01-snapshot-06s.png",
    "s01e01-vis-c01-v6-cute-smooth-motion-proof-30s-01-snapshot-14s.png",
    "s01e01-vis-c01-v6-cute-smooth-motion-proof-30s-01-snapshot-24s.png",
    "s01e01-vis-c01-v6-cute-smooth-motion-proof-30s-01-snapshot-29s.png",
]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


FONT_TITLE = font(30, bold=True)
FONT_LABEL = font(18, bold=True)
FONT_SMALL = font(14)


def draw_label(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fill: tuple[int, int, int]) -> None:
    x, y = xy
    bbox = draw.textbbox((x, y), text, font=FONT_SMALL)
    pad = 5
    draw.rounded_rectangle(
        (bbox[0] - pad, bbox[1] - pad, bbox[2] + pad, bbox[3] + pad),
        radius=6,
        fill=(20, 18, 15, 210),
    )
    draw.text((x, y), text, font=FONT_SMALL, fill=fill)


def annotated_panel(path: Path, size: tuple[int, int]) -> Image.Image:
    with Image.open(path) as img:
        panel = img.convert("RGBA").resize(size, Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(panel, "RGBA")
    w, h = panel.size

    margin_x = round(w * 0.10)
    margin_y = round(h * 0.10)
    top_12 = round(h * 0.12)
    mobile_x = round(w * 0.08)
    mobile_y = round(h * 0.08)

    # General 10% title/safe region.
    draw.rectangle((margin_x, margin_y, w - margin_x, h - margin_y), outline=(91, 210, 128, 230), width=3)
    draw_label(draw, (margin_x + 8, margin_y + 8), "10% safe inset", (152, 255, 180))

    # Top 12% caution line from source worksheet guidance.
    draw.line((0, top_12, w, top_12), fill=(255, 196, 82, 230), width=3)
    draw_label(draw, (12, top_12 + 8), "top 12% caution", (255, 218, 124))

    # Mobile/thumbnail caution region; not a platform proof, just a conservative source overlay.
    draw.rectangle((mobile_x, mobile_y, w - mobile_x, h - mobile_y), outline=(113, 180, 255, 190), width=2)
    draw_label(draw, (mobile_x + 8, h - mobile_y - 28), "8% mobile/thumbnail caution", (164, 209, 255))

    return panel.convert("RGB")


def make_safe_zone_sheet() -> Path:
    panel_w, panel_h = 512, 288
    gap = 24
    header_h = 112
    footer_h = 82
    cols = 2
    rows = 3
    sheet_w = cols * panel_w + (cols + 1) * gap
    sheet_h = header_h + rows * panel_h + (rows - 1) * gap + footer_h
    sheet = Image.new("RGB", (sheet_w, sheet_h), (245, 235, 218))
    draw = ImageDraw.Draw(sheet)
    draw.text((gap, 24), "S01E01 V6 Crop / Safe-Zone Proof Sheet", font=FONT_TITLE, fill=(48, 38, 28))
    draw.text(
        (gap, 64),
        "Local source-only overlay on existing V6 snapshots; not final render/export/upload proof.",
        font=FONT_SMALL,
        fill=(85, 69, 54),
    )

    for idx, name in enumerate(SNAPSHOTS):
        path = PROOF_DIR / name
        panel = annotated_panel(path, (panel_w, panel_h))
        col = idx % cols
        row = idx // cols
        x = gap + col * (panel_w + gap)
        y = header_h + row * (panel_h + gap)
        sheet.paste(panel, (x, y))
        label = name.rsplit("-", 1)[-1].replace(".png", "")
        draw.text((x + 8, y + 8), label, font=FONT_LABEL, fill=(255, 255, 255), stroke_width=2, stroke_fill=(20, 18, 15))

    footer_y = sheet_h - footer_h + 10
    draw.text(
        (gap, footer_y),
        "Review use: check top-left header, middle-left subtitles, and lower-right equalizer against conservative crop/safe-zone lines.",
        font=FONT_SMALL,
        fill=(65, 52, 42),
    )
    draw.text(
        (gap, footer_y + 26),
        "Still not a substitute for full assembly QA, final sidecars, render/export, upload, or platform/account review.",
        font=FONT_SMALL,
        fill=(119, 61, 47),
    )

    output = PROOF_DIR / "s01e01-vis-c01-v6-crop-safe-zone-proof-sheet-01.png"
    sheet.save(output)
    return output


def make_downscale_sheet() -> Path:
    widths = [375, 768, 1024, 1440]
    source = PROOF_DIR / "s01e01-vis-c01-v6-cute-smooth-motion-proof-30s-01-snapshot-06s.png"
    with Image.open(source) as img:
        base = img.convert("RGB")

    gap = 26
    header_h = 88
    max_w = 1500
    sheet_h = header_h + sum(round(width * 9 / 16) for width in widths) + gap * (len(widths) + 1)
    sheet = Image.new("RGB", (max_w + gap * 2, sheet_h), (245, 235, 218))
    draw = ImageDraw.Draw(sheet)
    draw.text((gap, 22), "S01E01 V6 Snapshot 06s Downscale Readability Sheet", font=FONT_TITLE, fill=(48, 38, 28))
    draw.text((gap, 58), "Local downscale check only; exact viewer/device UI is not simulated.", font=FONT_SMALL, fill=(85, 69, 54))

    y = header_h + gap
    for width in widths:
        height = round(width * 9 / 16)
        panel = base.resize((width, height), Image.Resampling.LANCZOS)
        x = gap
        sheet.paste(panel, (x, y))
        draw.rectangle((x, y, x + width, y + height), outline=(48, 38, 28), width=2)
        draw.text((x + width + 14, y + 8), f"{width}px wide", font=FONT_LABEL, fill=(48, 38, 28))
        draw.text((x + width + 14, y + 36), "snapshot 06s subtitle/header check", font=FONT_SMALL, fill=(85, 69, 54))
        y += height + gap

    output = PROOF_DIR / "s01e01-vis-c01-v6-downscale-readability-proof-sheet-01.png"
    sheet.save(output)
    return output


def main() -> None:
    missing = [str(PROOF_DIR / name) for name in SNAPSHOTS if not (PROOF_DIR / name).exists()]
    if missing:
        raise SystemExit(f"Missing snapshots: {missing}")

    safe_sheet = make_safe_zone_sheet()
    downscale_sheet = make_downscale_sheet()
    print(str(safe_sheet.relative_to(ROOT)))
    print(str(downscale_sheet.relative_to(ROOT)))


if __name__ == "__main__":
    main()
