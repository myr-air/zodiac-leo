#!/usr/bin/env python3
"""Create high-fidelity layered premium YouTube thumbnails for Mellow Longplay.

This command-line tool implements the authoritative visual design system approved
by the user (D138/D011). It layers the brand header, episode identifier, uppercase
Georgia-based extrabold titles, and bottom badges behind the right-side listener
character using a feathered soft alpha mask to achieve depth.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Widescreen dimensions
WIDTH = 1280
HEIGHT = 720

# System Fonts (macOS default locations)
SERIF_FONT_PATH = "/System/Library/Fonts/Supplemental/Georgia.ttf"
SERIF_ITALIC_FONT_PATH = "/System/Library/Fonts/Supplemental/Georgia Italic.ttf"
SANS_FONT_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"
SANS_BOLD_FONT_PATH = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"


def get_default_font(font_path: str, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Safely loads a TTF font, falling back to a default bitmap font if missing."""
    try:
        return ImageFont.truetype(font_path, size)
    except OSError:
        return ImageFont.load_default()


def subject_soft_mask() -> Image.Image:
    """Returns the soft alpha mask for the right-side listener character to achieve depth layering."""
    mask = Image.new("L", (WIDTH, HEIGHT), 0)
    draw = ImageDraw.Draw(mask)
    # Head and upper body soft bounding ellipse masks matching S01E01 and S01E02 character placements
    draw.ellipse((512, 44, 1038, 676), fill=212)
    draw.ellipse((658, 16, 940, 348), fill=235)
    draw.rounded_rectangle((602, 238, 1120, 694), radius=118, fill=176)
    return mask.filter(ImageFilter.GaussianBlur(22))


def draw_spaced_text(
    draw: ImageDraw.ImageDraw,
    position: tuple[int, int],
    text: str,
    font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
    fill: tuple[int, int, int, int],
    letter_spacing: int = 10,
    line_spacing: int = 34,
    stroke_width: int = 0,
    stroke_fill: tuple[int, int, int, int] | None = None
) -> None:
    """Draws custom letter-spaced multiline text in Pillow with optional stroke for extrabold weight."""
    x_start, y = position
    lines = text.split("\n")
    for i, line in enumerate(lines):
        current_x = x_start
        line_y = y + i * (font.size + line_spacing)
        for char in line:
            draw.text(
                (current_x, line_y),
                char,
                fill=fill,
                font=font,
                stroke_width=stroke_width,
                stroke_fill=stroke_fill
            )
            char_w = draw.textlength(char, font=font)
            current_x += char_w + letter_spacing


