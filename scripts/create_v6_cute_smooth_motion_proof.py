#!/usr/bin/env python3
"""Create V6 cute/smooth local animated proof for S01E01.

V6 keeps the full header but changes typography, redraws the headphone icon as
an anti-aliased line-vector mark, slows parallax to near-still, adds subtle
local hair/leaf movement, smooths the audio-reactive waveform, and slides the
track title in/out from behind the vertical divider. It is a local proof only and
does not call provider APIs, open browsers, upload files, or claim full
render/export/release readiness.
"""

from __future__ import annotations

import argparse
import array
import math
import subprocess
import wave
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont
from leo_resource_paths import resolve_candidates_root

import create_visual_layout_mockups as static
import create_v5_readable_motion_proof as v5


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LEO_CANDIDATES_ROOT = resolve_candidates_root(PROJECT_ROOT)
DEFAULT_AUDIO = LEO_CANDIDATES_ROOT / "s01e01-campus-cafe-longplay/audio/selected/aud-t01_c02--margin-notes-at-table-three.wav"
DEFAULT_OUTPUT = LEO_CANDIDATES_ROOT / "s01e01-campus-cafe-longplay/visual/proofs/animated-v6/s01e01-vis-c01-v6-cute-smooth-motion-proof-30s-01.mp4"
WIDTH = static.WIDTH
HEIGHT = static.HEIGHT

