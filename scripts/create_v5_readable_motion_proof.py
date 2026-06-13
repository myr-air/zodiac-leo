#!/usr/bin/env python3
"""Create a revised readable-motion proof for S01E01 visual V5.

This local helper responds to the V4-07 proof review: keep the full header but
use more readable fonts, replace the blocky headphone icon with an original
line-vector icon, time subtitles to a Track 1 proof cue map, replace the brick
equalizer with a soft waveform ribbon, and add subtle parallax/steam/light
motion. It does not call provider APIs, open browsers, upload files, or claim
full render/export/release readiness.
"""

from __future__ import annotations

import argparse
import array
import math
import random
import subprocess
import wave
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont
from leo_resource_paths import resolve_candidates_root

import create_visual_layout_mockups as static


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LEO_CANDIDATES_ROOT = resolve_candidates_root(PROJECT_ROOT)
DEFAULT_AUDIO = LEO_CANDIDATES_ROOT / "s01e01-campus-cafe-longplay/audio/selected/aud-t01_c02--margin-notes-at-table-three.wav"
DEFAULT_OUTPUT = LEO_CANDIDATES_ROOT / "s01e01-campus-cafe-longplay/visual/proofs/animated-v5/s01e01-vis-c01-v5-readable-motion-proof-30s-01.mp4"
WIDTH = static.WIDTH
HEIGHT = static.HEIGHT

INK = (58, 47, 39, 236)
BROWN = (96, 73, 55, 224)
SOFT_BROWN = (130, 91, 59, 210)
HONEY = (177, 126, 56, 184)
CREAM = (255, 239, 211, 168)


@dataclass(frozen=True)
class Cue:
    start: float
    end: float
    text: str


SUBTITLE_CUES = [
    Cue(4.2, 8.4, "After school, the rain comes down\nOn the window by our seats"),
    Cue(8.7, 12.8, "You set your bag beside my chair\nAt our table, table three"),
    Cue(13.5, 17.4, "I draw a line beside my notes\nBlue pen moving left to right"),
    Cue(17.8, 22.0, "You ask what page the homework starts\nI say page twelve, then lose my line"),
    Cue(23.0, 26.8, "You write a question in the margin\nI write back small and take my time"),
    Cue(27.1, 30.0, "Your sleeve brushes my notebook corner\nMine stays close beside your line"),
]


def root_path(path: Path) -> Path:
    return path if path.is_absolute() else LEO_CANDIDATES_ROOT / path


def load_font(paths: list[str], size: int, index: int = 0) -> ImageFont.FreeTypeFont:
    for value in paths:
        path = Path(value)
        if not path.exists():
            continue
        try:
            return ImageFont.truetype(str(path), size=size, index=index)
        except OSError:
            continue
    return ImageFont.load_default(size=size)


def fonts() -> dict[str, ImageFont.FreeTypeFont]:
    return {
        "header": load_font(["/System/Library/Fonts/Avenir Next.ttc", "/System/Library/Fonts/HelveticaNeue.ttc"], 28),
        "now": load_font(["/System/Library/Fonts/NewYorkItalic.ttf", "/System/Library/Fonts/Supplemental/Georgia Italic.ttf"], 25),
        "track": load_font(["/System/Library/Fonts/Avenir Next.ttc", "/System/Library/Fonts/HelveticaNeue.ttc"], 35),
        "subtitle": load_font(["/System/Library/Fonts/Avenir Next.ttc", "/System/Library/Fonts/HelveticaNeue.ttc"], 43),
    }


def ease(x: float) -> float:
    x = max(0.0, min(1.0, x))
    return x * x * (3.0 - 2.0 * x)


def fade(t: float, start: float, end: float) -> float:
    return ease((t - start) / max(0.001, end - start))


def fade_out(t: float, start: float, end: float) -> float:
    return 1.0 - fade(t, start, end)


def apply_alpha(layer: Image.Image, alpha: float) -> Image.Image:
    alpha = max(0.0, min(1.0, alpha))
    if alpha >= 0.999:
        return layer
    result = layer.copy()
    result.putalpha(result.getchannel("A").point(lambda p: int(p * alpha)))
    return result


def audio_energy(path: Path, fps: int, duration: float) -> list[float]:
    with wave.open(str(path), "rb") as wav:
        sample_width = wav.getsampwidth()
        channels = wav.getnchannels()
        rate = wav.getframerate()
        total = min(wav.getnframes(), int(duration * rate))
        raw = wav.readframes(total)
    if sample_width != 2 or not raw:
        return [0.3 for _ in range(int(duration * fps))]

    samples = array.array("h")
    samples.frombytes(raw)
    if channels > 1:
        mono = array.array("h")
        for index in range(0, len(samples) - channels + 1, channels):
            mono.append(int(sum(samples[index : index + channels]) / channels))
        samples = mono

    values: list[float] = []
    frame_count = int(duration * fps)
    for frame in range(frame_count):
        start = int(frame * rate / fps)
        end = max(start + 1, int((frame + 1) * rate / fps))
        window = samples[start:end]
        if not window:
            values.append(0.0)
            continue
        rms = math.sqrt(sum(sample * sample for sample in window) / len(window)) / 32768.0
        values.append(rms)
    peak = max(values) or 1.0
    smoothed: list[float] = []
    prev = 0.0
    for value in values:
        normalized = min(1.0, value / peak)
        rate_value = 0.22 if normalized > prev else 0.08
        prev += (normalized - prev) * rate_value
        smoothed.append(prev)
    return smoothed


