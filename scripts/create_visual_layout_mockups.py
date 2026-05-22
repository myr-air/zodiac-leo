#!/usr/bin/env python3
"""Create local static visual layout mockups for S01E01.

The script composites text, equalizer shapes, and particle overlays onto an
existing local background image. It does not call provider APIs, open browsers,
upload files, or claim render/release readiness.
"""

from __future__ import annotations

import argparse
import json
import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from PIL import Image, ImageDraw, ImageFilter, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[1]
WIDTH = 1920
HEIGHT = 1080

BG_PATH = Path("candidates/s01e01-campus-cafe-longplay/visual/G.png")
OUT_DIR = Path("candidates/s01e01-campus-cafe-longplay/visual/proofs/static-layout-mockups-v4")

CHANNEL = "MELLOW LONGPLAY"
EPISODE = "S01 - E01"
TRACK_LABEL = "Now Playing"
TRACK_TITLE = "01 - Margin Notes at Table Three"
SUBTITLE = "After school, the rain comes down\nOn the window by our seats"
TARGET_SUBTITLE = "After school, the rain comes down"

INK = (68, 52, 42, 232)
BROWN = (105, 78, 56, 220)
SOFT_BROWN = (129, 96, 68, 195)
HONEY = (178, 125, 54, 210)
HONEY_SOFT = (190, 136, 62, 118)
LIGHT_STROKE = (255, 238, 211, 150)


@dataclass(frozen=True)
class Mockup:
    slug: str
    label: str
    description: str
    draw: Callable[[Image.Image, dict[str, ImageFont.FreeTypeFont]], None]


def root_path(path: Path) -> Path:
    return path if path.is_absolute() else PROJECT_ROOT / path


def load_font(path: str, size: int, index: int = 0) -> ImageFont.FreeTypeFont:
    candidates = [Path(path), Path("/System/Library/Fonts/NewYork.ttf"), Path("/System/Library/Fonts/SFNS.ttf")]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size, index=index)
    return ImageFont.load_default(size=size)


def fonts() -> dict[str, ImageFont.FreeTypeFont]:
    # Header uses the same NewYork serif family that previously carried
    # "After Class, Gently".
    return {
        "header": load_font("/System/Library/Fonts/NewYork.ttf", 24),
        "header_small": load_font("/System/Library/Fonts/NewYork.ttf", 22),
        "now": load_font("/System/Library/Fonts/NewYork.ttf", 26),
        "track": load_font("/System/Library/Fonts/NewYork.ttf", 28),
        "track_small": load_font("/System/Library/Fonts/NewYork.ttf", 24),
        "subtitle": load_font("/System/Library/Fonts/Noteworthy.ttc", 46),
        "subtitle_serif": load_font("/System/Library/Fonts/NewYork.ttf", 43),
        "header_ref": load_font("/System/Library/Fonts/NewYork.ttf", 31),
        "now_ref": load_font("/System/Library/Fonts/NewYork.ttf", 25),
        "track_ref": load_font("/System/Library/Fonts/NewYork.ttf", 31),
        "subtitle_ref": load_font("/System/Library/Fonts/NewYorkItalic.ttf", 50),
    }


def cover_resize(image: Image.Image) -> Image.Image:
    image = image.convert("RGBA")
    scale = max(WIDTH / image.width, HEIGHT / image.height)
    resized = image.resize((math.ceil(image.width * scale), math.ceil(image.height * scale)), Image.Resampling.LANCZOS)
    left = (resized.width - WIDTH) // 2
    top = (resized.height - HEIGHT) // 2
    return resized.crop((left, top, left + WIDTH, top + HEIGHT))


def base_canvas(background_path: Path, seed: int) -> Image.Image:
    bg = cover_resize(Image.open(background_path))
    bg = Image.alpha_composite(bg, Image.new("RGBA", (WIDTH, HEIGHT), (255, 242, 220, 10)))
    return Image.alpha_composite(bg, particle_layer(seed))


def particle_layer(seed: int) -> Image.Image:
    rng = random.Random(seed)
    layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    for _ in range(145):
        x = rng.triangular(30, WIDTH - 30, 420)
        y = rng.triangular(30, HEIGHT - 50, 300)
        r = rng.uniform(1.0, 4.0)
        alpha = int(rng.uniform(18, 60))
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(255, rng.randrange(214, 236), rng.randrange(162, 200), alpha))
    for _ in range(14):
        x = rng.uniform(50, WIDTH * 0.75)
        y = rng.uniform(40, HEIGHT * 0.62)
        r = rng.uniform(10, 22)
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(255, 225, 176, 18))
    return layer.filter(ImageFilter.GaussianBlur(0.45))