def draw_badge(
    draw: ImageDraw.ImageDraw,
    center_x: float,
    center_y: float,
    radius: float,
    bg_color: tuple[int, int, int, int],
    border_color: tuple[int, int, int, int],
    label: str,
    icon_type: str
) -> None:
    """Draws a beautiful, color-matched glassmorphic seal badge with soft borders and delicate outlines."""
    # 1. Soft badge drop shadow (to make it float off the background artwork)
    for offset in range(3, 0, -1):
        alpha = int(10 * (4 - offset))
        draw.ellipse(
            [
                center_x - radius - offset,
                center_y - radius - offset + 1,
                center_x + radius + offset,
                center_y + radius + offset + 1
            ],
            fill=(30, 20, 15, alpha)
        )

    # 2. Glassmorphic cream-white/pastel background (with semi-transparency)
    r, g, b = bg_color[:3]
    glass_color = (r, g, b, 205)  # semi-transparent color-matched base
    draw.ellipse([center_x - radius, center_y - radius, center_x + radius, center_y + radius], fill=glass_color)

    # 3. Outer border ring matched to the image palette
    draw.ellipse([center_x - radius, center_y - radius, center_x + radius, center_y + radius], outline=border_color, width=1)

    # 4. Draw high-precision outline icon
    icon_color = (62, 45, 28, 235)  # Dark bronze
    icon_w = 2  # Thinner line weight for elegant feel

    if icon_type == "cafe":
        # Coffee cup
        draw.rectangle([center_x - 12, center_y - 3, center_x + 8, center_y + 9], outline=icon_color, width=icon_w)
        draw.arc([center_x + 4, center_y - 1, center_x + 14, center_y + 7], -90, 90, fill=icon_color, width=icon_w)
        draw.line([center_x - 16, center_y + 11, center_x + 12, center_y + 11], fill=icon_color, width=icon_w)
        draw.line([center_x - 6, center_y - 10, center_x - 6, center_y - 6], fill=icon_color, width=icon_w)
        draw.line([center_x - 1, center_y - 11, center_x - 1, center_y - 7], fill=icon_color, width=icon_w)
        draw.line([center_x + 4, center_y - 10, center_x + 4, center_y - 6], fill=icon_color, width=icon_w)

    elif icon_type == "retro":
        # Vinyl record
        draw.ellipse([center_x - 13, center_y - 13, center_x + 13, center_y + 13], outline=icon_color, width=icon_w)
        draw.ellipse([center_x - 4, center_y - 4, center_x + 4, center_y + 4], outline=icon_color, width=icon_w)
        draw.ellipse([center_x - 1, center_y - 1, center_x + 1, center_y + 1], fill=icon_color)

    elif icon_type == "playlist":
        # Play button
        draw.ellipse([center_x - 14, center_y - 14, center_x + 14, center_y + 14], outline=icon_color, width=icon_w)
        draw.polygon([
            (center_x - 3, center_y - 6),
            (center_x - 3, center_y + 6),
            (center_x + 6, center_y)
        ], fill=icon_color)

    elif icon_type == "study":
        # Book
        draw.rectangle([center_x - 14, center_y - 10, center_x + 14, center_y + 8], outline=icon_color, width=icon_w)
        draw.line([center_x, center_y - 10, center_x, center_y + 8], fill=icon_color, width=icon_w)
        draw.line([center_x - 10, center_y - 4, center_x - 4, center_y - 4], fill=icon_color, width=1)
        draw.line([center_x - 10, center_y, center_x - 4, center_y], fill=icon_color, width=1)
        draw.line([center_x + 4, center_y - 4, center_x + 10, center_y - 4], fill=icon_color, width=1)
        draw.line([center_x + 4, center_y, center_x + 10, center_y], fill=icon_color, width=1)

    elif icon_type == "classic":
        # Headphones
        draw.arc([center_x - 12, center_y - 12, center_x + 12, center_y + 4], 180, 360, fill=icon_color, width=icon_w)
        draw.rounded_rectangle([center_x - 15, center_y - 2, center_x - 9, center_y + 9], radius=2, outline=icon_color, width=icon_w)
        draw.rounded_rectangle([center_x + 9, center_y - 2, center_x + 15, center_y + 9], radius=2, outline=icon_color, width=icon_w)

    # 5. Spaced label
    font = get_default_font(SANS_FONT_PATH, 11)
    label_color = (62, 45, 28, 235)
    spaced_label = " ".join(list(label))
    label_w = draw.textlength(spaced_label, font=font)

    # Spacing between icon circle and text label: 18px
    text_y_offset = 18
    draw.text((center_x - label_w/2 + 1, center_y + radius + text_y_offset + 1), spaced_label, fill=(255, 255, 255, 180), font=font)
    draw.text((center_x - label_w/2, center_y + radius + text_y_offset), spaced_label, fill=label_color, font=font)


def draw_bottom_white_caption(image: Image.Image, text: str) -> None:
    """Draws a premium centered white caption at the bottom of the image with a beautiful soft dark shadow."""
    draw = ImageDraw.Draw(image, "RGBA")
    font_caption = get_default_font(SANS_FONT_PATH, 22)
    font_note = get_default_font(SANS_BOLD_FONT_PATH, 24)

    caption_parts = [
        ("♪", font_note),
        (" " + text + " ", font_caption),
        ("♫ ♬", font_note)
    ]

    # Calculate widths and coordinates
    widths = []
    for t_part, f_part in caption_parts:
        bbox = draw.textbbox((0, 0), t_part, font=f_part)
        widths.append(bbox[2] - bbox[0])

    total_w = sum(widths)
    start_x = (WIDTH - total_w) // 2
    caption_y = 650

    # Draw soft shadow layer
    shadow_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow_layer, "RGBA")
    draw_x = start_x
    for (t_part, f_part), w_part in zip(caption_parts, widths):
        shadow_draw.text((draw_x + 1, caption_y + 2), t_part, fill=(0, 0, 0, 160), font=f_part)
        draw_x += w_part

    image.alpha_composite(shadow_layer.filter(ImageFilter.GaussianBlur(2.0)))

    # Draw sharp white text layer
    draw_sharp = ImageDraw.Draw(image, "RGBA")
    draw_x = start_x
    for (t_part, f_part), w_part in zip(caption_parts, widths):
        draw_sharp.text((draw_x, caption_y), t_part, fill=(255, 255, 255, 240), font=f_part)
        draw_x += w_part


