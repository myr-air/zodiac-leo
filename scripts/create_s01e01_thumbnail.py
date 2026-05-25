#!/usr/bin/env python3
"""Create the local S01E01 YouTube thumbnail from the accepted G.png background.

This helper is local-only. It reads the existing user-approved visual background
direction and writes one 1280x720 JPEG thumbnail candidate under candidates/.
It does not call providers, browsers, platform APIs, account surfaces, or claim
release/platform readiness.
"""

from __future__ import annotations

import argparse
import io
import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EPISODE_ID = "s01e01-campus-cafe-longplay"
DEFAULT_BACKGROUND = Path("candidates/s01e01-campus-cafe-longplay/visual/G.png")
DEFAULT_OUTPUT_ROOT = Path("candidates/s01e01-campus-cafe-longplay/thumbnail")
DEFAULT_OUTPUT = DEFAULT_OUTPUT_ROOT / "s01e01-campus-cafe-longplay.thumbnail-1280x720.jpg"
MUSIC_PLAYLIST_OUTPUT = DEFAULT_OUTPUT_ROOT / "s01e01-campus-cafe-longplay.thumbnail-v2-music-playlist-1280x720.jpg"
SOFT_DEPTH_OUTPUT = DEFAULT_OUTPUT_ROOT / "s01e01-campus-cafe-longplay.thumbnail-v3-soft-depth-1280x720.jpg"
BIG_BRAND_OUTPUT = DEFAULT_OUTPUT_ROOT / "s01e01-campus-cafe-longplay.thumbnail-v4-big-brand-depth-1280x720.jpg"
ALLOWED_OUTPUT_ROOTS = (DEFAULT_OUTPUT_ROOT,)
LAYOUT_ORIGINAL = "original"
LAYOUT_MUSIC_PLAYLIST = "music-playlist"
LAYOUT_SOFT_DEPTH = "soft-depth"
LAYOUT_BIG_BRAND_DEPTH = "big-brand-depth"
LAYOUTS = (LAYOUT_ORIGINAL, LAYOUT_MUSIC_PLAYLIST, LAYOUT_SOFT_DEPTH, LAYOUT_BIG_BRAND_DEPTH)

WIDTH = 1280
HEIGHT = 720
YOUTUBE_THUMBNAIL_MAX_BYTES = 2_000_000

INK = (64, 48, 38, 242)
BROWN = (103, 76, 55, 230)
SOFT_BROWN = (130, 93, 62, 215)
CREAM = (255, 242, 219, 230)
HONEY = (192, 129, 49, 210)
BIG_BRAND_CAPTION_TEXT = "First Love After School Playlist"
BIG_BRAND_CAPTION_LEFT_NOTE = "♪"
BIG_BRAND_CAPTION_RIGHT_NOTES = "♫ ♬"


def project_path(path: Path | str) -> Path:
    path = Path(path).expanduser()
    return path if path.is_absolute() else PROJECT_ROOT / path


def assert_no_control_chars(path: Path) -> None:
    text = str(path)
    if any(ord(char) < 32 or ord(char) == 127 for char in text):
        raise ValueError(f"refusing path with control characters: {path!s}")


def assert_allowed_output_root(path: Path) -> None:
    """Refuse extra thumbnail roots that would exceed this narrow local gate."""
    assert_no_control_chars(path)
    resolved = project_path(path).resolve()
    allowed = {project_path(root).resolve() for root in ALLOWED_OUTPUT_ROOTS}
    if resolved not in allowed:
        raise ValueError(
            "refusing non-canonical thumbnail output root; additional or revised "
            "thumbnail outputs require a new explicit gate"
        )