def glow_text(
    image: Image.Image,
    xy: tuple[int, int],
    value: str,
    font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int, int] = INK,
    *,
    anchor: str | None = None,
    align: str = "left",
    spacing: int = 4,
    stroke_width: int = 1,
    glow_radius: float = 2.0,
    glow_alpha: int = 54,
) -> None:
    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow, "RGBA")
    gd.multiline_text(
        xy,
        value,
        font=font,
        fill=(255, 231, 190, glow_alpha),
        anchor=anchor,
        align=align,
        spacing=spacing,
        stroke_width=stroke_width + 1,
        stroke_fill=(255, 231, 190, max(18, glow_alpha - 12)),
    )
    image.alpha_composite(glow.filter(ImageFilter.GaussianBlur(glow_radius)))
    draw = ImageDraw.Draw(image, "RGBA")
    draw.multiline_text(
        xy,
        value,
        font=font,
        fill=fill,
        anchor=anchor,
        align=align,
        spacing=spacing,
        stroke_width=stroke_width,
        stroke_fill=LIGHT_STROKE,
    )


def dot(draw: ImageDraw.ImageDraw, cx: int, cy: int, r: int = 4, alpha: int = 190) -> None:
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(178, 125, 54, alpha))


def line(draw: ImageDraw.ImageDraw, x1: int, y1: int, x2: int, y2: int, alpha: int = 150, width: int = 2) -> None:
    draw.line((x1, y1, x2, y2), fill=(178, 125, 54, alpha), width=width)


def headphone_icon(draw: ImageDraw.ImageDraw, x: int, y: int, scale: float = 1.0, alpha: int = 210) -> None:
    color = (105, 78, 56, alpha)
    w = int(24 * scale)
    h = int(22 * scale)
    draw.arc((x, y, x + w, y + h), start=196, end=344, fill=color, width=max(2, int(2 * scale)))
    draw.rounded_rectangle((x + 1, y + int(11 * scale), x + int(6 * scale), y + int(21 * scale)), radius=2, fill=color)
    draw.rounded_rectangle((x + w - int(6 * scale), y + int(11 * scale), x + w - 1, y + int(21 * scale)), radius=2, fill=color)


def headphone_icon_reference(draw: ImageDraw.ImageDraw, x: int, y: int, alpha: int = 192) -> None:
    color = (105, 78, 56, alpha)
    draw.arc((x, y, x + 86, y + 78), start=202, end=338, fill=color, width=5)
    draw.rounded_rectangle((x + 3, y + 47, x + 18, y + 77), radius=4, fill=color)
    draw.rounded_rectangle((x + 68, y + 47, x + 83, y + 77), radius=4, fill=color)


def top_left_block(
    image: Image.Image,
    f: dict[str, ImageFont.FreeTypeFont],
    *,
    x: int = 112,
    y: int = 88,
    rule_width: int = 630,
    scale: float = 1.0,
) -> None:
    draw = ImageDraw.Draw(image, "RGBA")
    headphone_icon(draw, x, y + 6, scale=0.92 * scale)
    text_x = x + int(38 * scale)
    glow_text(image, (text_x, y), CHANNEL, f["header"], BROWN, glow_alpha=38, glow_radius=1.35)
    ch_w = int(draw.textlength(CHANNEL, font=f["header"]))
    dot(draw, text_x + ch_w + 24, y + 16, r=4, alpha=170)
    glow_text(image, (text_x + ch_w + 44, y), EPISODE, f["header"], BROWN, glow_alpha=38, glow_radius=1.35)

    glow_text(image, (x, y + int(58 * scale)), TRACK_LABEL, f["now"], SOFT_BROWN, glow_alpha=42, glow_radius=1.45)
    glow_text(image, (x, y + int(96 * scale)), TRACK_TITLE, f["track"], INK, glow_alpha=48, glow_radius=1.6)
    line_y = y + int(142 * scale)
    line(draw, x, line_y, x + rule_width, line_y, alpha=145, width=2)
    dot(draw, x + rule_width + 24, line_y, r=5, alpha=175)