def create_s01e01(base_resized: Image.Image, text_canvas: ImageDraw.ImageDraw, layered: Image.Image, fill_color: tuple[int, int, int, int] | int | None = None) -> None:
    """Specifies colors and elements for Campus Cafe."""
    if fill_color is None:
        fill_color = (76, 56, 42, 255)
    font_title = get_default_font(SERIF_FONT_PATH, 62)
    font_header = get_default_font(SERIF_ITALIC_FONT_PATH, 25)

    # Brand name "mellow longplay"
    text_canvas.text((60, 60), "mellow longplay", fill=fill_color, font=font_header)

    # Title
    title_text = "CAMPUS CAFE\nPLAYLIST"
    title_y = 185
    draw_spaced_text(
        text_canvas,
        (60, title_y),
        title_text,
        font_title,
        fill=fill_color,
        letter_spacing=10,
        line_spacing=34,
        stroke_width=3,
        stroke_fill=fill_color
    )

    # Badges
    if isinstance(fill_color, tuple):
        sage = (216, 226, 208, 240)
        rose = (235, 216, 212, 240)
        sand = (242, 230, 212, 240)
        border_color = (162, 134, 102, 160)
        draw_badges = ImageDraw.Draw(layered, "RGBA")
        badge_y = 540
        draw_badge(draw_badges, center_x=100, center_y=badge_y, radius=32, bg_color=sage, border_color=border_color, label="CAFÉ", icon_type="cafe")
        draw_badge(draw_badges, center_x=220, center_y=badge_y, radius=32, bg_color=rose, border_color=border_color, label="RETRO", icon_type="retro")
        draw_badge(draw_badges, center_x=340, center_y=badge_y, radius=32, bg_color=sand, border_color=border_color, label="PLAYLIST", icon_type="playlist")


def create_s01e02(base_resized: Image.Image, text_canvas: ImageDraw.ImageDraw, layered: Image.Image, fill_color: tuple[int, int, int, int] | int | None = None) -> None:
    """Specifies colors and elements for Classroom Window."""
    if fill_color is None:
        fill_color = (42, 34, 52, 255)
    font_title = get_default_font(SERIF_FONT_PATH, 62)
    font_header = get_default_font(SERIF_ITALIC_FONT_PATH, 25)

    # Brand name "mellow longplay"
    text_canvas.text((60, 60), "mellow longplay", fill=fill_color, font=font_header)

    # Title
    title_text = "CLASSROOM\nWINDOW"
    title_y = 185
    draw_spaced_text(
        text_canvas,
        (60, title_y),
        title_text,
        font_title,
        fill=fill_color,
        letter_spacing=10,
        line_spacing=34,
        stroke_width=3,
        stroke_fill=fill_color
    )

    # Badges
    if isinstance(fill_color, tuple):
        slate_blue = (202, 214, 224, 240)
        violet_indigo = (214, 208, 224, 240)
        moon_sand = (226, 222, 208, 240)
        border_color = (122, 136, 150, 160)
        draw_badges = ImageDraw.Draw(layered, "RGBA")
        badge_y = 540
        draw_badge(draw_badges, center_x=100, center_y=badge_y, radius=32, bg_color=slate_blue, border_color=border_color, label="STUDY", icon_type="study")
        draw_badge(draw_badges, center_x=220, center_y=badge_y, radius=32, bg_color=violet_indigo, border_color=border_color, label="CLASSIC", icon_type="classic")
        draw_badge(draw_badges, center_x=340, center_y=badge_y, radius=32, bg_color=moon_sand, border_color=border_color, label="PLAYLIST", icon_type="playlist")


