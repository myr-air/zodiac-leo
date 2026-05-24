#!/usr/bin/env python3
"""Create the approved local S01E01 render/export QA outputs.

This helper is local-only. It reads selected local WAV candidates, the accepted
G.png visual direction, and final English sidecars. It writes only local ignored
render evidence under candidates/ and never calls providers, browsers, APIs,
uploads, account surfaces, or release tooling.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import re
import shutil
import subprocess
import tempfile
import warnings
import wave
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFilter

import create_v6_cute_smooth_motion_proof as v6

with warnings.catch_warnings():
    warnings.simplefilter("ignore", DeprecationWarning)
    import audioop


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EPISODE_ID = "s01e01-campus-cafe-longplay"
DEFAULT_OUTPUT_ROOT = Path("candidates/s01e01-campus-cafe-longplay/render/future-local-render-05")
ALLOWED_OUTPUT_ROOTS = (DEFAULT_OUTPUT_ROOT,)
DEFAULT_TEMP_ROOT = Path(tempfile.gettempdir()) / "opencode" / "s01e01-render"
BACKGROUND = Path("candidates/s01e01-campus-cafe-longplay/visual/G.png")
SOURCE_SRT = Path(f"channel/episodes/{EPISODE_ID}/subtitles/{EPISODE_ID}.en.srt")
SOURCE_VTT = Path(f"channel/episodes/{EPISODE_ID}/subtitles/{EPISODE_ID}.en.vtt")
HEADER_FONT_PATHS = ("/System/Library/Fonts/Supplemental/ChalkboardSE.ttc", "/System/Library/Fonts/Avenir Next.ttc")
NOW_PLAYING_FONT_PATHS = HEADER_FONT_PATHS
SUBTITLE_ASS_FONT_NAME = "Chalkboard SE"
SUBTITLE_CENTER = (430, 500)
SUBTITLE_SLIDE = (2, 8)
SUBTITLE_FADE_MAX_MS = 720
SUBTITLE_OVERLAY_X = 0
SUBTITLE_OVERLAY_Y = 370
SUBTITLE_CANVAS_WIDTH = 920
SUBTITLE_CANVAS_HEIGHT = 260
SUBTITLE_SLIDE_MAX_SECONDS = 1.35
HEADPHONE_ICON_POS = (48, 88)
MUSIC_NOTE_OVERLAY_X = 46
MUSIC_NOTE_OVERLAY_Y = 62
MUSIC_NOTE_CANVAS_WIDTH = 136
MUSIC_NOTE_CANVAS_HEIGHT = 132
MUSIC_NOTE_LOOP_SECONDS = 5.4

WIDTH = 1920
HEIGHT = 1080
FPS = 24
GAP_SECONDS = 1.0
TARGET_DURATION = 2503.28
EQ_WIDTH = 430
EQ_HEIGHT = 140
SNAPSHOT_SPECS: tuple[tuple[str, float], ...] = (
    ("s01e01-render-05-sample-01-open.png", 2.0),
    ("s01e01-render-05-sample-02-track02.png", 306.0),
    ("s01e01-render-05-sample-03-track04.png", 735.0),
    ("s01e01-render-05-sample-04-track07.png", 1320.0),
    ("s01e01-render-05-sample-05-track09.png", 1660.0),
    ("s01e01-render-05-sample-06-track11.png", 2050.0),
    ("s01e01-render-05-sample-07-track13-subtitle-motion.png", 2367.0),
)


@dataclass(frozen=True)
class Track:
    number: int
    title: str
    audio_path: Path
    start: float
    end: float


@dataclass(frozen=True)
class SubtitleCue:
    start: float
    end: float
    text: str


@dataclass(frozen=True)
class RenderSegment:
    index: int
    track: Track
    start: float
    end: float

    @property
    def duration(self) -> float:
        return self.end - self.start


TRACKS: tuple[Track, ...] = (
    Track(1, "Margin Notes at Table Three", Path("candidates/s01e01-campus-cafe-longplay/audio/selected/aud-t01_c02--margin-notes-at-table-three.wav"), 0.00, 279.92),
    Track(2, "Two Lids, One Tray", Path("candidates/s01e01-campus-cafe-longplay/audio/selected/aud-t02_c01--two-lids-one-tray.wav"), 280.92, 505.92),
    Track(3, "Borrowed Eraser, Written Name", Path("candidates/s01e01-campus-cafe-longplay/audio/selected/aud-t03_c01--borrowed-eraser-written-name.wav"), 506.92, 711.04),
    Track(4, "Checkout Slip at Chapter Nine", Path("candidates/s01e01-campus-cafe-longplay/audio/selected/aud-t04_c01--checkout-slip-at-chapter-nine.wav"), 712.04, 921.60),
    Track(5, "Steam on the Glass Door", Path("candidates/s01e01-campus-cafe-longplay/audio/selected/aud-t05_c01--steam-on-the-glass-door.wav"), 922.60, 1141.00),
    Track(6, "Peach Can at B4", Path("candidates/s01e01-campus-cafe-longplay/audio/selected/aud-t06_c02--peach-can-at-b4.wav"), 1142.00, 1301.92),
    Track(7, "Green Dot on Your Schedule", Path("candidates/s01e01-campus-cafe-longplay/audio/selected/aud-t07_c01--green-dot-on-your-schedule.wav"), 1302.92, 1497.84),
    Track(8, "Cushion Seat, Charging Cord", Path("candidates/s01e01-campus-cafe-longplay/audio/selected/aud-t08_c01--cushion-seat-charging-cord.wav"), 1498.84, 1630.72),
    Track(9, "Crosswalk Stripes Before Six", Path("candidates/s01e01-campus-cafe-longplay/audio/selected/aud-t09_c01--crosswalk-stripes-before-six.wav"), 1631.72, 1797.64),
    Track(10, "Yellow Tag on the Umbrella Rack", Path("candidates/s01e01-campus-cafe-longplay/audio/selected/aud-t10_c01--yellow-tag-on-the-umbrella-rack.wav"), 1798.64, 1991.08),
    Track(11, "Quiz Key in Blue Ink", Path("candidates/s01e01-campus-cafe-longplay/audio/selected/aud-t11_c01--quiz-key-in-blue-ink.wav"), 1992.08, 2151.96),
    Track(12, "Tray Return at 5:59", Path("candidates/s01e01-campus-cafe-longplay/audio/selected/aud-t12_c01--tray-return-at-559.wav"), 2152.96, 2352.28),
    Track(13, "Latch Click at the Courtyard Gate", Path("candidates/s01e01-campus-cafe-longplay/audio/selected/aud-t13_c01--latch-click-at-the-courtyard-gate.wav"), 2353.28, 2503.28),
)


def render_segments() -> tuple[RenderSegment, ...]:
    """Return one resumable render segment per song, including its following gap."""
    segments: list[RenderSegment] = []
    for index, track in enumerate(TRACKS):
        end = TRACKS[index + 1].start if index + 1 < len(TRACKS) else TARGET_DURATION
        segments.append(RenderSegment(index=index + 1, track=track, start=track.start, end=end))
    return tuple(segments)


def project_path(path: Path | str) -> Path:
    path = Path(path)
    return path if path.is_absolute() else PROJECT_ROOT / path


def assert_under_candidates(path: Path) -> None:
    resolved = path.resolve()
    candidates = (PROJECT_ROOT / "candidates").resolve()
    if candidates not in [resolved, *resolved.parents]:
        raise ValueError(f"refusing to write local render evidence outside candidates/: {path}")


def assert_no_control_chars(path: Path) -> None:
    text = str(path)
    if any(ord(char) < 32 or ord(char) == 127 for char in text):
        raise ValueError(f"refusing path with control characters: {path!s}")


def assert_allowed_output_root(path: Path) -> None:
    """Refuse extra render roots that would exceed the approved local QA gate."""
    assert_no_control_chars(path)
    resolved = path.resolve()
    allowed = {project_path(root).resolve() for root in ALLOWED_OUTPUT_ROOTS}
    if resolved not in allowed:
        raise ValueError(
            "refusing non-canonical render output root; additional or revised "
            "outputs require a new explicit gate"
        )


def assert_safe_temp_root(path: Path) -> None:
    """Limit removable temp files to this script's private temp subtree."""
    assert_no_control_chars(path)
    resolved = path.resolve()
    safe_root = DEFAULT_TEMP_ROOT.resolve()
    if safe_root not in [resolved, *resolved.parents]:
        raise ValueError(f"refusing temp root outside {safe_root}: {path}")