def draw_line_headphones(draw: ImageDraw.ImageDraw, x: int, y: int, alpha: int = 218) -> None:
    color = (103, 79, 61, alpha)
    draw.arc((x + 4, y + 2, x + 74, y + 70), start=204, end=336, fill=color, width=5)
    draw.arc((x + 13, y + 12, x + 65, y + 65), start=210, end=330, fill=(103, 79, 61, 126), width=2)
    draw.rounded_rectangle((x + 2, y + 42, x + 17, y + 74), radius=6, outline=color, width=4)
    draw.rounded_rectangle((x + 61, y + 42, x + 76, y + 74), radius=6, outline=color, width=4)
    draw.line((x + 18, y + 55, x + 26, y + 61), fill=(103, 79, 61, 132), width=3)
    draw.line((x + 60, y + 55, x + 52, y + 61), fill=(103, 79, 61, 132), width=3)


def text_with_soft_stroke(
    layer: Image.Image,
    xy: tuple[int, int],
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int, int],
    *,
    anchor: str | None = None,
    align: str = "left",
    spacing: int = 8,
    stroke_width: int = 1,
) -> None:
    draw = ImageDraw.Draw(layer, "RGBA")
    draw.multiline_text(
        xy,
        text,
        font=font,
        fill=fill,
        anchor=anchor,
        align=align,
        spacing=spacing,
        stroke_width=stroke_width,
        stroke_fill=CREAM,
    )


def header_layer() -> Image.Image:
    f = fonts()
    layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    draw_line_headphones(draw, 84, 76)
    draw.line((188, 78, 188, 202), fill=(176, 126, 66, 116), width=2)
    x = 224
    text_with_soft_stroke(layer, (x, 88), "MELLOW LONGPLAY  •  S01 - E01", f["header"], BROWN, stroke_width=0)
    text_with_soft_stroke(layer, (x, 130), "Now Playing", f["now"], SOFT_BROWN, stroke_width=0)
    text_with_soft_stroke(layer, (x, 168), "01 - Margin Notes at Table Three", f["track"], INK, stroke_width=1)
    draw.line((x, 226, x + 516, 226), fill=(177, 126, 56, 130), width=2)
    draw.ellipse((x + 524, 221, x + 534, 231), fill=(177, 126, 56, 168))
    return layer.filter(ImageFilter.GaussianBlur(0.05))


def moving_background(base: Image.Image, t: float) -> Image.Image:
    zoom = 1.012 + 0.004 * math.sin(t * 0.22)
    w = int(WIDTH * zoom)
    h = int(HEIGHT * zoom)
    enlarged = base.resize((w, h), Image.Resampling.LANCZOS)
    pan_x = int((w - WIDTH) / 2 + math.sin(t * 0.16) * 10)
    pan_y = int((h - HEIGHT) / 2 + math.cos(t * 0.13) * 6)
    return enlarged.crop((pan_x, pan_y, pan_x + WIDTH, pan_y + HEIGHT))


def particle_specs(seed: int = 505) -> list[tuple[float, float, float, float, float, int]]:
    rng = random.Random(seed)
    specs = []
    for _ in range(130):
        specs.append(
            (
                rng.triangular(20, WIDTH - 20, 460),
                rng.triangular(10, HEIGHT - 40, 280),
                rng.uniform(0.9, 3.2),
                rng.uniform(6.0, 15.0),
                rng.uniform(1.0, 4.5),
                int(rng.uniform(12, 44)),
            )
        )
    return specs


def draw_particles(image: Image.Image, specs: list[tuple[float, float, float, float, float, int]], t: float) -> None:
    layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    for x, y, r, speed, wobble, alpha in specs:
        px = x + math.sin(t * 0.52 + y * 0.02) * wobble
        py = ((y - t * speed) % (HEIGHT + 90)) - 45
        draw.ellipse((px - r, py - r, px + r, py + r), fill=(255, 222, 172, alpha))
    image.alpha_composite(layer.filter(ImageFilter.GaussianBlur(0.25)))


def draw_steam(image: Image.Image, t: float) -> None:
    layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    bases = [(1396, 750), (1415, 744), (1432, 752), (1382, 760)]
    for index, (x0, y0) in enumerate(bases):
        points = []
        for step in range(30):
            k = step / 29
            x = x0 + math.sin(k * 7.0 + t * 0.9 + index) * (8 + index * 2)
            y = y0 - k * (92 + index * 9)
            points.append((x, y))
        alpha = int(30 + 18 * math.sin(t * 0.7 + index) ** 2)
        draw.line(points, fill=(255, 240, 215, alpha), width=3)
    image.alpha_composite(layer.filter(ImageFilter.GaussianBlur(3.0)))