def create_s01e03(base_resized: Image.Image, text_canvas: ImageDraw.ImageDraw, layered: Image.Image, fill_color: tuple[int, int, int, int] | int | None = None) -> None:
    """Specifies colors and elements for Rooftop Golden Hour."""
    if fill_color is None:
        fill_color = (78, 52, 38, 255)
    font_title = get_default_font(SERIF_FONT_PATH, 62)
    font_header = get_default_font(SERIF_ITALIC_FONT_PATH, 25)

    # Brand name "mellow longplay"
    text_canvas.text((60, 60), "mellow longplay", fill=fill_color, font=font_header)

    # Title
    title_text = "ROOFTOP\nGOLDEN HOUR"
    title_y = 185
    draw_spaced_text(
        text_canvas,
        (60, title_y),
        title_text,
        font_title,
        fill=fill_color,
        letter_spacing=10,
        line_spacing=34,
        stroke_width=3,
        stroke_fill=fill_color
    )

    # Badges
    if isinstance(fill_color, tuple):
        apricot = (255, 222, 205, 240)
        lavender = (226, 218, 235, 240)
        gold = (253, 235, 205, 240)
        border_color = (170, 138, 115, 160)
        draw_badges = ImageDraw.Draw(layered, "RGBA")
        badge_y = 540
        draw_badge(draw_badges, center_x=100, center_y=badge_y, radius=32, bg_color=apricot, border_color=border_color, label="SUNSET", icon_type="retro")
        draw_badge(draw_badges, center_x=220, center_y=badge_y, radius=32, bg_color=lavender, border_color=border_color, label="COZY", icon_type="classic")
        draw_badge(draw_badges, center_x=340, center_y=badge_y, radius=32, bg_color=gold, border_color=border_color, label="PLAYLIST", icon_type="playlist")


def create_s01e04(base_resized: Image.Image, text_canvas: ImageDraw.ImageDraw, layered: Image.Image, fill_color: tuple[int, int, int, int] | int | None = None) -> None:
    """Specifies colors and elements for Bookstore Afternoon."""
    if fill_color is None:
        fill_color = (68, 48, 34, 255)
    font_title = get_default_font(SERIF_FONT_PATH, 62)
    font_header = get_default_font(SERIF_ITALIC_FONT_PATH, 25)

    # Brand name "mellow longplay"
    text_canvas.text((60, 60), "mellow longplay", fill=fill_color, font=font_header)

    # Title
    title_text = "BOOKSTORE\nAFTERNOON"
    title_y = 185
    draw_spaced_text(
        text_canvas,
        (60, title_y),
        title_text,
        font_title,
        fill=fill_color,
        letter_spacing=10,
        line_spacing=34,
        stroke_width=3,
        stroke_fill=fill_color
    )

    # Badges
    if isinstance(fill_color, tuple):
        paper_sand = (242, 228, 208, 240)
        sage = (212, 224, 208, 240)
        gold = (253, 235, 205, 240)
        border_color = (165, 135, 110, 160)
        draw_badges = ImageDraw.Draw(layered, "RGBA")
        badge_y = 540
        draw_badge(draw_badges, center_x=100, center_y=badge_y, radius=32, bg_color=paper_sand, border_color=border_color, label="READING", icon_type="study")
        draw_badge(draw_badges, center_x=220, center_y=badge_y, radius=32, bg_color=sage, border_color=border_color, label="COZY", icon_type="classic")
        draw_badge(draw_badges, center_x=340, center_y=badge_y, radius=32, bg_color=gold, border_color=border_color, label="PLAYLIST", icon_type="playlist")


def create_s01e05(base_resized: Image.Image, text_canvas: ImageDraw.ImageDraw, layered: Image.Image, fill_color: tuple[int, int, int, int] | int | None = None) -> None:
    """Specifies colors and elements for Apartment Window."""
    if fill_color is None:
        fill_color = (44, 48, 68, 255)
    font_title = get_default_font(SERIF_FONT_PATH, 62)
    font_header = get_default_font(SERIF_ITALIC_FONT_PATH, 25)

    # Brand name "mellow longplay"
    text_canvas.text((60, 60), "mellow longplay", fill=fill_color, font=font_header)

    # Title
    title_text = "APARTMENT\nWINDOW"
    title_y = 185
    draw_spaced_text(
        text_canvas,
        (60, title_y),
        title_text,
        font_title,
        fill=fill_color,
        letter_spacing=10,
        line_spacing=34,
        stroke_width=3,
        stroke_fill=fill_color
    )

    # Badges
    if isinstance(fill_color, tuple):
        paper_blue = (212, 220, 235, 240)
        sage = (212, 224, 208, 240)
        gold = (253, 235, 205, 240)
        border_color = (122, 136, 150, 160)
        draw_badges = ImageDraw.Draw(layered, "RGBA")
        badge_y = 540
        draw_badge(draw_badges, center_x=100, center_y=badge_y, radius=32, bg_color=paper_blue, border_color=border_color, label="RAINY", icon_type="classic")
        draw_badge(draw_badges, center_x=220, center_y=badge_y, radius=32, bg_color=sage, border_color=border_color, label="COZY", icon_type="classic")
        draw_badge(draw_badges, center_x=340, center_y=badge_y, radius=32, bg_color=gold, border_color=border_color, label="PLAYLIST", icon_type="playlist")


