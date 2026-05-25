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
ALLOWED_OUTPUT_ROOTS = (DEFAULT_OUTPUT_ROOT,)

WIDTH = 1280
HEIGHT = 720
YOUTUBE_THUMBNAIL_MAX_BYTES = 2_000_000

INK = (64, 48, 38, 242)
BROWN = (103, 76, 55, 230)
SOFT_BROWN = (130, 93, 62, 215)
CREAM = (255, 242, 219, 230)
HONEY = (192, 129, 49, 210)


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


def compose_thumbnail(background_path: Path) -> Image.Image:
    with Image.open(background_path) as source:
        base = cover_resize(source).convert("RGBA")
    base = ImageEnhance.Color(base).enhance(1.04)
    base = ImageEnhance.Contrast(base).enhance(1.03)
    draw_warm_readability_layer(base)

    draw = ImageDraw.Draw(base, "RGBA")
    f = fonts()
    draw_headphone_icon(draw, 72, 82)
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
    image = compose_thumbnail(background)
    byte_count = save_jpeg_under_limit(image, output)
    return {
        "episode_id": EPISODE_ID,
        "background_path": str(background.relative_to(PROJECT_ROOT) if PROJECT_ROOT in [background, *background.parents] else background),
        "output_path": str(output.relative_to(PROJECT_ROOT) if PROJECT_ROOT in [output, *output.parents] else output),
        "width": image.width,
        "height": image.height,
        "bytes": byte_count,
        "mime_type": "image/jpeg",
        "source_only_boundary": "local_thumbnail_from_existing_G_png_no_provider_or_platform_action",
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--background", type=Path, default=DEFAULT_BACKGROUND, help="Existing local background image")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Thumbnail JPEG output path")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    summary = create_thumbnail(args.background, args.output, enforce_output_root=True)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