def load_font(candidates: tuple[str, ...], size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def fonts() -> dict[str, ImageFont.FreeTypeFont | ImageFont.ImageFont]:
    return {
        "eyebrow": load_font(
            (
                "/System/Library/Fonts/Supplemental/ChalkboardSE.ttc",
                "/System/Library/Fonts/Avenir Next.ttc",
                "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            ),
            30,
        ),
        "title": load_font(
            (
                "/System/Library/Fonts/Supplemental/ChalkboardSE.ttc",
                "/System/Library/Fonts/Avenir Next.ttc",
                "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            ),
            62,
        ),
        "subtitle": load_font(
            (
                "/System/Library/Fonts/Avenir Next.ttc",
                "/System/Library/Fonts/Supplemental/Arial.ttf",
                "/System/Library/Fonts/SFNS.ttf",
            ),
            32,
        ),
        "small": load_font(
            (
                "/System/Library/Fonts/Avenir Next.ttc",
                "/System/Library/Fonts/Supplemental/Arial.ttf",
                "/System/Library/Fonts/SFNS.ttf",
            ),
            24,
        ),
        "ghost": load_font(
            (
                "/System/Library/Fonts/Avenir Next.ttc",
                "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
                "/System/Library/Fonts/SFNS.ttf",
            ),
            118,
        ),
        "brand_top": load_font(
            (
                "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
                "/System/Library/Fonts/Avenir Next.ttc",
                "/System/Library/Fonts/SFNS.ttf",
            ),
            152,
        ),
        "brand_bottom": load_font(
            (
                "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
                "/System/Library/Fonts/Avenir Next.ttc",
                "/System/Library/Fonts/SFNS.ttf",
            ),
            80,
        ),
        "bottom_caption": load_font(
            (
                "/System/Library/Fonts/Supplemental/Arial.ttf",
                "/System/Library/Fonts/Avenir Next.ttc",
                "/System/Library/Fonts/SFNS.ttf",
            ),
            22,
        ),
        "bottom_caption_note": load_font(
            (
                "/System/Library/Fonts/Apple Symbols.ttf",
                "/System/Library/Fonts/Supplemental/Arial.ttf",
                "/System/Library/Fonts/SFNS.ttf",
            ),
            24,
        ),
    }


def cover_resize(image: Image.Image, size: tuple[int, int] = (WIDTH, HEIGHT)) -> Image.Image:
    image = image.convert("RGB")
    target_w, target_h = size
    scale = max(target_w / image.width, target_h / image.height)
    resized = image.resize((math.ceil(image.width * scale), math.ceil(image.height * scale)), Image.Resampling.LANCZOS)
    left = (resized.width - target_w) // 2
    top = (resized.height - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def glow_text(
    image: Image.Image,
    xy: tuple[int, int],
    text: str,
    font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
    fill: tuple[int, int, int, int],
    *,
    stroke_width: int = 1,
    glow_radius: float = 2.0,
    glow_alpha: int = 76,
    spacing: int = 8,
) -> None:
    glow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow, "RGBA")
    glow_draw.multiline_text(
        xy,
        text,
        font=font,
        fill=(255, 231, 190, glow_alpha),
        spacing=spacing,
        stroke_width=stroke_width + 2,
        stroke_fill=(255, 236, 207, max(22, glow_alpha - 16)),
    )
    image.alpha_composite(glow.filter(ImageFilter.GaussianBlur(glow_radius)))
    draw = ImageDraw.Draw(image, "RGBA")
    draw.multiline_text(
        xy,
        text,
        font=font,
        fill=fill,
        spacing=spacing,
        stroke_width=stroke_width,
        stroke_fill=(255, 243, 220, 180),
    )


def draw_warm_readability_layer(image: Image.Image) -> None:
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")
    for x in range(WIDTH):
        strength = max(0, 150 - int(x * 150 / (WIDTH * 0.76)))
        draw.line((x, 0, x, HEIGHT), fill=(255, 235, 202, strength))
    draw.rounded_rectangle((44, 58, 738, 534), radius=34, fill=(255, 244, 222, 52), outline=(255, 238, 202, 92), width=2)
    image.alpha_composite(overlay.filter(ImageFilter.GaussianBlur(0.35)))


def draw_headphone_icon(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    color = (103, 76, 55, 215)
    draw.arc((x, y, x + 54, y + 52), start=202, end=338, fill=color, width=4)
    draw.rounded_rectangle((x + 2, y + 31, x + 13, y + 52), radius=3, fill=color)
    draw.rounded_rectangle((x + 41, y + 31, x + 52, y + 52), radius=3, fill=color)


def draw_single_music_note(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    *,
    scale: float = 1.0,
    alpha: int = 90,
    double: bool = False,
) -> None:
    color = (192, 129, 49, alpha)
    width = max(2, int(4 * scale))
    head_w = int(17 * scale)
    head_h = int(12 * scale)
    stem_h = int(44 * scale)
    gap = int(26 * scale)

    def one_note(nx: int, ny: int) -> None:
        draw.ellipse((nx, ny + stem_h - head_h, nx + head_w, ny + stem_h), fill=color)
        stem_x = nx + head_w - width // 2
        draw.line((stem_x, ny + stem_h - head_h // 2, stem_x, ny), fill=color, width=width)
        draw.line((stem_x, ny, stem_x + int(17 * scale), ny + int(7 * scale)), fill=color, width=width)

    one_note(x, y)
    if double:
        one_note(x + gap, y + int(4 * scale))
        draw.line((x + head_w, y + int(5 * scale), x + gap + head_w, y + int(9 * scale)), fill=color, width=width)


def draw_music_notes(image: Image.Image, f: dict[str, ImageFont.FreeTypeFont | ImageFont.ImageFont]) -> None:
    draw = ImageDraw.Draw(image, "RGBA")
    draw_single_music_note(draw, 616, 190, scale=0.92, alpha=86)
    draw_single_music_note(draw, 544, 394, scale=0.72, alpha=62, double=True)
    draw_single_music_note(draw, 470, 470, scale=0.56, alpha=48)


def draw_original_copy(
    base: Image.Image,
    draw: ImageDraw.ImageDraw,
    f: dict[str, ImageFont.FreeTypeFont | ImageFont.ImageFont],
) -> None:
    glow_text(base, (142, 88), "MELLOW LONGPLAY  ·  S01 E01", f["eyebrow"], BROWN, stroke_width=1, glow_radius=1.5, glow_alpha=56)
    draw.line((72, 142, 650, 142), fill=HONEY, width=3)
    draw.ellipse((672, 137, 684, 149), fill=HONEY)

    glow_text(base, (70, 190), "After-School\nFirst Love", f["title"], INK, stroke_width=2, glow_radius=2.2, glow_alpha=86, spacing=5)
    glow_text(base, (74, 360), "Soft Cozy Vocals for Study\n& Coffee Breaks", f["subtitle"], SOFT_BROWN, stroke_width=1, glow_radius=1.7, glow_alpha=60, spacing=6)

    pill = Image.new("RGBA", base.size, (0, 0, 0, 0))
    pill_draw = ImageDraw.Draw(pill, "RGBA")
    pill_draw.rounded_rectangle((74, 470, 466, 526), radius=28, fill=CREAM, outline=(194, 132, 54, 128), width=2)
    base.alpha_composite(pill)
    glow_text(base, (102, 486), "41-minute mellow vocal mix", f["small"], BROWN, stroke_width=0, glow_radius=1.1, glow_alpha=36)


def draw_music_playlist_copy(
    base: Image.Image,
    draw: ImageDraw.ImageDraw,
    f: dict[str, ImageFont.FreeTypeFont | ImageFont.ImageFont],
) -> None:
    glow_text(base, (142, 88), "MELLOW LONGPLAY  ·  MUSIC MIX", f["eyebrow"], BROWN, stroke_width=1, glow_radius=1.5, glow_alpha=56)
    draw.line((72, 142, 650, 142), fill=HONEY, width=3)
    draw.ellipse((672, 137, 684, 149), fill=HONEY)

    glow_text(base, (70, 190), "Cozy Vocal\nPlaylist", f["title"], INK, stroke_width=2, glow_radius=2.2, glow_alpha=86, spacing=5)
    glow_text(base, (76, 366), "After-School First Love", f["subtitle"], SOFT_BROWN, stroke_width=1, glow_radius=1.7, glow_alpha=58)

    pill = Image.new("RGBA", base.size, (0, 0, 0, 0))
    pill_draw = ImageDraw.Draw(pill, "RGBA")
    pill_draw.rounded_rectangle((74, 465, 418, 521), radius=28, fill=CREAM, outline=(194, 132, 54, 128), width=2)
    base.alpha_composite(pill)
    glow_text(base, (104, 481), "41-min music mix", f["small"], BROWN, stroke_width=0, glow_radius=1.1, glow_alpha=36)
    draw_music_notes(base, f)


def subject_soft_mask() -> Image.Image:
    mask = Image.new("L", (WIDTH, HEIGHT), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((512, 44, 1038, 676), fill=212)
    draw.ellipse((658, 16, 940, 348), fill=235)
    draw.rounded_rectangle((602, 238, 1120, 694), radius=118, fill=176)
    return mask.filter(ImageFilter.GaussianBlur(22))


def draw_waveform(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    heights = [12, 22, 34, 48, 36, 24, 14, 28, 42, 30, 18]
    for index, height in enumerate(heights):
        bx = x + index * 16
        draw.rounded_rectangle((bx, y - height // 2, bx + 6, y + height // 2), radius=3, fill=(192, 129, 49, 112))


def draw_soft_depth_copy(
    base: Image.Image,
    original_foreground: Image.Image,
    draw: ImageDraw.ImageDraw,
    f: dict[str, ImageFont.FreeTypeFont | ImageFont.ImageFont],
) -> None:
    ghost = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ghost_draw = ImageDraw.Draw(ghost, "RGBA")
    ghost_draw.text((372, 238), "LONGPLAY", font=f["ghost"], fill=(154, 106, 64, 38))
    ghost = ghost.filter(ImageFilter.GaussianBlur(0.25))
    base.alpha_composite(ghost)
    base.paste(original_foreground, (0, 0), subject_soft_mask())

    glow_text(base, (142, 88), "MELLOW LONGPLAY  ·  S01 E01", f["eyebrow"], BROWN, stroke_width=1, glow_radius=1.5, glow_alpha=56)
    draw.line((72, 142, 650, 142), fill=HONEY, width=3)
    draw.ellipse((672, 137, 684, 149), fill=HONEY)

    glow_text(base, (70, 188), "Soft Vocal\nLongplay", f["title"], INK, stroke_width=2, glow_radius=2.2, glow_alpha=88, spacing=4)
    glow_text(base, (76, 366), "After-School First Love", f["subtitle"], SOFT_BROWN, stroke_width=1, glow_radius=1.7, glow_alpha=58)

    pill = Image.new("RGBA", base.size, (0, 0, 0, 0))
    pill_draw = ImageDraw.Draw(pill, "RGBA")
    pill_draw.rounded_rectangle((74, 465, 390, 521), radius=28, fill=CREAM, outline=(194, 132, 54, 128), width=2)
    base.alpha_composite(pill)
    glow_text(base, (104, 481), "41-min cozy mix", f["small"], BROWN, stroke_width=0, glow_radius=1.1, glow_alpha=36)
    draw_waveform(ImageDraw.Draw(base, "RGBA"), 434, 493)


def draw_big_brand_depth(
    base: Image.Image,
    original_foreground: Image.Image,
    f: dict[str, ImageFont.FreeTypeFont | ImageFont.ImageFont],
) -> None:
    typography = Image.new("RGBA", base.size, (0, 0, 0, 0))
    tdraw = ImageDraw.Draw(typography, "RGBA")
    tdraw.text(
        (72, 72),
        "MELLOW",
        font=f["brand_top"],
        fill=(96, 64, 42, 130),
        stroke_width=2,
        stroke_fill=(255, 239, 218, 70),
    )
    tdraw.text(
        (72, 342),
        "LONGPLAY",
        font=f["brand_bottom"],
        fill=(96, 64, 42, 172),
        stroke_width=2,
        stroke_fill=(255, 239, 218, 104),
    )
    typography = typography.filter(ImageFilter.GaussianBlur(0.18))
    base.alpha_composite(typography)
    base.paste(original_foreground, (0, 0), subject_soft_mask())
    charm_glow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    cdraw = ImageDraw.Draw(charm_glow, "RGBA")
    cdraw.ellipse((276, 590, 358, 672), fill=(255, 210, 92, 34), outline=(196, 130, 42, 88), width=2)
    base.alpha_composite(charm_glow.filter(ImageFilter.GaussianBlur(4)))

    caption_draw = ImageDraw.Draw(base, "RGBA")
    caption_gap = 6
    caption_parts = (
        (BIG_BRAND_CAPTION_LEFT_NOTE, f["bottom_caption_note"]),
        (BIG_BRAND_CAPTION_TEXT, f["bottom_caption"]),
        (BIG_BRAND_CAPTION_RIGHT_NOTES, f["bottom_caption_note"]),
    )
    caption_widths = []
    for text, font in caption_parts:
        bbox = caption_draw.textbbox((0, 0), text, font=font)
        caption_widths.append(bbox[2] - bbox[0])
    caption_x = (WIDTH - (sum(caption_widths) + caption_gap * 2)) // 2
    caption_y = 652
    caption_glow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(caption_glow, "RGBA")
    draw_x = caption_x
    for (text, font), width in zip(caption_parts, caption_widths):
        glow_draw.text(
            (draw_x + 1, caption_y + 2),
            text,
            font=font,
            fill=(0, 0, 0, 108),
        )
        draw_x += width + caption_gap
    base.alpha_composite(caption_glow.filter(ImageFilter.GaussianBlur(2.4)))
    draw_x = caption_x
    for (text, font), width in zip(caption_parts, caption_widths):
        caption_draw.text(
            (draw_x, caption_y),
            text,
            font=font,
            fill=(255, 255, 255, 226),
        )
        draw_x += width + caption_gap


def compose_thumbnail(background_path: Path, *, layout: str = LAYOUT_ORIGINAL) -> Image.Image:
    if layout not in LAYOUTS:
        raise ValueError(f"unknown thumbnail layout: {layout}")
    with Image.open(background_path) as source:
        original = cover_resize(source).convert("RGBA")
    base = original.copy()
    base = ImageEnhance.Color(base).enhance(1.04)
    base = ImageEnhance.Contrast(base).enhance(1.03)
    if layout != LAYOUT_BIG_BRAND_DEPTH:
        draw_warm_readability_layer(base)

    draw = ImageDraw.Draw(base, "RGBA")
    f = fonts()
    if layout == LAYOUT_BIG_BRAND_DEPTH:
        draw_big_brand_depth(base, original, f)
    elif layout == LAYOUT_SOFT_DEPTH:
        draw_headphone_icon(draw, 72, 82)
        draw_soft_depth_copy(base, original, draw, f)
    elif layout == LAYOUT_MUSIC_PLAYLIST:
        draw_headphone_icon(draw, 72, 82)
        draw_music_playlist_copy(base, draw, f)
    else:
        draw_headphone_icon(draw, 72, 82)
        draw_original_copy(base, draw, f)

    return base.convert("RGB")


def save_jpeg_under_limit(image: Image.Image, output_path: Path) -> int:
    for quality in range(92, 69, -4):
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=quality, optimize=True, progressive=True)
        data = buffer.getvalue()
        if len(data) <= YOUTUBE_THUMBNAIL_MAX_BYTES:
            output_path.write_bytes(data)
            return len(data)
    raise ValueError("thumbnail JPEG could not be saved under the YouTube 2 MB limit")


def create_thumbnail(
    background_path: Path | str = DEFAULT_BACKGROUND,
    output_path: Path | str = DEFAULT_OUTPUT,
    *,
    enforce_output_root: bool = False,
    layout: str = LAYOUT_ORIGINAL,
) -> dict[str, object]:
    background = project_path(background_path)
    output = project_path(output_path)
    assert_no_control_chars(background)
    assert_no_control_chars(output)
    if enforce_output_root:
        assert_allowed_output_root(output.parent)
    if not background.is_file():
        raise FileNotFoundError(f"background image not found: {background}")

    output.parent.mkdir(parents=True, exist_ok=True)
    image = compose_thumbnail(background, layout=layout)
    byte_count = save_jpeg_under_limit(image, output)
    return {
        "episode_id": EPISODE_ID,
        "background_path": str(background.relative_to(PROJECT_ROOT) if PROJECT_ROOT in [background, *background.parents] else background),
        "output_path": str(output.relative_to(PROJECT_ROOT) if PROJECT_ROOT in [output, *output.parents] else output),
        "width": image.width,
        "height": image.height,
        "bytes": byte_count,
        "mime_type": "image/jpeg",
        "layout": layout,
        "source_only_boundary": "local_thumbnail_from_existing_G_png_no_provider_or_platform_action",
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--background", type=Path, default=DEFAULT_BACKGROUND, help="Existing local background image")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Thumbnail JPEG output path")
    parser.add_argument("--layout", choices=LAYOUTS, default=LAYOUT_ORIGINAL, help="Text/layout variant to render")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    summary = create_thumbnail(args.background, args.output, enforce_output_root=True, layout=args.layout)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