def process_episode(episode_id: str, background_path: Path, output_path: Path) -> None:
    """Executes the high-precision premium thumbnail generation process."""
    if not background_path.exists():
        print(f"Error: Background file '{background_path}' does not exist.")
        sys.exit(1)

    print(f"Intaking visual background: {background_path}")
    base = Image.open(background_path)
    base_resized = base.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS).convert("RGBA")
    original_foreground = base_resized.copy()

    # Create text canvas
    text_canvas = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw_text = ImageDraw.Draw(text_canvas)

    # Determine episode specific values
    if episode_id == "s01e01":
        glow_color = (255, 253, 248, 225)
        shadow_color = (38, 30, 22, 35)
        glow_blur = 16
        caption_text = "Cozy Chill Vocals for Coffee Breaks"
        tr_text = "S01E01"

        # Build layered base using text masks
        glow_mask = Image.new("L", (WIDTH, HEIGHT), 0)
        glow_mask_draw = ImageDraw.Draw(glow_mask)
        create_s01e01(base_resized, glow_mask_draw, base_resized, fill_color=255)

        blurred_glow_mask = glow_mask.filter(ImageFilter.GaussianBlur(glow_blur))
        glow_layer = Image.new("RGBA", (WIDTH, HEIGHT), glow_color)
        layered = Image.composite(glow_layer, base_resized, blurred_glow_mask)

        # Draw final clean text on top of the glow halo
        create_s01e01(base_resized, draw_text, layered)
        layered.alpha_composite(text_canvas)

    elif episode_id == "s01e02":
        glow_color = (255, 253, 248, 230)
        shadow_color = (15, 12, 10, 35)
        glow_blur = 18
        caption_text = "Cozy Chill Vocals for Study & Focus"
        tr_text = "S01E02"

        # Build layered base using text masks
        glow_mask = Image.new("L", (WIDTH, HEIGHT), 0)
        glow_mask_draw = ImageDraw.Draw(glow_mask)
        create_s01e02(base_resized, glow_mask_draw, base_resized, fill_color=255)

        blurred_glow_mask = glow_mask.filter(ImageFilter.GaussianBlur(glow_blur))
        glow_layer = Image.new("RGBA", (WIDTH, HEIGHT), glow_color)
        layered = Image.composite(glow_layer, base_resized, blurred_glow_mask)

        # Draw final clean text on top of the glow halo
        create_s01e02(base_resized, draw_text, layered)
        layered.alpha_composite(text_canvas)

    elif episode_id == "s01e03":
        glow_color = (255, 250, 240, 235)
        shadow_color = (48, 30, 20, 35)
        glow_blur = 18
        caption_text = "Cozy Chill Vocals for Late-Afternoon Wind"
        tr_text = "S01E03"

        # Build layered base using text masks
        glow_mask = Image.new("L", (WIDTH, HEIGHT), 0)
        glow_mask_draw = ImageDraw.Draw(glow_mask)
        create_s01e03(base_resized, glow_mask_draw, base_resized, fill_color=255)

        blurred_glow_mask = glow_mask.filter(ImageFilter.GaussianBlur(glow_blur))
        glow_layer = Image.new("RGBA", (WIDTH, HEIGHT), glow_color)
        layered = Image.composite(glow_layer, base_resized, blurred_glow_mask)

        # Draw final clean text on top of the glow halo
        create_s01e03(base_resized, draw_text, layered)
        layered.alpha_composite(text_canvas)

    elif episode_id == "s01e04":
        glow_color = (255, 252, 245, 235)
        shadow_color = (42, 32, 24, 35)
        glow_blur = 18
        caption_text = "Cozy Chill Vocals for Afternoon Reading & Quiet Hope"
        tr_text = "S01E04"

        # Build layered base using text masks
        glow_mask = Image.new("L", (WIDTH, HEIGHT), 0)
        glow_mask_draw = ImageDraw.Draw(glow_mask)
        create_s01e04(base_resized, glow_mask_draw, base_resized, fill_color=255)

        blurred_glow_mask = glow_mask.filter(ImageFilter.GaussianBlur(glow_blur))
        glow_layer = Image.new("RGBA", (WIDTH, HEIGHT), glow_color)
        layered = Image.composite(glow_layer, base_resized, blurred_glow_mask)

        # Draw final clean text on top of the glow halo
        create_s01e04(base_resized, draw_text, layered)
        layered.alpha_composite(text_canvas)

    elif episode_id == "s01e05":
        glow_color = (255, 253, 248, 230)
        shadow_color = (24, 28, 48, 35)
        glow_blur = 18
        caption_text = "Cozy Chill Vocals for Evening Study & Solitary Calm"
        tr_text = "S01E05"

        # Build layered base using text masks
        glow_mask = Image.new("L", (WIDTH, HEIGHT), 0)
        glow_mask_draw = ImageDraw.Draw(glow_mask)
        create_s01e05(base_resized, glow_mask_draw, base_resized, fill_color=255)

        blurred_glow_mask = glow_mask.filter(ImageFilter.GaussianBlur(glow_blur))
        glow_layer = Image.new("RGBA", (WIDTH, HEIGHT), glow_color)
        layered = Image.composite(glow_layer, base_resized, blurred_glow_mask)

        # Draw final clean text on top of the glow halo
        create_s01e05(base_resized, draw_text, layered)
        layered.alpha_composite(text_canvas)

    else:
        print(f"Error: Reusable configuration for episode '{episode_id}' is not implemented yet.")
        sys.exit(1)

    # Paste character shadow softly behind character
    shadow_canvas = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    solid_shadow = Image.new("RGBA", (WIDTH, HEIGHT), shadow_color)
    shadow_canvas.paste(solid_shadow, (0, 0), subject_soft_mask())
    blurred_shadow = shadow_canvas.filter(ImageFilter.GaussianBlur(28))

    offset_shadow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    offset_shadow.paste(blurred_shadow, (-14, 3))
    layered = Image.alpha_composite(layered, offset_shadow)

    # Paste original foreground character on top using soft blur mask (Depth effect)
    layered.paste(original_foreground, (0, 0), subject_soft_mask())

    # Draw S01EXX in top right corner
    font_top_right = get_default_font(SERIF_FONT_PATH, 25)
    tr_glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    tr_glow_draw = ImageDraw.Draw(tr_glow, "RGBA")
    tr_glow_draw.text(
        (WIDTH - 150, 60),
        tr_text,
        fill=(0, 0, 0, 0),
        font=font_top_right,
        stroke_width=4,
        stroke_fill=(shadow_color[0], shadow_color[1], shadow_color[2], 60 if episode_id == "s01e01" else 80)
    )
    layered = Image.alpha_composite(layered, tr_glow.filter(ImageFilter.GaussianBlur(2)))
    draw_final = ImageDraw.Draw(layered)
    draw_final.text((WIDTH - 150, 60), tr_text, fill=(255, 252, 245, 235), font=font_top_right)

    # Centered white bottom caption
    draw_bottom_white_caption(layered, caption_text)

    # Ensure output parent directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    layered.convert("RGB").save(output_path, "PNG")
    print(f"Success: Layered premium floating-text thumbnail saved to: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create Mellow Longplay layered premium thumbnails.")
    parser.add_argument("--episode", required=True, choices=["s01e01", "s01e02", "s01e03", "s01e04", "s01e05"], help="Episode identifier (s01e01, s01e02, s01e03, s01e04, or s01e05)")
    parser.add_argument("--background", required=True, type=Path, help="Path to input visual background illustration")
    parser.add_argument("--output", required=True, type=Path, help="Path to write the final 1280x720 PNG thumbnail")

    args = parser.parse_args()
    process_episode(args.episode, args.background, args.output)


if __name__ == "__main__":
    main()