INK = (62, 48, 38, 238)
BROWN = (101, 78, 59, 226)
SOFT_BROWN = (134, 93, 61, 214)
HONEY = (178, 126, 56, 176)
CREAM = (255, 239, 213, 170)


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
    cute = ["/System/Library/Fonts/Supplemental/ChalkboardSE.ttc", "/System/Library/Fonts/Avenir Next.ttc"]
    return {
        "header": load_font(cute, 27),
        "now": load_font(["/System/Library/Fonts/MarkerFelt.ttc", "/System/Library/Fonts/NewYorkItalic.ttf"], 25),
        "track": load_font(cute, 34),
        "subtitle": load_font(cute, 41),
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


def translate(image: Image.Image, dx: float, dy: float) -> Image.Image:
    return image.transform(
        (WIDTH, HEIGHT),
        Image.Transform.AFFINE,
        (1, 0, -dx, 0, 1, -dy),
        resample=Image.Resampling.BICUBIC,
    )


def slow_parallax(image: Image.Image, t: float) -> Image.Image:
    zoom = 1.004
    dx = math.sin(t * 0.055) * 1.15
    dy = math.cos(t * 0.045) * 0.65
    return image.transform(
        (WIDTH, HEIGHT),
        Image.Transform.AFFINE,
        (
            1 / zoom,
            0,
            WIDTH / 2 - WIDTH / (2 * zoom) - dx,
            0,
            1 / zoom,
            HEIGHT / 2 - HEIGHT / (2 * zoom) - dy,
        ),
        resample=Image.Resampling.BICUBIC,
    )


def text_soft(
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
    ImageDraw.Draw(layer, "RGBA").multiline_text(
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


def antialiased_headphones() -> Image.Image:
    scale = 4
    w = 94 * scale
    h = 92 * scale
    icon = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(icon, "RGBA")
    c = (104, 79, 59, 220)
    soft = (104, 79, 59, 118)
    def box(values: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
        return tuple(v * scale for v in values)

    draw.arc(box((14, 9, 80, 74)), start=204, end=336, fill=c, width=4 * scale)
    draw.arc(box((24, 20, 70, 68)), start=214, end=326, fill=soft, width=2 * scale)
    draw.rounded_rectangle(box((8, 42, 24, 75)), radius=7 * scale, outline=c, width=4 * scale)
    draw.rounded_rectangle(box((70, 42, 86, 75)), radius=7 * scale, outline=c, width=4 * scale)
    draw.arc(box((14, 48, 36, 76)), start=115, end=250, fill=soft, width=2 * scale)
    draw.arc(box((58, 48, 80, 76)), start=290, end=65, fill=soft, width=2 * scale)
    draw.ellipse(box((41, 76, 45, 80)), fill=(180, 129, 62, 156))
    draw.line(box((43, 77, 53, 77)), fill=(180, 129, 62, 120), width=1 * scale)
    return icon.resize((94, 92), Image.Resampling.LANCZOS)


def header_static_layer() -> Image.Image:
    f = fonts()
    layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    layer.alpha_composite(antialiased_headphones(), (72, 70))
    draw = ImageDraw.Draw(layer, "RGBA")
    draw.line((190, 78, 190, 202), fill=(178, 126, 56, 112), width=2)
    x = 224
    text_soft(layer, (x, 88), "MELLOW LONGPLAY  •  S01 - E01", f["header"], BROWN, stroke_width=0)
    text_soft(layer, (x, 130), "Now Playing", f["now"], SOFT_BROWN, stroke_width=0)
    draw.line((x, 226, x + 516, 226), fill=(178, 126, 56, 118), width=2)
    draw.ellipse((x + 524, 221, x + 534, 231), fill=(178, 126, 56, 160))
    return layer


def draw_sliding_track_title(image: Image.Image, t: float) -> None:
    f = fonts()
    layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    target_x = 224
    in_progress = fade(t, 0.48, 1.65)
    out_progress = fade(t, 28.72, 29.88)
    x = int(target_x - (1.0 - in_progress) * 360 - out_progress * 360)
    alpha = int(238 * fade(t, 0.38, 1.1) * fade_out(t, 28.72, 29.88))
    text_soft(layer, (x, 168), "01 - Margin Notes at Table Three", f["track"], (62, 48, 38, alpha), stroke_width=1)
    mask = Image.new("L", (WIDTH, HEIGHT), 0)
    ImageDraw.Draw(mask).rectangle((198, 0, WIDTH, 290), fill=255)
    layer.putalpha(Image.composite(layer.getchannel("A"), Image.new("L", (WIDTH, HEIGHT), 0), mask))
    image.alpha_composite(layer)


def audio_energy(path: Path, fps: int, duration: float) -> list[float]:
    with wave.open(str(path), "rb") as wav:
        sample_width = wav.getsampwidth()
        channels = wav.getnchannels()
        rate = wav.getframerate()
        total = min(wav.getnframes(), int(duration * rate))
        raw = wav.readframes(total)
    if sample_width != 2 or not raw:
        return [0.24 for _ in range(int(duration * fps))]

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

    sorted_values = sorted(values)
    p95 = sorted_values[int(len(sorted_values) * 0.95)] or max(values) or 1.0
    normalized = [min(1.0, value / p95) for value in values]
    smoothed: list[float] = []
    prev = 0.0
    for value in normalized:
        rate_value = 0.055 if value > prev else 0.032
        prev += (value - prev) * rate_value
        smoothed.append(prev)

    averaged: list[float] = []
    radius = max(1, int(fps * 0.35))
    for index in range(len(smoothed)):
        start = max(0, index - radius)
        end = min(len(smoothed), index + radius + 1)
        averaged.append(sum(smoothed[start:end]) / (end - start))
    return averaged


def make_motion_masks() -> tuple[Image.Image, Image.Image]:
    hair = Image.new("L", (WIDTH, HEIGHT), 0)
    hd = ImageDraw.Draw(hair)
    hd.ellipse((820, 70, 1325, 610), fill=46)
    hd.polygon([(770, 190), (1070, 90), (1280, 420), (1170, 710), (835, 545)], fill=42)
    hair = hair.filter(ImageFilter.GaussianBlur(28))

    leaves = Image.new("L", (WIDTH, HEIGHT), 0)
    ld = ImageDraw.Draw(leaves)
    ld.ellipse((1510, 30, 1940, 390), fill=82)
    ld.ellipse((1600, 710, 1960, 1110), fill=112)
    ld.polygon([(1770, 420), (1920, 470), (1920, 840), (1705, 755)], fill=60)
    leaves = leaves.filter(ImageFilter.GaussianBlur(22))
    return hair, leaves


def apply_local_motion(image: Image.Image, t: float, hair_mask: Image.Image, leaves_mask: Image.Image) -> Image.Image:
    hair_dx = math.sin(t * 0.42) * 0.72
    hair_dy = math.cos(t * 0.37) * 0.28
    leaf_dx = math.sin(t * 0.36 + 0.8) * 1.85
    leaf_dy = math.cos(t * 0.31) * 0.95
    moved = Image.composite(translate(image, hair_dx, hair_dy), image, hair_mask)
    moved = Image.composite(translate(moved, leaf_dx, leaf_dy), moved, leaves_mask)
    return moved


def particle_specs() -> list[tuple[float, float, float, float, float, int]]:
    rng = __import__("random").Random(606)
    return [
        (
            rng.triangular(20, WIDTH - 20, 460),
            rng.triangular(10, HEIGHT - 40, 280),
            rng.uniform(0.8, 3.0),
            rng.uniform(4.0, 10.0),
            rng.uniform(0.8, 3.4),
            int(rng.uniform(9, 34)),
        )
        for _ in range(120)
    ]


def draw_particles(image: Image.Image, specs: list[tuple[float, float, float, float, float, int]], t: float) -> None:
    layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    for x, y, r, speed, wobble, alpha in specs:
        px = x + math.sin(t * 0.38 + y * 0.015) * wobble
        py = ((y - t * speed) % (HEIGHT + 80)) - 40
        draw.ellipse((px - r, py - r, px + r, py + r), fill=(255, 222, 172, alpha))
    image.alpha_composite(layer.filter(ImageFilter.GaussianBlur(0.22)))


def draw_steam(image: Image.Image, t: float) -> None:
    layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    for index, x0 in enumerate((1390, 1410, 1430)):
        points = []
        for step in range(32):
            k = step / 31
            x = x0 + math.sin(k * 6.3 + t * 0.42 + index) * (5 + index)
            y = 762 - k * (84 + index * 8)
            points.append((x, y))
        draw.line(points, fill=(255, 240, 215, 24 + index * 4), width=3)
    image.alpha_composite(layer.filter(ImageFilter.GaussianBlur(3.2)))


def draw_light_sweep(image: Image.Image, t: float) -> None:
    layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    x = -180 + (t * 10) % (WIDTH + 360)
    draw.polygon(
        [(x, -80), (x + 170, -80), (x + 610, HEIGHT + 80), (x + 440, HEIGHT + 80)],
        fill=(255, 230, 178, 12),
    )
    image.alpha_composite(layer.filter(ImageFilter.GaussianBlur(54)))


def draw_smooth_equalizer(image: Image.Image, energy: float, t: float) -> None:
    layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    base_x = 1452
    base_y = 918
    width = 430
    phase = t * 0.32
    amp = 6.0 + 18.0 * energy
    for band, offset in enumerate((-16, 0, 16)):
        points = []
        for index in range(170):
            u = index / 169
            x = base_x + width * u
            arc = 32 * math.sin(u * math.pi * 0.78)
            wave = amp * math.sin(u * math.tau * 2.1 + phase + band * 0.55)
            y = base_y + arc + offset + wave
            points.append((x, y))
        draw.line(points, fill=(178, 126, 56, 62 + band * 10), width=2 if band != 1 else 3)
    for index in range(18):
        u = index / 17
        x = base_x + width * u
        arc = 32 * math.sin(u * math.pi * 0.78)
        y = base_y + arc + amp * math.sin(u * math.tau * 2.1 + phase)
        r = 2.5 + 3.2 * energy * (0.65 + 0.35 * math.sin(phase + index * 0.8))
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(184, 131, 62, int(98 + 58 * energy)))
    image.alpha_composite(layer.filter(ImageFilter.GaussianBlur(0.28)))


def active_subtitle(t: float) -> tuple[v5.Cue, float] | None:
    for cue in v5.SUBTITLE_CUES:
        if cue.start <= t <= cue.end:
            alpha = min(fade(t, cue.start, cue.start + 0.32), fade_out(t, cue.end - 0.26, cue.end))
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
    cy = 500 + math.sin(t * 0.25) * 1.3
    haze = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    hz = ImageDraw.Draw(haze, "RGBA")
    hz.rounded_rectangle(
        (cx - text_w / 2 - 34, cy - text_h / 2 - 22, cx + text_w / 2 + 34, cy + text_h / 2 + 22),
        radius=30,
        fill=(255, 238, 211, int(30 * alpha)),
    )
    layer.alpha_composite(haze.filter(ImageFilter.GaussianBlur(14)))
    text_soft(layer, (int(cx), int(cy - text_h / 2)), cue.text, f, (55, 44, 36, int(236 * alpha)), anchor="ma", align="center", spacing=10)
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
    base = Image.alpha_composite(base, Image.new("RGBA", (WIDTH, HEIGHT), (255, 242, 220, 7)))
    header = header_static_layer()
    hair_mask, leaves_mask = make_motion_masks()
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
        image = slow_parallax(base, t)
        image = apply_local_motion(image, t, hair_mask, leaves_mask)
        draw_light_sweep(image, t)
        draw_particles(image, particles, t)
        draw_steam(image, t)
        draw_smooth_equalizer(image, energies[min(frame, len(energies) - 1)], t)
        image.alpha_composite(apply_alpha(header, fade(t, 0.16, 1.0)))
        draw_sliding_track_title(image, t)
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