def top_left_block_reference(image: Image.Image, f: dict[str, ImageFont.FreeTypeFont]) -> None:
    draw = ImageDraw.Draw(image, "RGBA")
    icon_x = 92
    icon_y = 78
    headphone_icon_reference(draw, icon_x, icon_y, alpha=190)
    line(draw, 212, 78, 212, 205, alpha=112, width=1)

    text_x = 250
    y = 88
    glow_text(image, (text_x, y), CHANNEL, f["header_ref"], BROWN, glow_alpha=34, glow_radius=1.25)
    ch_w = int(draw.textlength(CHANNEL, font=f["header_ref"]))
    dot(draw, text_x + ch_w + 26, y + 18, r=4, alpha=170)
    glow_text(image, (text_x + ch_w + 52, y), EPISODE, f["header_ref"], BROWN, glow_alpha=34, glow_radius=1.25)

    glow_text(image, (text_x, y + 48), TRACK_LABEL, f["now_ref"], SOFT_BROWN, glow_alpha=38, glow_radius=1.35)
    glow_text(image, (text_x, y + 88), TRACK_TITLE, f["track_ref"], INK, glow_alpha=44, glow_radius=1.45)
    line_y = y + 144
    line(draw, text_x, line_y, text_x + 450, line_y, alpha=132, width=2)
    dot(draw, text_x + 458, line_y, r=5, alpha=170)


def subtitle_block(
    image: Image.Image,
    f: dict[str, ImageFont.FreeTypeFont],
    *,
    cx: int = 374,
    cy: int = 430,
    font_key: str = "subtitle",
    spacing: int = 8,
    alpha: int = 236,
) -> None:
    glow_text(
        image,
        (cx, cy),
        SUBTITLE,
        f[font_key],
        (66, 51, 42, alpha),
        anchor="ma",
        align="center",
        spacing=spacing,
        stroke_width=1,
        glow_alpha=58,
        glow_radius=2.1,
    )


def subtitle_reference(image: Image.Image, f: dict[str, ImageFont.FreeTypeFont]) -> None:
    glow_text(
        image,
        (415, 464),
        TARGET_SUBTITLE,
        f["subtitle_ref"],
        (78, 58, 44, 226),
        anchor="ma",
        align="center",
        stroke_width=1,
        glow_alpha=46,
        glow_radius=1.8,
    )


def ornament(image: Image.Image, cx: int = 415, y: int = 542) -> None:
    draw = ImageDraw.Draw(image, "RGBA")
    color = (178, 125, 54, 112)
    line(draw, cx - 132, y, cx - 42, y, alpha=82, width=1)
    line(draw, cx + 42, y, cx + 132, y, alpha=82, width=1)
    dot(draw, cx, y, r=4, alpha=116)
    for dx in (-30, 30):
        draw.polygon(
            [(cx + dx, y), (cx + dx + (9 if dx < 0 else -9), y - 8), (cx + dx + (18 if dx < 0 else -18), y - 1)],
            fill=color,
        )
        draw.polygon(
            [(cx + dx, y), (cx + dx + (9 if dx < 0 else -9), y + 8), (cx + dx + (18 if dx < 0 else -18), y + 1)],
            fill=color,
        )
    for side in (-1, 1):
        x1 = cx + side * 52
        x2 = cx + side * 118
        draw.arc((min(x1, x2), y - 16, max(x1, x2), y + 16), start=200 if side < 0 else 340, end=20 if side < 0 else 160, fill=color, width=1)
        for index in range(3):
            lx = cx + side * (70 + index * 17)
            ly = y - 3 - index * 2
            draw.ellipse((lx - 6, ly - 3, lx + 6, ly + 3), fill=(178, 125, 54, 72))


def rotated_brick(
    image: Image.Image,
    center: tuple[float, float],
    angle: float,
    radius: float,
    length: float,
    thickness: float,
    color: tuple[int, int, int, int],
) -> None:
    cx, cy = center
    radial = (math.cos(angle), math.sin(angle))
    tangent = (-math.sin(angle), math.cos(angle))
    inner = radius - length / 2
    outer = radius + length / 2
    half = thickness / 2
    points = [
        (cx + radial[0] * inner + tangent[0] * half, cy + radial[1] * inner + tangent[1] * half),
        (cx + radial[0] * outer + tangent[0] * half, cy + radial[1] * outer + tangent[1] * half),
        (cx + radial[0] * outer - tangent[0] * half, cy + radial[1] * outer - tangent[1] * half),
        (cx + radial[0] * inner - tangent[0] * half, cy + radial[1] * inner - tangent[1] * half),
    ]
    ImageDraw.Draw(image, "RGBA").polygon(points, fill=color)


