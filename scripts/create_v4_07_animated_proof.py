#!/usr/bin/env python3
"""Create a short local animated proof for S01E01 V4-07.

This is a bounded local proof helper. It composites the approved local
background, V4-07 overlay treatment, subtle particles, and a low-amplitude
quarter equalizer onto a short Track 1 excerpt. It does not call provider APIs,
open browsers, upload files, or claim full render/export/release readiness.
"""

from __future__ import annotations

import argparse
import array
import math
import random
import subprocess
import wave
from pathlib import Path

from PIL import Image, ImageDraw

import create_visual_layout_mockups as static


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_AUDIO = Path("candidates/s01e01-campus-cafe-longplay/audio/selected/aud-t01_c02--margin-notes-at-table-three.wav")
DEFAULT_OUTPUT = Path("candidates/s01e01-campus-cafe-longplay/visual/proofs/animated-v4-07/s01e01-vis-c01-v4-07-animated-proof-15s-01.mp4")
WIDTH = static.WIDTH
HEIGHT = static.HEIGHT


def root_path(path: Path) -> Path:
    return path if path.is_absolute() else PROJECT_ROOT / path


def opacity(layer: Image.Image, value: float) -> Image.Image:
    value = max(0.0, min(1.0, value))
    if value >= 0.999:
        return layer
    result = layer.copy()
    alpha = result.getchannel("A").point(lambda p: int(p * value))
    result.putalpha(alpha)
    return result


def ease_in_out(x: float) -> float:
    x = max(0.0, min(1.0, x))
    return x * x * (3.0 - 2.0 * x)


def fade(t: float, start: float, end: float) -> float:
    return ease_in_out((t - start) / max(0.001, end - start))


def audio_energy(path: Path, fps: int, duration: float) -> list[float]:
    with wave.open(str(path), "rb") as wav:
        sample_width = wav.getsampwidth()
        channels = wav.getnchannels()
        rate = wav.getframerate()
        total = min(wav.getnframes(), int(duration * rate))
        raw = wav.readframes(total)
    if sample_width != 2 or not raw:
        return [0.35 for _ in range(int(duration * fps))]

    samples = array.array("h")
    samples.frombytes(raw)
    if channels > 1:
        mono = array.array("h")
        for index in range(0, len(samples) - channels + 1, channels):
            mono.append(int(sum(samples[index : index + channels]) / channels))
        samples = mono

    frame_count = int(duration * fps)
    values: list[float] = []
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
    normalized = [min(1.0, value / peak) for value in values]
    smoothed: list[float] = []
    prev = 0.0
    for value in normalized:
        attack = 0.26 if value > prev else 0.09
        prev = prev + (value - prev) * attack
        smoothed.append(prev)
    return smoothed


def build_base(background: Path) -> Image.Image:
    bg = static.cover_resize(Image.open(background))
    return Image.alpha_composite(bg, Image.new("RGBA", (WIDTH, HEIGHT), (255, 242, 220, 10)))


def build_overlay_layers() -> tuple[Image.Image, Image.Image, Image.Image]:
    fonts = static.fonts()
    top = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    static.top_left_block_reference(top, fonts)
    subtitle = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    static.subtitle_reference(subtitle, fonts)
    ornament = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    static.ornament(ornament)
    return top, subtitle, ornament


def particle_specs(seed: int = 407) -> list[tuple[float, float, float, float, float, int]]:
    rng = random.Random(seed)
    specs = []
    for _ in range(150):
        x = rng.triangular(20, WIDTH - 20, 430)
        y = rng.triangular(20, HEIGHT - 40, 300)
        r = rng.uniform(1.0, 3.7)
        speed = rng.uniform(4.0, 10.0)
        wobble = rng.uniform(0.2, 0.9)
        alpha = int(rng.uniform(14, 48))
        specs.append((x, y, r, speed, wobble, alpha))
    return specs


def draw_particles(image: Image.Image, specs: list[tuple[float, float, float, float, float, int]], t: float) -> None:
    layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    for x, y, r, speed, wobble, alpha in specs:
        px = x + math.sin(t * 0.45 + y * 0.017) * (2.0 + wobble)
        py = ((y - t * speed) % (HEIGHT + 80)) - 40
        pulse = 0.72 + 0.28 * math.sin(t * 0.8 + x * 0.01)
        draw.ellipse((px - r, py - r, px + r, py + r), fill=(255, 225, 176, int(alpha * pulse)))
    image.alpha_composite(layer)


def draw_dynamic_equalizer(image: Image.Image, energy: float, frame: int) -> None:
    draw = ImageDraw.Draw(image, "RGBA")
    cx = 1972
    cy = 1124
    radius = 354
    start = math.radians(196)
    end = math.radians(286)
    for rr, alpha in ((radius - 26, 34), (radius + 31, 28)):
        prev: tuple[float, float] | None = None
        for i in range(84):
            angle = start + (end - start) * i / 83
            p = (cx + math.cos(angle) * rr, cy + math.sin(angle) * rr)
            if prev is not None:
                draw.line((*prev, *p), fill=(178, 125, 54, alpha), width=2)
            prev = p

    count = 46
    for index in range(count):
        angle = start + (end - start) * index / (count - 1)
        wave = 0.48 + 0.52 * abs(math.sin(index * 0.45 + frame * 0.045))
        local = 0.36 + 0.42 * wave + 0.22 * energy
        length = 18 + 38 * min(0.92, local)
        thickness = 8 + (index % 3 == 1) * 2
        alpha = int(112 + 42 * min(1.0, local))
        rr = radius + math.sin(index * 0.7) * 4
        static.rotated_brick(image, (cx, cy), angle, rr, length, thickness, (178, 125, 54, alpha))

    for frac in (0.06, 0.26, 0.47, 0.70, 0.91):
        angle = start + (end - start) * frac
        static.dot(draw, int(cx + math.cos(angle) * (radius - 54)), int(cy + math.sin(angle) * (radius - 54)), r=4, alpha=118)


def render(args: argparse.Namespace) -> Path:
    background = root_path(args.background)
    audio = root_path(args.audio)
    output = root_path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    if not background.exists():
        raise FileNotFoundError(background)
    if not audio.exists():
        raise FileNotFoundError(audio)

    base = build_base(background)
    top, subtitle, ornament = build_overlay_layers()
    particles = particle_specs()
    energies = audio_energy(audio, args.fps, args.duration)

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
        "20",
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
    frames = int(args.duration * args.fps)
    for frame in range(frames):
        t = frame / args.fps
        image = base.copy()
        draw_particles(image, particles, t)
        draw_dynamic_equalizer(image, energies[min(frame, len(energies) - 1)], frame)
        image.alpha_composite(opacity(top, fade(t, 0.25, 1.35)))
        image.alpha_composite(opacity(subtitle, fade(t, 1.2, 2.2)))
        image.alpha_composite(opacity(ornament, fade(t, 1.45, 2.45)))
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
    parser.add_argument("--duration", type=float, default=15.0)
    parser.add_argument("--fps", type=int, default=24)
    args = parser.parse_args()
    output = render(args)
    print(output.relative_to(PROJECT_ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