def ensure_inputs_exist() -> None:
    required = [BACKGROUND, SOURCE_SRT, SOURCE_VTT, *(track.audio_path for track in TRACKS)]
    missing = [str(path) for path in required if not project_path(path).exists()]
    if missing:
        raise FileNotFoundError("missing required render input(s): " + ", ".join(missing))


def prepare_output(path: Path) -> None:
    assert_under_candidates(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(
            f"output exists; refusing to overwrite recorded QA evidence without a new gate: {path}"
        )


def expected_audio_plan() -> tuple[wave._wave_params, int, list[dict[str, object]]]:
    first = project_path(TRACKS[0].audio_path)
    with wave.open(str(first), "rb") as wav:
        params = wav.getparams()
    if params.nchannels != 2 or params.sampwidth != 2 or params.framerate != 48000:
        raise ValueError(f"unexpected first WAV params: {params}")

    total_frames = 0
    gap_frames = int(GAP_SECONDS * params.framerate)
    track_summaries: list[dict[str, object]] = []
    for index, track in enumerate(TRACKS):
        path = project_path(track.audio_path)
        with wave.open(str(path), "rb") as wav:
            if wav.getparams()[:3] != params[:3] or wav.getframerate() != params.framerate:
                raise ValueError(f"WAV params mismatch for {path}: {wav.getparams()}")
            frames = wav.getnframes()
        total_frames += frames
        track_summaries.append(
            {
                "track": track.number,
                "path": str(track.audio_path),
                "frames": frames,
                "duration_seconds": round(frames / params.framerate, 3),
            }
        )
        if index < len(TRACKS) - 1:
            total_frames += gap_frames

    return params, total_frames, track_summaries


def audio_summary(audio_out: Path, params: wave._wave_params, total_frames: int, track_summaries: list[dict[str, object]], reused: bool) -> dict[str, object]:
    duration = total_frames / params.framerate
    return {
        "path": str(audio_out.relative_to(PROJECT_ROOT)),
        "sample_rate": params.framerate,
        "channels": params.nchannels,
        "sample_width_bytes": params.sampwidth,
        "duration_seconds": round(duration, 3),
        "track_count": len(TRACKS),
        "gap_count": len(TRACKS) - 1,
        "gap_seconds": GAP_SECONDS,
        "tracks": track_summaries,
        "reused_existing": reused,
    }


def concat_audio(output_root: Path) -> dict[str, object]:
    audio_out = output_root / "audio" / f"{EPISODE_ID}.timeline-41m43s28.wav"
    params, total_frames, track_summaries = expected_audio_plan()

    if audio_out.exists():
        with wave.open(str(audio_out), "rb") as existing:
            if existing.getparams()[:3] != params[:3] or existing.getframerate() != params.framerate:
                raise ValueError(f"existing audio timeline params mismatch: {existing.getparams()}")
            if existing.getnframes() != total_frames:
                raise ValueError(
                    f"existing audio timeline frame count mismatch: {existing.getnframes()} != {total_frames}"
                )
        return audio_summary(audio_out, params, total_frames, track_summaries, reused=True)

    prepare_output(audio_out)
    gap_frames = int(GAP_SECONDS * params.framerate)
    silence = b"\x00" * gap_frames * params.nchannels * params.sampwidth

    with wave.open(str(audio_out), "wb") as out:
        out.setparams(params)
        for index, track in enumerate(TRACKS):
            path = project_path(track.audio_path)
            with wave.open(str(path), "rb") as wav:
                out.writeframes(wav.readframes(wav.getnframes()))
            if index < len(TRACKS) - 1:
                out.writeframes(silence)

    return audio_summary(audio_out, params, total_frames, track_summaries, reused=False)


def copy_sidecars(output_root: Path) -> list[str]:
    subtitle_dir = output_root / "subtitles"
    subtitle_dir.mkdir(parents=True, exist_ok=True)
    copied: list[str] = []
    for source in (SOURCE_SRT, SOURCE_VTT):
        src = project_path(source)
        dest = subtitle_dir / src.name
        if dest.exists():
            if dest.read_bytes() != src.read_bytes():
                raise ValueError(f"existing sidecar copy differs from source: {dest}")
            copied.append(str(dest.relative_to(PROJECT_ROOT)))
            continue
        prepare_output(dest)
        shutil.copy2(src, dest)
        copied.append(str(dest.relative_to(PROJECT_ROOT)))
    return copied


def parse_srt_time(value: str) -> float:
    match = re.fullmatch(r"(\d{2}):(\d{2}):(\d{2}),(\d{3})", value.strip())
    if not match:
        raise ValueError(f"invalid SRT timestamp: {value!r}")
    hours, minutes, seconds, millis = map(int, match.groups())
    return hours * 3600 + minutes * 60 + seconds + millis / 1000


def parse_srt(path: Path) -> list[SubtitleCue]:
    text = path.read_text(encoding="utf-8-sig")
    cues: list[SubtitleCue] = []
    for block in re.split(r"\n\s*\n", text.strip()):
        lines = [line.rstrip() for line in block.splitlines() if line.strip()]
        if len(lines) < 3:
            continue
        timing = lines[1]
        if "-->" not in timing:
            continue
        start_text, end_text = [part.strip() for part in timing.split("-->", 1)]
        cues.append(SubtitleCue(parse_srt_time(start_text), parse_srt_time(end_text), "\n".join(lines[2:])))
    return cues


def current_track(t: float) -> Track:
    for index, track in enumerate(TRACKS):
        next_start = TRACKS[index + 1].start if index + 1 < len(TRACKS) else TARGET_DURATION + 1
        if track.start <= t < next_start:
            return track
    return TRACKS[0]


def active_subtitle(cues: Iterable[SubtitleCue], t: float) -> SubtitleCue | None:
    for cue in cues:
        if cue.start <= t < cue.end:
            return cue
    return None


def rounded_time(value: float) -> float:
    return round(max(0.0, value), 3)


def render_fonts() -> dict[str, object]:
    """Fonts for render-05 overlays.

    The user asked `Now Playing` to use the same face as `MELLOW LONGPLAY`,
    but stay visually smaller/lighter than the header.
    """
    return {
        "header": v6.load_font(list(HEADER_FONT_PATHS), 27),
        "now": v6.load_font(list(NOW_PLAYING_FONT_PATHS), 23),
        "track": v6.load_font(list(HEADER_FONT_PATHS), 34),
        "subtitle": v6.load_font(list(HEADER_FONT_PATHS), 41),
    }


def cubic_bezier_points(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    steps: int = 44,
) -> list[tuple[float, float]]:
    """Return evenly sampled cubic Bézier points for hand-drawn vector marks."""
    points: list[tuple[float, float]] = []
    for index in range(steps + 1):
        t = index / steps
        u = 1.0 - t
        x = (u**3 * p0[0]) + (3 * u * u * t * p1[0]) + (3 * u * t * t * p2[0]) + (t**3 * p3[0])
        y = (u**3 * p0[1]) + (3 * u * u * t * p1[1]) + (3 * u * t * t * p2[1]) + (t**3 * p3[1])
        points.append((x, y))
    return points


def draw_round_polyline(
    draw: ImageDraw.ImageDraw,
    points: list[tuple[float, float]],
    scale: int,
    fill: tuple[int, int, int, int],
    width: float,
) -> None:
    """Draw a smooth scaled polyline with rounded caps."""
    scaled = [(round(x * scale), round(y * scale)) for x, y in points]
    scaled_width = max(1, round(width * scale))
    if len(scaled) >= 2:
        draw.line(scaled, fill=fill, width=scaled_width, joint="curve")
    cap_radius = scaled_width / 2
    for x, y in (scaled[0], scaled[-1]):
        draw.ellipse((x - cap_radius, y - cap_radius, x + cap_radius, y + cap_radius), fill=fill)


def draw_round_polyline_pixels(
    draw: ImageDraw.ImageDraw,
    points: list[tuple[float, float]],
    fill: tuple[int, int, int, int],
    width: float,
) -> None:
    """Draw a pixel-space polyline with rounded caps."""
    scaled_width = max(1, round(width))
    rounded = [(round(x), round(y)) for x, y in points]
    if len(rounded) >= 2:
        draw.line(rounded, fill=fill, width=scaled_width, joint="curve")
    cap_radius = scaled_width / 2
    for x, y in (rounded[0], rounded[-1]):
        draw.ellipse((x - cap_radius, y - cap_radius, x + cap_radius, y + cap_radius), fill=fill)


def refined_headphone_icon() -> Image.Image:
    """Draw a mathematically balanced, cozy line-vector headphone mark.

    The V6 icon was functional but read as loose arcs and rectangles at full
    render size. This mark keeps the same header footprint while using mirrored
    Bézier curves, equal cup geometry, rounded caps, and a small warm accent so
    it feels intentionally designed rather than sketched in a hurry.
    """
    scale = 6
    base_w, base_h = 94, 92
    icon = Image.new("RGBA", (base_w * scale, base_h * scale), (0, 0, 0, 0))
    draw = ImageDraw.Draw(icon, "RGBA")

    main = (104, 79, 59, 224)
    soft = (104, 79, 59, 68)
    inner = (104, 79, 59, 126)
    gold = (180, 129, 62, 156)
    cream = (255, 239, 211, 32)

    def box(values: tuple[float, float, float, float]) -> tuple[int, int, int, int]:
        return tuple(round(value * scale) for value in values)

    # Soft halo beneath the band keeps it integrated with the warm illustration.
    outer_band = cubic_bezier_points((18, 53), (21, 17), (73, 17), (76, 53), steps=64)
    draw_round_polyline(draw, outer_band, scale, soft, 9.0)
    draw_round_polyline(draw, outer_band, scale, main, 4.6)

    # Inner echo follows the same symmetry at a golden-ish narrower width.
    inner_band = cubic_bezier_points((29, 50), (32, 29), (62, 29), (65, 50), steps=48)
    draw_round_polyline(draw, inner_band, scale, inner, 1.8)

    highlight_band = cubic_bezier_points((34, 43), (38, 32), (56, 32), (60, 43), steps=34)
    draw_round_polyline(draw, highlight_band, scale, (255, 236, 205, 42), 1.3)

    # Mirrored ear cups: equal dimensions, rounded corners, and subtle inner pads.
    for left in (True, False):
        if left:
            cup = (10, 43, 28, 76)
            pad = (15, 50, 25, 70)
            joint = cubic_bezier_points((23, 51), (20, 54), (19, 60), (19, 67), steps=18)
        else:
            cup = (66, 43, 84, 76)
            pad = (69, 50, 79, 70)
            joint = cubic_bezier_points((71, 51), (74, 54), (75, 60), (75, 67), steps=18)
        draw.rounded_rectangle(box(cup), radius=8 * scale, fill=cream, outline=main, width=round(3.8 * scale))
        draw.rounded_rectangle(box(pad), radius=5 * scale, outline=inner, width=round(1.8 * scale))
        draw_round_polyline(draw, joint, scale, inner, 1.4)

    # Small centered accent/cord hint anchors the icon without making it busy.
    draw.ellipse(box((42.0, 77.0, 46.0, 81.0)), fill=gold)
    draw_round_polyline(draw, [(46, 78.7), (53, 78.7), (57, 76.8)], scale, (180, 129, 62, 118), 1.1)

    return icon.resize((base_w, base_h), Image.Resampling.LANCZOS)


def draw_music_note_mark(
    draw: ImageDraw.ImageDraw,
    x: float,
    y: float,
    size: float,
    alpha: int,
    *,
    double: bool = False,
) -> None:
    """Draw an original tiny music-note vector mark in pixel coordinates."""
    alpha = max(0, min(255, alpha))
    if alpha <= 0:
        return

    main = (104, 79, 59, alpha)
    warm = (180, 129, 62, max(0, min(255, int(alpha * 0.62))))
    glow = (255, 238, 211, max(0, min(255, int(alpha * 0.22))))
    stroke = max(1.0, size * 0.105)

    def note_head(cx: float, cy: float, scale: float = 1.0) -> tuple[float, float]:
        w = size * 0.48 * scale
        h = size * 0.32 * scale
        draw.ellipse((cx - w * 0.50, cy - h * 0.48, cx + w * 0.50, cy + h * 0.52), fill=glow)
        draw.ellipse((cx - w * 0.42, cy - h * 0.36, cx + w * 0.42, cy + h * 0.42), outline=main, width=round(stroke))
        draw.ellipse((cx - w * 0.22, cy - h * 0.18, cx + w * 0.18, cy + h * 0.18), fill=warm)
        return (cx + w * 0.34, cy - h * 0.02)

    if double:
        first_stem = note_head(x, y)
        second_stem = note_head(x + size * 0.72, y - size * 0.18, 0.92)
        stem_top_1 = (first_stem[0], y - size * 1.16)
        stem_top_2 = (second_stem[0], y - size * 1.34)
        draw_round_polyline_pixels(draw, [first_stem, stem_top_1], main, stroke)
        draw_round_polyline_pixels(draw, [second_stem, stem_top_2], main, stroke)
        draw_round_polyline_pixels(
            draw,
            [stem_top_1, (stem_top_1[0] + size * 0.36, stem_top_1[1] - size * 0.06), stem_top_2],
            warm,
            stroke * 1.28,
        )
        draw_round_polyline_pixels(
            draw,
            [(stem_top_1[0], stem_top_1[1] + size * 0.22), (stem_top_2[0], stem_top_2[1] + size * 0.22)],
            main,
            stroke * 0.88,
        )
        return

    stem_base = note_head(x, y)
    stem_top = (stem_base[0], y - size * 1.12)
    draw_round_polyline_pixels(draw, [stem_base, stem_top], main, stroke)
    flag = cubic_bezier_points(
        stem_top,
        (stem_top[0] + size * 0.46, stem_top[1] + size * 0.02),
        (stem_top[0] + size * 0.60, stem_top[1] + size * 0.40),
        (stem_top[0] + size * 0.18, stem_top[1] + size * 0.54),
        steps=18,
    )
    draw_round_polyline_pixels(draw, flag, warm, stroke * 0.92)


def render_music_note_frame(t: float) -> Image.Image:
    """Render a small transparent animated-note layer near the headphone mark."""
    antialias = 3
    frame = Image.new(
        "RGBA",
        (MUSIC_NOTE_CANVAS_WIDTH * antialias, MUSIC_NOTE_CANVAS_HEIGHT * antialias),
        (0, 0, 0, 0),
    )
    draw = ImageDraw.Draw(frame, "RGBA")
    specs = (
        # x, y, size, phase, double
        (88.0, 46.0, 16.0, 0.0, False),
        (105.0, 76.0, 13.0, 1.8, True),
        (69.0, 32.0, 11.0, 3.4, False),
    )
    for base_x, base_y, size, phase, double in specs:
        local = ((t + phase) % MUSIC_NOTE_LOOP_SECONDS) / MUSIC_NOTE_LOOP_SECONDS
        ease = v6.ease(local)
        alpha = int(78 * math.sin(math.pi * local) ** 0.92)
        if alpha < 4:
            continue
        x = (base_x + 1.2 * math.sin(math.tau * local + phase)) * antialias
        y = (base_y - 12.0 * ease) * antialias
        draw_music_note_mark(draw, x, y, size * antialias, alpha, double=double)
    return frame.resize((MUSIC_NOTE_CANVAS_WIDTH, MUSIC_NOTE_CANVAS_HEIGHT), Image.Resampling.LANCZOS)


def build_music_note_overlay(duration: float, temp_root: Path, start_seconds: float = 0.0) -> tuple[Path, dict[str, object]]:
    output = temp_root / "render-05-music-note-overlay.mov"
    if output.exists():
        output.unlink()
    frame_count = math.ceil(duration * FPS)
    command = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-f",
        "rawvideo",
        "-pix_fmt",
        "rgba",
        "-s",
        f"{MUSIC_NOTE_CANVAS_WIDTH}x{MUSIC_NOTE_CANVAS_HEIGHT}",
        "-r",
        str(FPS),
        "-i",
        "-",
        "-an",
        "-c:v",
        "qtrle",
        "-pix_fmt",
        "argb",
        str(output),
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    assert process.stdin is not None
    for frame in range(frame_count):
        process.stdin.write(render_music_note_frame(start_seconds + frame / FPS).tobytes())
    process.stdin.close()
    result = process.wait()
    if result != 0:
        raise RuntimeError(f"ffmpeg music-note overlay exited with {result}")
    return output, {
        "renderer": "generated_rgba_qtrle_overlay",
        "canvas": f"{MUSIC_NOTE_CANVAS_WIDTH}x{MUSIC_NOTE_CANVAS_HEIGHT}",
        "position": {"x": MUSIC_NOTE_OVERLAY_X, "y": MUSIC_NOTE_OVERLAY_Y},
        "loop_seconds": MUSIC_NOTE_LOOP_SECONDS,
        "start_seconds": round(start_seconds, 3),
        "note_count": 3,
        "motion": "tiny warm vector notes drift upward beside the headphone icon with low opacity",
    }


def header_static_layer() -> Image.Image:
    fonts = render_fonts()
    layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    layer.alpha_composite(refined_headphone_icon(), HEADPHONE_ICON_POS)
    draw = ImageDraw.Draw(layer, "RGBA")
    draw.line((190, 78, 190, 202), fill=(178, 126, 56, 112), width=2)
    x = 224
    v6.text_soft(layer, (x, 88), "MELLOW LONGPLAY  •  S01 - E01", fonts["header"], v6.BROWN, stroke_width=0)
    v6.text_soft(layer, (x, 130), "Now Playing", fonts["now"], (134, 93, 61, 196), stroke_width=0)
    draw.line((x, 226, x + 516, 226), fill=(178, 126, 56, 118), width=2)
    draw.ellipse((x + 524, 221, x + 534, 231), fill=(178, 126, 56, 160))
    return layer


def overlay_events(cues: list[SubtitleCue], duration: float) -> list[tuple[float, float, Track, SubtitleCue | None]]:
    points = {0.0, rounded_time(duration)}
    for track in TRACKS:
        if track.start <= duration:
            points.add(rounded_time(track.start))
    for cue in cues:
        if cue.start < duration and cue.end > 0:
            points.add(rounded_time(max(0.0, cue.start)))
            points.add(rounded_time(min(duration, cue.end)))
    ordered = sorted(point for point in points if 0 <= point <= duration)
    result: list[tuple[float, float, Track, SubtitleCue | None]] = []
    for start, end in zip(ordered, ordered[1:]):
        if end - start < 0.01:
            continue
        mid = (start + end) / 2
        result.append((start, end, current_track(mid), active_subtitle(cues, mid)))
    return result


def safe_key(track: Track, cue: SubtitleCue | None) -> str:
    return f"t{track.number:02d}-header"


def draw_overlay_frame(path: Path, track: Track, cue: SubtitleCue | None, header: Image.Image) -> None:
    fonts = render_fonts()
    image = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    image.alpha_composite(header)
    track_text = f"{track.number:02d} - {track.title}"
    v6.text_soft(image, (224, 168), track_text, fonts["track"], (62, 48, 38, 238), stroke_width=1)
    image.save(path)


def quote_concat_path(path: Path) -> str:
    assert_no_control_chars(path)
    return str(path).replace("'", "'\\''")


def escape_filter_value(path: Path) -> str:
    """Escape a path for use as a quoted ffmpeg filter option value."""
    assert_no_control_chars(path)
    text = str(path)
    for char in ("\\", "'", ":", ",", "[", "]"):
        text = text.replace(char, f"\\{char}")
    return text


def format_ass_time(seconds: float) -> str:
    centiseconds = int(round(max(0.0, seconds) * 100))
    hours, remainder = divmod(centiseconds, 360000)
    minutes, remainder = divmod(remainder, 6000)
    whole_seconds, centiseconds = divmod(remainder, 100)
    return f"{hours}:{minutes:02d}:{whole_seconds:02d}.{centiseconds:02d}"


def escape_ass_text(text: str) -> str:
    return (
        text.replace("\\", "＼")
        .replace("{", "｛")
        .replace("}", "｝")
        .replace("\r\n", "\n")
        .replace("\r", "\n")
        .replace("\n", r"\N")
    )


def ass_subtitle_override(cue: SubtitleCue) -> str:
    duration_ms = max(1, int(round((cue.end - cue.start) * 1000)))
    fade_ms = min(SUBTITLE_FADE_MAX_MS, max(120, int(duration_ms * 0.28)))
    if fade_ms * 2 >= duration_ms:
        fade_ms = max(80, duration_ms // 3)
    center_x, center_y = SUBTITLE_CENTER
    slide_x, slide_y = SUBTITLE_SLIDE
    return (
        r"{"
        rf"\move({center_x - slide_x},{center_y + slide_y},{center_x},{center_y},0,{duration_ms})"
        rf"\fad({fade_ms},{fade_ms})"
        r"}"
    )


def write_subtitle_ass(cues: list[SubtitleCue], path: Path) -> dict[str, object]:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "[Script Info]",
        "ScriptType: v4.00+",
        f"PlayResX: {WIDTH}",
        f"PlayResY: {HEIGHT}",
        "ScaledBorderAndShadow: yes",
        "WrapStyle: 2",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, "
        "Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
        "Alignment, MarginL, MarginR, MarginV, Encoding",
        f"Style: MellowSubtitle,{SUBTITLE_ASS_FONT_NAME},41,&H00242C37,&H00D5EFFF,&H00D5EFFF,&H00000000,"
        "0,0,0,0,100,100,0,0,1,1,0,5,120,120,0,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    for cue in cues:
        lines.append(
            "Dialogue: 0,"
            f"{format_ass_time(cue.start)},{format_ass_time(cue.end)},"
            "MellowSubtitle,,0,0,0,,"
            f"{ass_subtitle_override(cue)}{escape_ass_text(cue.text)}"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {
        "renderer": "ass_subtitles_filter",
        "cue_count": len(cues),
        "font": SUBTITLE_ASS_FONT_NAME,
        "fade_max_ms": SUBTITLE_FADE_MAX_MS,
        "slide_pixels": {"x": SUBTITLE_SLIDE[0], "y": -SUBTITLE_SLIDE[1]},
        "motion": "very subtle upward slide with minimal right drift and slow fade in/out",
    }


def subtitle_fade_seconds(cue: SubtitleCue) -> float:
    duration = max(0.001, cue.end - cue.start)
    fade = min(SUBTITLE_FADE_MAX_MS / 1000, max(0.12, duration * 0.28))
    if fade * 2 >= duration:
        fade = max(0.08, duration / 3)
    return fade


def subtitle_motion_state(cue: SubtitleCue, t: float) -> tuple[float, float, float]:
    duration = max(0.001, cue.end - cue.start)
    fade = subtitle_fade_seconds(cue)
    fade_in = v6.fade(t, cue.start, cue.start + fade)
    fade_out = v6.fade_out(t, cue.end - fade, cue.end)
    alpha = min(fade_in, fade_out)
    slide_window = min(SUBTITLE_SLIDE_MAX_SECONDS, max(0.32, duration * 0.55))
    progress = v6.ease((t - cue.start) / slide_window)
    return (
        max(0.0, min(1.0, alpha)),
        -SUBTITLE_SLIDE[0] * (1.0 - progress),
        SUBTITLE_SLIDE[1] * (1.0 - progress),
    )


def apply_canvas_alpha(layer: Image.Image, alpha: float) -> Image.Image:
    alpha = max(0.0, min(1.0, alpha))
    if alpha >= 0.999:
        return layer
    result = layer.copy()
    result.putalpha(result.getchannel("A").point(lambda value: int(value * alpha)))
    return result


def translate_canvas(layer: Image.Image, dx: float, dy: float) -> Image.Image:
    return layer.transform(
        (SUBTITLE_CANVAS_WIDTH, SUBTITLE_CANVAS_HEIGHT),
        Image.Transform.AFFINE,
        (1, 0, -dx, 0, 1, -dy),
        resample=Image.Resampling.BICUBIC,
    )


def render_subtitle_base_layer(cue: SubtitleCue) -> Image.Image:
    fonts = render_fonts()
    layer = Image.new("RGBA", (SUBTITLE_CANVAS_WIDTH, SUBTITLE_CANVAS_HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    bbox = draw.multiline_textbbox((0, 0), cue.text, font=fonts["subtitle"], spacing=10, stroke_width=1)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    cx = SUBTITLE_CENTER[0] - SUBTITLE_OVERLAY_X
    cy = SUBTITLE_CENTER[1] - SUBTITLE_OVERLAY_Y
    haze = Image.new("RGBA", (SUBTITLE_CANVAS_WIDTH, SUBTITLE_CANVAS_HEIGHT), (0, 0, 0, 0))
    hz = ImageDraw.Draw(haze, "RGBA")
    hz.rounded_rectangle(
        (cx - text_w / 2 - 34, cy - text_h / 2 - 22, cx + text_w / 2 + 34, cy + text_h / 2 + 22),
        radius=30,
        fill=(255, 238, 211, 30),
    )
    layer.alpha_composite(haze.filter(ImageFilter.GaussianBlur(14)))
    v6.text_soft(
        layer,
        (int(cx), int(cy - text_h / 2)),
        cue.text,
        fonts["subtitle"],
        (55, 44, 36, 236),
        anchor="ma",
        align="center",
        spacing=10,
    )
    return layer


def build_subtitle_motion_overlay(cues: list[SubtitleCue], duration: float, temp_root: Path) -> tuple[Path, dict[str, object]]:
    output = temp_root / "render-05-subtitle-motion-overlay.mov"
    if output.exists():
        output.unlink()
    frame_count = math.ceil(duration * FPS)
    command = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-f",
        "rawvideo",
        "-pix_fmt",
        "rgba",
        "-s",
        f"{SUBTITLE_CANVAS_WIDTH}x{SUBTITLE_CANVAS_HEIGHT}",
        "-r",
        str(FPS),
        "-i",
        "-",
        "-an",
        "-c:v",
        "qtrle",
        "-pix_fmt",
        "argb",
        str(output),
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    assert process.stdin is not None
    cache: dict[int, Image.Image] = {}
    cue_index = 0
    for frame in range(frame_count):
        t = frame / FPS
        while cue_index < len(cues) and cues[cue_index].end <= t:
            cue_index += 1
        image = Image.new("RGBA", (SUBTITLE_CANVAS_WIDTH, SUBTITLE_CANVAS_HEIGHT), (0, 0, 0, 0))
        if cue_index < len(cues) and cues[cue_index].start <= t < cues[cue_index].end:
            cue = cues[cue_index]
            if cue_index not in cache:
                cache[cue_index] = render_subtitle_base_layer(cue)
            alpha, dx, dy = subtitle_motion_state(cue, t)
            image.alpha_composite(translate_canvas(apply_canvas_alpha(cache[cue_index], alpha), dx, dy))
        process.stdin.write(image.tobytes())
    process.stdin.close()
    result = process.wait()
    if result != 0:
        raise RuntimeError(f"ffmpeg subtitle motion overlay exited with {result}")
    return output, {
        "renderer": "generated_rgba_qtrle_overlay",
        "cue_count": len(cues),
        "canvas": f"{SUBTITLE_CANVAS_WIDTH}x{SUBTITLE_CANVAS_HEIGHT}",
        "position": {"x": SUBTITLE_OVERLAY_X, "y": SUBTITLE_OVERLAY_Y},
        "fade_max_ms": SUBTITLE_FADE_MAX_MS,
        "slide_pixels": {"x": SUBTITLE_SLIDE[0], "y": -SUBTITLE_SLIDE[1]},
        "motion": "very subtle upward slide-in with minimal right drift and smooth slow fade in/out per cue",
    }


def make_particle_texture(path: Path) -> None:
    rng = random.Random(606)
    base = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(base, "RGBA")
    for _ in range(230):
        x = rng.triangular(10, WIDTH - 10, 430)
        y = rng.triangular(8, HEIGHT - 8, 260)
        r = rng.uniform(0.9, 3.4)
        alpha = int(rng.uniform(18, 72))
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(255, 222, 172, alpha))
    for _ in range(26):
        x = rng.triangular(60, 860, 350)
        y = rng.triangular(20, 540, 190)
        r = rng.uniform(5.0, 15.0)
        alpha = int(rng.uniform(10, 28))
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(255, 230, 184, alpha))
    base = base.filter(ImageFilter.GaussianBlur(0.28))
    texture = Image.new("RGBA", (WIDTH, HEIGHT * 2), (0, 0, 0, 0))
    texture.alpha_composite(base, (0, 0))
    texture.alpha_composite(base, (0, HEIGHT))
    texture.save(path)


def make_light_sweep(path: Path) -> None:
    sweep_width = 2400
    layer = Image.new("RGBA", (sweep_width, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    draw.polygon(
        [(-30, -100), (190, -100), (840, HEIGHT + 100), (590, HEIGHT + 100)],
        fill=(255, 230, 178, 18),
    )
    draw.polygon(
        [(160, -100), (270, -100), (930, HEIGHT + 100), (800, HEIGHT + 100)],
        fill=(255, 245, 211, 10),
    )
    layer = layer.filter(ImageFilter.GaussianBlur(58))
    layer.save(path)


def make_sunlight_texture(path: Path) -> None:
    layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    for index in range(8):
        inset = index * 58
        alpha = max(5, 26 - index * 3)
        draw.ellipse((70 - inset, 10 - inset, 970 + inset, 620 + inset), fill=(255, 223, 164, alpha))
    draw.polygon([(-80, -80), (250, -80), (900, HEIGHT + 120), (620, HEIGHT + 120)], fill=(255, 234, 190, 12))
    draw.polygon([(120, -80), (250, -80), (880, HEIGHT + 120), (740, HEIGHT + 120)], fill=(255, 248, 220, 8))
    layer = layer.filter(ImageFilter.GaussianBlur(64))
    layer.save(path)


def make_reflection_texture(path: Path) -> None:
    layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    for index, (x0, y0, x1, y1) in enumerate(
        (
            (1010, 730, 1450, 768),
            (1120, 790, 1580, 826),
            (1280, 852, 1740, 886),
            (230, 700, 690, 730),
        )
    ):
        draw.rounded_rectangle((x0, y0, x1, y1), radius=18, fill=(255, 236, 196, 18 - index * 3))
    for index in range(5):
        y = 760 + index * 34
        draw.line((960 + index * 42, y, 1680 - index * 22, y + 18), fill=(255, 250, 225, 8), width=5)
    layer = layer.filter(ImageFilter.GaussianBlur(18))
    layer.save(path)


def make_shadow_texture(path: Path) -> None:
    layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    draw.ellipse((1180, 620, 2050, 1200), fill=(64, 44, 30, 26))
    draw.ellipse((-180, 720, 720, 1240), fill=(74, 50, 34, 14))
    draw.polygon([(1540, -80), (2010, 0), (1940, 430), (1710, 370)], fill=(60, 43, 31, 10))
    layer = layer.filter(ImageFilter.GaussianBlur(52))
    layer.save(path)


def audio_energy(path: Path, fps: int, duration: float, start_seconds: float = 0.0) -> list[float]:
    frame_count = math.ceil(duration * fps)
    with wave.open(str(path), "rb") as wav:
        sample_width = wav.getsampwidth()
        rate = wav.getframerate()
        start_frame = min(wav.getnframes(), max(0, int(round(start_seconds * rate))))
        total_frames = min(wav.getnframes(), start_frame + int(math.ceil(duration * rate)))
        wav.setpos(start_frame)
        values: list[float] = []
        last_frame = start_frame
        for frame in range(frame_count):
            next_frame = min(total_frames, start_frame + int((frame + 1) * rate / fps))
            raw = wav.readframes(max(0, next_frame - last_frame))
            last_frame = next_frame
            if not raw or sample_width != 2:
                values.append(0.0)
            else:
                values.append(audioop.rms(raw, sample_width) / 32768.0)

    if not values:
        return [0.18]
    sorted_values = sorted(values)
    p95 = sorted_values[min(len(sorted_values) - 1, int(len(sorted_values) * 0.95))] or max(values) or 1.0
    normalized = [min(1.0, value / p95) for value in values]
    smoothed: list[float] = []
    prev = 0.0
    for value in normalized:
        coeff = 0.075 if value > prev else 0.035
        prev += (value - prev) * coeff
        smoothed.append(prev)
    averaged: list[float] = []
    radius = max(1, int(fps * 0.30))
    for index in range(len(smoothed)):
        start = max(0, index - radius)
        end = min(len(smoothed), index + radius + 1)
        averaged.append(sum(smoothed[start:end]) / (end - start))
    return averaged


def make_equalizer_frame(energy: float, t: float) -> Image.Image:
    layer = Image.new("RGBA", (EQ_WIDTH, EQ_HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    base_y = 68
    phase = t * 0.32
    amp = 6.0 + 18.0 * max(0.0, min(1.0, energy))
    for band, offset in enumerate((-16, 0, 16)):
        points = []
        for index in range(170):
            u = index / 169
            x = EQ_WIDTH * u
            arc = 32 * math.sin(u * math.pi * 0.78)
            wave = amp * math.sin(u * math.tau * 2.1 + phase + band * 0.55)
            points.append((x, base_y + arc + offset + wave))
        draw.line(points, fill=(178, 126, 56, 68 + band * 12), width=2 if band != 1 else 3)
    for index in range(18):
        u = index / 17
        x = EQ_WIDTH * u
        arc = 32 * math.sin(u * math.pi * 0.78)
        y = base_y + arc + amp * math.sin(u * math.tau * 2.1 + phase)
        r = 2.5 + 3.2 * energy * (0.65 + 0.35 * math.sin(phase + index * 0.8))
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(184, 131, 62, int(108 + 62 * energy)))
    return layer.filter(ImageFilter.GaussianBlur(0.28))


def build_equalizer_overlay(audio_path: Path, duration: float, temp_root: Path, start_seconds: float = 0.0) -> Path:
    output = temp_root / "render-05-equalizer-overlay.mov"
    if output.exists():
        output.unlink()
    energies = audio_energy(audio_path, FPS, duration, start_seconds=start_seconds)
    command = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-f",
        "rawvideo",
        "-pix_fmt",
        "rgba",
        "-s",
        f"{EQ_WIDTH}x{EQ_HEIGHT}",
        "-r",
        str(FPS),
        "-i",
        "-",
        "-an",
        "-c:v",
        "qtrle",
        "-pix_fmt",
        "argb",
        str(output),
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    assert process.stdin is not None
    for frame, energy in enumerate(energies):
        process.stdin.write(make_equalizer_frame(energy, start_seconds + frame / FPS).tobytes())
    process.stdin.close()
    result = process.wait()
    if result != 0:
        raise RuntimeError(f"ffmpeg equalizer overlay exited with {result}")
    return output


def build_visual_assets(audio_path: Path, duration: float, temp_root: Path, start_seconds: float = 0.0) -> dict[str, Path]:
    particle_path = temp_root / "render-05-particles.png"
    light_path = temp_root / "render-05-light-sweep.png"
    sunlight_path = temp_root / "render-05-sunlight.png"
    reflection_path = temp_root / "render-05-reflection.png"
    shadow_path = temp_root / "render-05-shadow.png"
    make_particle_texture(particle_path)
    make_light_sweep(light_path)
    make_sunlight_texture(sunlight_path)
    make_reflection_texture(reflection_path)
    make_shadow_texture(shadow_path)
    equalizer_path = build_equalizer_overlay(audio_path, duration, temp_root, start_seconds=start_seconds)
    return {
        "particles": particle_path,
        "light": light_path,
        "sunlight": sunlight_path,
        "reflection": reflection_path,
        "shadow": shadow_path,
        "equalizer": equalizer_path,
    }


def build_overlay_concat(cues: list[SubtitleCue], duration: float, temp_root: Path) -> tuple[Path, dict[str, object]]:
    frame_dir = temp_root / "overlay-frames"
    frame_dir.mkdir(parents=True, exist_ok=True)
    concat_path = temp_root / "overlay.ffconcat"
    header = header_static_layer()
    events = overlay_events(cues, duration)
    cache: dict[str, Path] = {}
    sequence: list[tuple[Path, float]] = []

    for start, end, track, cue in events:
        key = safe_key(track, cue)
        if key not in cache:
            frame_path = frame_dir / f"frame-{len(cache):04d}.png"
            draw_overlay_frame(frame_path, track, cue, header)
            cache[key] = frame_path
        sequence.append((cache[key], end - start))

    with concat_path.open("w", encoding="utf-8") as handle:
        handle.write("ffconcat version 1.0\n")
        for frame_path, interval_duration in sequence:
            handle.write(f"file '{quote_concat_path(frame_path)}'\n")
            handle.write(f"duration {interval_duration:.6f}\n")
        if sequence:
            handle.write(f"file '{quote_concat_path(sequence[-1][0])}'\n")

    return concat_path, {
        "interval_count": len(sequence),
        "unique_overlay_frame_count": len(cache),
        "subtitle_cue_count": len(cues),
    }


def segment_cues(cues: list[SubtitleCue], segment: RenderSegment) -> list[SubtitleCue]:
    """Return cues overlapping a segment, shifted onto the segment-local timeline."""
    shifted: list[SubtitleCue] = []
    for cue in cues:
        if cue.start < segment.end and cue.end > segment.start:
            shifted.append(
                SubtitleCue(
                    max(0.0, cue.start - segment.start),
                    min(segment.duration, cue.end - segment.start),
                    cue.text,
                )
            )
    return shifted


def build_segment_overlay_concat(segment: RenderSegment, temp_root: Path) -> tuple[Path, dict[str, object]]:
    """Build a constant header/title overlay for one resumable song segment."""
    frame_dir = temp_root / "overlay-frames"
    frame_dir.mkdir(parents=True, exist_ok=True)
    concat_path = temp_root / "overlay.ffconcat"
    frame_path = frame_dir / f"segment-{segment.index:02d}-header.png"
    draw_overlay_frame(frame_path, segment.track, None, header_static_layer())

    with concat_path.open("w", encoding="utf-8") as handle:
        handle.write("ffconcat version 1.0\n")
        handle.write(f"file '{quote_concat_path(frame_path)}'\n")
        handle.write(f"duration {segment.duration:.6f}\n")
        handle.write(f"file '{quote_concat_path(frame_path)}'\n")

    return concat_path, {
        "interval_count": 1,
        "unique_overlay_frame_count": 1,
        "subtitle_cue_count": 0,
        "segment_index": segment.index,
        "track": segment.track.number,
        "start_seconds": round(segment.start, 3),
        "duration_seconds": round(segment.duration, 3),
    }


def run_ffmpeg_render(
    audio_path: Path,
    overlay_concat: Path,
    subtitle_overlay: Path,
    music_note_overlay: Path,
    output_root: Path,
    duration: float,
    visual_assets: dict[str, Path],
    temp_root: Path,
) -> Path:
    video_out = output_root / "video" / f"{EPISODE_ID}.v6-subtitled-1080p24-qa.mp4"
    prepare_output(video_out)
    temp_video = temp_root / "render-05-video.tmp.mp4"
    if temp_video.exists():
        temp_video.unlink()
    bg = project_path(BACKGROUND)

    filter_graph = ";".join(
        [
            "[1:a]anull[aout]",
            "[0:v]scale=1928:1085:force_original_aspect_ratio=increase,"
            "crop=1920:1080:x='(in_w-out_w)/2+sin(t*0.021)*0.32':"
            "y='(in_h-out_h)/2+cos(t*0.018)*0.22',fps=24,format=rgba[bg]",
            "[8:v]format=rgba[shadow]",
            "[bg][shadow]overlay=x='sin(t*0.030)*2.0':y='cos(t*0.027)*1.2':format=auto[withshadow]",
            "[3:v]format=rgba[pt]",
            "[withshadow][pt]overlay=x=0:y='mod(-t*4.6,1080)-1080':format=auto[withparticles]",
            "[4:v]format=rgba[light]",
            "[withparticles][light]overlay=x='mod(t*7.4,2400)-520':y='sin(t*0.041)*10':format=auto[withlight]",
            "[6:v]format=rgba[sun]",
            "[withlight][sun]overlay=x='sin(t*0.026)*14':y='cos(t*0.022)*8':format=auto[withsun]",
            "[7:v]format=rgba[ref]",
            "[withsun][ref]overlay=x='sin(t*0.052)*9':y='cos(t*0.046)*5':format=auto[withref]",
            "[5:v]format=rgba[eq]",
            "[withref][eq]overlay=1452:850:format=auto[witheq]",
            "[2:v]fps=24,format=rgba[ov]",
            "[witheq][ov]overlay=0:0:format=auto[withov]",
            "[9:v]format=rgba[sub]",
            f"[withov][sub]overlay={SUBTITLE_OVERLAY_X}:{SUBTITLE_OVERLAY_Y}:format=auto[withsub]",
            "[10:v]format=rgba[notes]",
            f"[withsub][notes]overlay={MUSIC_NOTE_OVERLAY_X}:{MUSIC_NOTE_OVERLAY_Y}:format=auto,format=yuv420p[v]",
        ]
    )
    command = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-loop",
        "1",
        "-framerate",
        str(FPS),
        "-i",
        str(bg),
        "-i",
        str(audio_path),
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(overlay_concat),
        "-loop",
        "1",
        "-framerate",
        str(FPS),
        "-i",
        str(visual_assets["particles"]),
        "-loop",
        "1",
        "-framerate",
        str(FPS),
        "-i",
        str(visual_assets["light"]),
        "-i",
        str(visual_assets["equalizer"]),
        "-loop",
        "1",
        "-framerate",
        str(FPS),
        "-i",
        str(visual_assets["sunlight"]),
        "-loop",
        "1",
        "-framerate",
        str(FPS),
        "-i",
        str(visual_assets["reflection"]),
        "-loop",
        "1",
        "-framerate",
        str(FPS),
        "-i",
        str(visual_assets["shadow"]),
        "-i",
        str(subtitle_overlay),
        "-i",
        str(music_note_overlay),
        "-filter_complex",
        filter_graph,
        "-map",
        "[v]",
        "-map",
        "[aout]",
        "-t",
        f"{duration:.3f}",
        "-r",
        str(FPS),
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
        "192k",
        "-movflags",
        "+faststart",
        "-shortest",
        str(temp_video),
    ]
    subprocess.run(command, check=True)
    shutil.move(str(temp_video), video_out)
    return video_out


def segment_video_path(output_root: Path, segment: RenderSegment) -> Path:
    return output_root / "video" / "segments" / f"{EPISODE_ID}.render-05-segment-{segment.index:02d}-track-{segment.track.number:02d}.mp4"


def video_probe_matches(path: Path, expected_duration: float, tolerance: float = 0.12) -> bool:
    if not path.exists():
        return False
    try:
        probe = summarize_probe(path)
    except Exception:
        return False
    video = probe.get("video", {})
    return (
        video.get("width") == WIDTH
        and video.get("height") == HEIGHT
        and video.get("frame_rate") == "24/1"
        and abs(float(probe.get("duration_seconds", 0.0)) - expected_duration) <= tolerance
    )


def run_ffmpeg_segment_render(
    segment: RenderSegment,
    overlay_concat: Path,
    subtitle_overlay: Path,
    music_note_overlay: Path,
    output_root: Path,
    visual_assets: dict[str, Path],
    temp_root: Path,
) -> tuple[Path, bool]:
    """Render one video-only segment with all motion keyed to global time.

    The final QA MP4 is later muxed with one continuous WAV timeline, so audio is
    never stitched from per-song AAC chunks. Visual expressions use `t + segment
    start` to avoid particle/light/parallax/music-note resets at segment seams.
    """
    video_out = segment_video_path(output_root, segment)
    if video_probe_matches(video_out, segment.duration):
        return video_out, True
    prepare_output(video_out)
    temp_video = temp_root / f"render-05-segment-{segment.index:02d}.tmp.mp4"
    if temp_video.exists():
        temp_video.unlink()
    bg = project_path(BACKGROUND)
    gt = f"(t+{segment.start:.6f})"

    filter_graph = ";".join(
        [
            "[0:v]scale=1928:1085:force_original_aspect_ratio=increase,"
            f"crop=1920:1080:x='(in_w-out_w)/2+sin({gt}*0.021)*0.32':"
            f"y='(in_h-out_h)/2+cos({gt}*0.018)*0.22',fps=24,format=rgba[bg]",
            "[7:v]format=rgba[shadow]",
            f"[bg][shadow]overlay=x='sin({gt}*0.030)*2.0':y='cos({gt}*0.027)*1.2':format=auto[withshadow]",
            "[2:v]format=rgba[pt]",
            f"[withshadow][pt]overlay=x=0:y='mod(-{gt}*4.6,1080)-1080':format=auto[withparticles]",
            "[3:v]format=rgba[light]",
            f"[withparticles][light]overlay=x='mod({gt}*7.4,2400)-520':y='sin({gt}*0.041)*10':format=auto[withlight]",
            "[5:v]format=rgba[sun]",
            f"[withlight][sun]overlay=x='sin({gt}*0.026)*14':y='cos({gt}*0.022)*8':format=auto[withsun]",
            "[6:v]format=rgba[ref]",
            f"[withsun][ref]overlay=x='sin({gt}*0.052)*9':y='cos({gt}*0.046)*5':format=auto[withref]",
            "[4:v]format=rgba[eq]",
            "[withref][eq]overlay=1452:850:format=auto[witheq]",
            "[1:v]fps=24,format=rgba[ov]",
            "[witheq][ov]overlay=0:0:format=auto[withov]",
            "[8:v]format=rgba[sub]",
            f"[withov][sub]overlay={SUBTITLE_OVERLAY_X}:{SUBTITLE_OVERLAY_Y}:format=auto[withsub]",
            "[9:v]format=rgba[notes]",
            f"[withsub][notes]overlay={MUSIC_NOTE_OVERLAY_X}:{MUSIC_NOTE_OVERLAY_Y}:format=auto,format=yuv420p[v]",
        ]
    )
    command = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-loop",
        "1",
        "-framerate",
        str(FPS),
        "-i",
        str(bg),
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(overlay_concat),
        "-loop",
        "1",
        "-framerate",
        str(FPS),
        "-i",
        str(visual_assets["particles"]),
        "-loop",
        "1",
        "-framerate",
        str(FPS),
        "-i",
        str(visual_assets["light"]),
        "-i",
        str(visual_assets["equalizer"]),
        "-loop",
        "1",
        "-framerate",
        str(FPS),
        "-i",
        str(visual_assets["sunlight"]),
        "-loop",
        "1",
        "-framerate",
        str(FPS),
        "-i",
        str(visual_assets["reflection"]),
        "-loop",
        "1",
        "-framerate",
        str(FPS),
        "-i",
        str(visual_assets["shadow"]),
        "-i",
        str(subtitle_overlay),
        "-i",
        str(music_note_overlay),
        "-filter_complex",
        filter_graph,
        "-map",
        "[v]",
        "-t",
        f"{segment.duration:.3f}",
        "-r",
        str(FPS),
        "-an",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "20",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        str(temp_video),
    ]
    subprocess.run(command, check=True)
    shutil.move(str(temp_video), video_out)
    return video_out, False


def write_concat_file(paths: list[Path], concat_path: Path) -> None:
    concat_path.parent.mkdir(parents=True, exist_ok=True)
    with concat_path.open("w", encoding="utf-8") as handle:
        handle.write("ffconcat version 1.0\n")
        for path in paths:
            handle.write(f"file '{quote_concat_path(path)}'\n")


def assemble_chunked_video(segment_paths: list[Path], audio_path: Path, output_root: Path, temp_root: Path) -> tuple[Path, dict[str, object]]:
    video_out = output_root / "video" / f"{EPISODE_ID}.v6-subtitled-1080p24-qa.mp4"
    if video_probe_matches(video_out, TARGET_DURATION, tolerance=0.20):
        return video_out, {"reused_existing": True, "segment_count": len(segment_paths)}
    prepare_output(video_out)
    concat_path = temp_root / "render-05-segments.ffconcat"
    write_concat_file(segment_paths, concat_path)
    temp_video = temp_root / "render-05-final.tmp.mp4"
    if temp_video.exists():
        temp_video.unlink()
    command = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_path),
        "-i",
        str(audio_path),
        "-map",
        "0:v:0",
        "-map",
        "1:a:0",
        "-t",
        f"{TARGET_DURATION:.3f}",
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-movflags",
        "+faststart",
        "-shortest",
        str(temp_video),
    ]
    subprocess.run(command, check=True)
    shutil.move(str(temp_video), video_out)
    return video_out, {"reused_existing": False, "segment_count": len(segment_paths)}


def extract_snapshots(video_path: Path, output_root: Path) -> list[str]:
    snapshot_dir = output_root / "qa" / "snapshots"
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    paths: list[str] = []
    for name, timestamp in SNAPSHOT_SPECS:
        path = snapshot_dir / name
        if path.exists():
            Image.open(path).verify()
            paths.append(str(path.relative_to(PROJECT_ROOT)))
            continue
        prepare_output(path)
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-ss",
                f"{timestamp:.3f}",
                "-i",
                str(video_path),
                "-frames:v",
                "1",
                str(path),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        paths.append(str(path.relative_to(PROJECT_ROOT)))
    return paths


def ffprobe_json(path: Path) -> dict[str, object]:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_format",
            "-show_streams",
            "-of",
            "json",
            str(path),
        ],
        check=True,
        stdout=subprocess.PIPE,
        text=True,
    )
    return json.loads(result.stdout)