def quarter_equalizer(
    image: Image.Image,
    *,
    cx: int = 1802,
    cy: int = 1012,
    radius: int = 236,
    spread_deg: tuple[int, int] = (184, 276),
    count: int = 30,
    alpha: int = 168,
    seed: int = 11,
) -> None:
    draw = ImageDraw.Draw(image, "RGBA")
    start, end = [math.radians(v) for v in spread_deg]
    rng = random.Random(seed)
    # subtle quarter guide lines
    for rr, aa in ((radius - 26, 44), (radius + 31, 34)):
        prev: tuple[float, float] | None = None
        for i in range(80):
            t = start + (end - start) * i / 79
            p = (cx + math.cos(t) * rr, cy + math.sin(t) * rr)
            if prev is not None:
                draw.line((*prev, *p), fill=(178, 125, 54, aa), width=2)
            prev = p
    for idx in range(count):
        t = start + (end - start) * idx / max(1, count - 1)
        amp = 0.42 + 0.46 * abs(math.sin(idx * 0.53)) + rng.uniform(-0.08, 0.08)
        length = 18 + 42 * max(0.12, min(0.96, amp))
        thickness = 9 + (idx % 3 == 1) * 2
        rr = radius + rng.uniform(-5, 6)
        color = (178, 125, 54, int(alpha * (0.78 + 0.22 * amp)))
        rotated_brick(image, (cx, cy), t, rr, length, thickness, color)
    # spaced dots along the inner arc make it feel designed, not like a generic player.
    for frac in (0.06, 0.26, 0.47, 0.70, 0.91):
        t = start + (end - start) * frac
        dot(draw, int(cx + math.cos(t) * (radius - 54)), int(cy + math.sin(t) * (radius - 54)), r=4, alpha=135)


def quarter_equalizer_reference(image: Image.Image) -> None:
    quarter_equalizer(
        image,
        cx=1972,
        cy=1124,
        radius=354,
        spread_deg=(196, 286),
        count=46,
        alpha=154,
        seed=17,
    )


def layout_v4_01(image: Image.Image, f: dict[str, ImageFont.FreeTypeFont]) -> None:
    top_left_block(image, f, x=112, y=88, rule_width=624)
    subtitle_block(image, f, cx=386, cy=432, font_key="subtitle")
    quarter_equalizer(image, cx=1808, cy=1018, radius=240, count=32, alpha=166, seed=1)


def layout_v4_02(image: Image.Image, f: dict[str, ImageFont.FreeTypeFont]) -> None:
    top_left_block(image, f, x=108, y=82, rule_width=590)
    subtitle_block(image, f, cx=374, cy=405, font_key="subtitle")
    quarter_equalizer(image, cx=1814, cy=1018, radius=260, spread_deg=(188, 278), count=34, alpha=148, seed=2)


def layout_v4_03(image: Image.Image, f: dict[str, ImageFont.FreeTypeFont]) -> None:
    top_left_block(image, f, x=110, y=94, rule_width=646)
    subtitle_block(image, f, cx=398, cy=455, font_key="subtitle_serif", spacing=7)
    quarter_equalizer(image, cx=1814, cy=1008, radius=226, spread_deg=(184, 270), count=28, alpha=174, seed=3)


def layout_v4_04(image: Image.Image, f: dict[str, ImageFont.FreeTypeFont]) -> None:
    top_left_block(image, f, x=104, y=76, rule_width=560, scale=0.94)
    subtitle_block(image, f, cx=366, cy=426, font_key="subtitle")
    quarter_equalizer(image, cx=1776, cy=1000, radius=226, spread_deg=(190, 286), count=27, alpha=154, seed=4)


def layout_v4_05(image: Image.Image, f: dict[str, ImageFont.FreeTypeFont]) -> None:
    top_left_block(image, f, x=124, y=88, rule_width=596)
    subtitle_block(image, f, cx=398, cy=410, font_key="subtitle", alpha=225)
    quarter_equalizer(image, cx=1818, cy=1032, radius=276, spread_deg=(188, 276), count=38, alpha=128, seed=5)


def layout_v4_06(image: Image.Image, f: dict[str, ImageFont.FreeTypeFont]) -> None:
    top_left_block(image, f, x=112, y=86, rule_width=620)
    subtitle_block(image, f, cx=382, cy=468, font_key="subtitle")
    quarter_equalizer(image, cx=1798, cy=1014, radius=214, spread_deg=(184, 282), count=33, alpha=178, seed=6)