def draw_light_sweep(image: Image.Image, t: float) -> None:
    layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    x = -220 + (t * 34) % (WIDTH + 420)
    draw.polygon(
        [(x, -80), (x + 210, -80), (x + 690, HEIGHT + 80), (x + 480, HEIGHT + 80)],
        fill=(255, 230, 178, 18),
    )
    image.alpha_composite(layer.filter(ImageFilter.GaussianBlur(42)))


def draw_soft_equalizer(image: Image.Image, energy: float, t: float) -> None:
    layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    base_x = 1450
    base_y = 920
    width = 430
    for band, offset in enumerate((-18, 0, 18)):
        points = []
        for index in range(150):
            u = index / 149
            x = base_x + width * u
            curve = 34 * math.sin(u * math.pi * 0.78)
            wave = (11 + 22 * energy) * math.sin(u * math.tau * 2.6 + t * (1.0 + band * 0.16))
            y = base_y + curve + offset + wave
            points.append((x, y))
        alpha = 62 - band * 8
        draw.line(points, fill=(177, 126, 56, alpha), width=3 if band == 1 else 2)
    for index in range(22):
        u = index / 21
        x = base_x + width * u
        curve = 34 * math.sin(u * math.pi * 0.78)
        pulse = 0.5 + 0.5 * math.sin(t * 2.1 + index * 0.9)
        y = base_y + curve + (14 + 24 * energy) * math.sin(u * math.tau * 2.4 + t * 1.2)
        r = 2.4 + 5.5 * energy * pulse
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(183, 130, 61, int(68 + 72 * energy * pulse)))
    image.alpha_composite(layer.filter(ImageFilter.GaussianBlur(0.3)))


def active_subtitle(t: float) -> tuple[Cue, float] | None:
    for cue in SUBTITLE_CUES:
        if cue.start <= t <= cue.end:
            alpha = min(fade(t, cue.start, cue.start + 0.28), fade_out(t, cue.end - 0.22, cue.end))
            return cue, alpha
    return None


def draw_subtitle(image: Image.Image, t: float) -> None:
    active = active_subtitle(t)
    if active is None:
        return
    cue, alpha = active
    f = fonts()["subtitle"]
    layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    bbox = draw.multiline_textbbox((0, 0), cue.text, font=f, spacing=10, stroke_width=1)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    cx = 430
    cy = 492 + math.sin(t * 0.55) * 2.5
    haze = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    hz = ImageDraw.Draw(haze, "RGBA")
    hz.rounded_rectangle(
        (cx - text_w / 2 - 36, cy - text_h / 2 - 22, cx + text_w / 2 + 36, cy + text_h / 2 + 22),
        radius=28,
        fill=(255, 238, 211, int(34 * alpha)),
    )
    layer.alpha_composite(haze.filter(ImageFilter.GaussianBlur(12)))
    text_with_soft_stroke(layer, (int(cx), int(cy - text_h / 2)), cue.text, f, (54, 43, 36, int(238 * alpha)), anchor="ma", align="center", spacing=10)
    image.alpha_composite(layer)


def render(args: argparse.Namespace) -> Path:
    background = root_path(args.background)
    audio = root_path(args.audio)
    output = root_path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    if not background.exists():
        raise FileNotFoundError(background)
    if not audio.exists():
        raise FileNotFoundError(audio)

    base = static.cover_resize(Image.open(background)).convert("RGBA")
    base = Image.alpha_composite(base, Image.new("RGBA", (WIDTH, HEIGHT), (255, 242, 220, 8)))
    header = header_layer()
    particles = particle_specs()
    energies = audio_energy(audio, args.fps, args.duration)
    frames = int(args.duration * args.fps)

    command = [
        "ffmpeg",
        "-y",
        "-f",
        "rawvideo",
        "-vcodec",
        "rawvideo",
        "-pix_fmt",
        "rgb24",
        "-s",
        f"{WIDTH}x{HEIGHT}",
        "-r",
        str(args.fps),
        "-i",
        "-",
        "-ss",
        "0",
        "-t",
        f"{args.duration:.3f}",
        "-i",
        str(audio),
        "-map",
        "0:v:0",
        "-map",
        "1:a:0",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "19",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "160k",
        "-shortest",
        str(output),
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    assert process.stdin is not None
    for frame in range(frames):
        t = frame / args.fps
        image = moving_background(base, t)
        draw_light_sweep(image, t)
        draw_particles(image, particles, t)
        draw_steam(image, t)
        draw_soft_equalizer(image, energies[min(frame, len(energies) - 1)], t)
        image.alpha_composite(apply_alpha(header, fade(t, 0.15, 1.0)))
        draw_subtitle(image, t)
        process.stdin.write(image.convert("RGB").tobytes())
    process.stdin.close()
    result = process.wait()
    if result != 0:
        raise RuntimeError(f"ffmpeg exited with {result}")
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--background", type=Path, default=static.BG_PATH)
    parser.add_argument("--audio", type=Path, default=DEFAULT_AUDIO)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--duration", type=float, default=30.0)
    parser.add_argument("--fps", type=int, default=24)
    args = parser.parse_args()
    output = render(args)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