def summarize_probe(path: Path) -> dict[str, object]:
    probe = ffprobe_json(path)
    streams = probe.get("streams", [])
    video_stream = next((stream for stream in streams if stream.get("codec_type") == "video"), {})
    audio_stream = next((stream for stream in streams if stream.get("codec_type") == "audio"), {})
    return {
        "path": str(path.relative_to(PROJECT_ROOT)),
        "bytes": path.stat().st_size,
        "duration_seconds": round(float(probe.get("format", {}).get("duration", 0.0)), 3),
        "video": {
            "codec": video_stream.get("codec_name"),
            "width": video_stream.get("width"),
            "height": video_stream.get("height"),
            "frame_rate": video_stream.get("r_frame_rate"),
        },
        "audio": {
            "codec": audio_stream.get("codec_name"),
            "sample_rate": audio_stream.get("sample_rate"),
            "channels": audio_stream.get("channels"),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    parser.add_argument("--temp-root", type=Path, default=DEFAULT_TEMP_ROOT)
    parser.add_argument("--keep-temp", action="store_true")
    parser.add_argument("--print-json", action="store_true")
    args = parser.parse_args()

    ensure_inputs_exist()
    output_root = project_path(args.output_root)
    assert_allowed_output_root(output_root)
    assert_under_candidates(output_root)
    duration = TARGET_DURATION

    temp_root = args.temp_root if args.temp_root.is_absolute() else DEFAULT_TEMP_ROOT / args.temp_root
    assert_safe_temp_root(temp_root)
    if temp_root.exists() and not args.keep_temp:
        shutil.rmtree(temp_root)
    temp_root.mkdir(parents=True, exist_ok=True)

    audio_summary = concat_audio(output_root)
    sidecars = copy_sidecars(output_root)
    cues = parse_srt(project_path(SOURCE_SRT))
    audio_path = project_path(audio_summary["path"])
    segment_summaries: list[dict[str, object]] = []
    segment_paths: list[Path] = []
    for segment in render_segments():
        segment_temp = temp_root / "segments" / f"segment-{segment.index:02d}"
        segment_temp.mkdir(parents=True, exist_ok=True)
        local_cues = segment_cues(cues, segment)
        overlay_concat, overlay_summary = build_segment_overlay_concat(segment, segment_temp)
        subtitle_overlay, subtitle_motion_summary = build_subtitle_motion_overlay(local_cues, segment.duration, segment_temp)
        music_note_overlay, music_note_summary = build_music_note_overlay(
            segment.duration,
            segment_temp,
            start_seconds=segment.start,
        )
        visual_assets = build_visual_assets(audio_path, segment.duration, segment_temp, start_seconds=segment.start)
        segment_path, reused_segment = run_ffmpeg_segment_render(
            segment,
            overlay_concat,
            subtitle_overlay,
            music_note_overlay,
            output_root,
            visual_assets,
            segment_temp,
        )
        segment_paths.append(segment_path)
        segment_summaries.append(
            {
                "index": segment.index,
                "track": segment.track.number,
                "start_seconds": round(segment.start, 3),
                "duration_seconds": round(segment.duration, 3),
                "path": str(segment_path.relative_to(PROJECT_ROOT)),
                "reused_existing": reused_segment,
                "subtitle_cue_count": len(local_cues),
                "overlay": overlay_summary,
                "subtitle_motion": subtitle_motion_summary,
                "music_notes": music_note_summary,
            }
        )
    video_path, assembly_summary = assemble_chunked_video(segment_paths, audio_path, output_root, temp_root)
    snapshots = extract_snapshots(video_path, output_root)
    summary = {
        "episode_id": EPISODE_ID,
        "duration_target_seconds": round(duration, 3),
        "audio_master": audio_summary,
        "rendered_video": summarize_probe(video_path),
        "copied_sidecars": sidecars,
        "snapshots": snapshots,
        "chunked_render": {
            "mode": "one_video_segment_per_song_then_concat_video_and_mux_continuous_audio",
            "segment_count": len(segment_summaries),
            "assembly": assembly_summary,
            "segments": segment_summaries,
            "continuity": "visual effects use global timeline offsets; final audio is one continuous WAV master, not stitched AAC chunks",
        },
        "visual_revision": "render-05 carries forward render-04 visual revision and burns in the corrected Track 1 cue 58 subtitle text from authoritative source sidecars",
        "boundary": "local ignored render evidence only; no upload, provider, account, release, or rights/platform claim",
    }

    if not args.keep_temp:
        shutil.rmtree(temp_root)
    if args.print_json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(summary["rendered_video"]["path"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