def layout_v4_07(image: Image.Image, f: dict[str, ImageFont.FreeTypeFont]) -> None:
    top_left_block_reference(image, f)
    subtitle_reference(image, f)
    ornament(image)
    quarter_equalizer_reference(image)


def mockups() -> list[Mockup]:
    return [
        Mockup("v4-01-balanced-quarter", "Balanced quarter equalizer", "New top-left info block, subtitle centered higher, medium quarter-brick equalizer.", layout_v4_01),
        Mockup("v4-02-higher-subtitle-wide-arc", "Higher subtitle wide arc", "Subtitle moves up; equalizer has wider radius and softer opacity.", layout_v4_02),
        Mockup("v4-03-serif-subtitle-tight-arc", "Serif subtitle tight arc", "Tests full serif typography and tighter lower-right quarter arc.", layout_v4_03),
        Mockup("v4-04-compact-header-left-arc", "Compact header left arc", "Slightly smaller header and equalizer shifted left for motion clearance.", layout_v4_04),
        Mockup("v4-05-airy-wide-arc", "Airy wide arc", "More negative space with a large faint quarter equalizer texture.", layout_v4_05),
        Mockup("v4-06-lower-subtitle-dense-arc", "Lower subtitle dense arc", "Subtitle lower balance test with stronger brick-wave density.", layout_v4_06),
        Mockup("v4-07-user-reference-match", "User reference match", "Closest static proof to the supplied reference: larger separated headphone icon, vertical divider, serif italic one-line subtitle, ornament, and large off-canvas quarter equalizer.", layout_v4_07),
    ]


def save_contact_sheet(paths: list[Path], output_path: Path) -> None:
    thumbs: list[Image.Image] = []
    for path in paths:
        thumb = Image.open(path).convert("RGB")
        thumb.thumbnail((640, 360), Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", (640, 390), (246, 235, 218))
        canvas.paste(thumb, (0, 0))
        draw = ImageDraw.Draw(canvas)
        draw.text((12, 366), path.stem, fill=(84, 64, 48))
        thumbs.append(canvas)
    cols = 2
    rows = math.ceil(len(thumbs) / cols)
    sheet = Image.new("RGB", (cols * 640, rows * 390), (238, 226, 208))
    for index, thumb in enumerate(thumbs):
        sheet.paste(thumb, ((index % cols) * 640, (index // cols) * 390))
    sheet.save(output_path, quality=95)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--background", type=Path, default=BG_PATH)
    parser.add_argument("--out-dir", type=Path, default=OUT_DIR)
    args = parser.parse_args()

    background = root_path(args.background)
    out_dir = root_path(args.out_dir)
    if not background.exists():
        raise FileNotFoundError(background)
    out_dir.mkdir(parents=True, exist_ok=True)

    f = fonts()
    index = {
        "schema_version": "0.4.1",
        "status": "local_static_layout_mockups_v4_source_only",
        "boundary": "No provider/API/browser/upload/render/release action. Static proof images only.",
        "background": str(background.relative_to(PROJECT_ROOT)),
        "requirements": [
            "top-left info block uses NewYork serif like the previous After Class Gently title",
            "vector headphone icon plus MELLOW LONGPLAY dot S01 - E01",
            "Now Playing and track title remain top-left under the channel line",
            "long rule plus terminal dot under track title",
            "subtitle sits centered in the left blank area and slightly higher",
            "bottom-right quarter-circle brick/bar equalizer with curved spacing",
            "v4-07 tests the user-supplied reference layout with separated icon, vertical divider, one-line italic subtitle, ornament, and larger off-canvas equalizer",
        ],
        "outputs": [],
    }
    output_paths: list[Path] = []
    for mockup in mockups():
        image = base_canvas(background, seed=mockup.slug.__hash__() & 0xFFFF)
        mockup.draw(image, f)
        output_path = out_dir / f"s01e01-vis-c01-layout-{mockup.slug}.png"
        image.convert("RGB").save(output_path, quality=95)
        output_paths.append(output_path)
        index["outputs"].append(
            {
                "path": str(output_path.relative_to(PROJECT_ROOT)),
                "label": mockup.label,
                "description": mockup.description,
            }
        )
    contact_path = out_dir / "s01e01-vis-c01-layout-v4-contact-sheet.png"
    save_contact_sheet(output_paths, contact_path)
    index["contact_sheet"] = str(contact_path.relative_to(PROJECT_ROOT))
    for output in index["outputs"]:
        print(output["path"])
    print(index["contact_sheet"])
    print(json.dumps(index, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
