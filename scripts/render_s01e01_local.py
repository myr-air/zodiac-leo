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
import re
import shutil
import subprocess
import tempfile
import wave
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFilter

import create_v6_cute_smooth_motion_proof as v6


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EPISODE_ID = "s01e01-campus-cafe-longplay"
DEFAULT_OUTPUT_ROOT = Path("candidates/s01e01-campus-cafe-longplay/render/future-local-render-01")
DEFAULT_TEMP_ROOT = Path(tempfile.gettempdir()) / "opencode" / "s01e01-render"
BACKGROUND = Path("candidates/s01e01-campus-cafe-longplay/visual/G.png")
SOURCE_SRT = Path(f"channel/episodes/{EPISODE_ID}/subtitles/{EPISODE_ID}.en.srt")
SOURCE_VTT = Path(f"channel/episodes/{EPISODE_ID}/subtitles/{EPISODE_ID}.en.vtt")

WIDTH = 1920
HEIGHT = 1080
FPS = 24
GAP_SECONDS = 1.0
TARGET_DURATION = 2503.28


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


def project_path(path: Path | str) -> Path:
    path = Path(path)
    return path if path.is_absolute() else PROJECT_ROOT / path


def assert_under_candidates(path: Path) -> None:
    resolved = path.resolve()
    candidates = (PROJECT_ROOT / "candidates").resolve()
    if candidates not in [resolved, *resolved.parents]:
        raise ValueError(f"refusing to write local render evidence outside candidates/: {path}")


def assert_default_output_root(path: Path) -> None:
    """Refuse extra render roots that would exceed the approved local QA gate."""
    resolved = path.resolve()
    default = project_path(DEFAULT_OUTPUT_ROOT).resolve()
    if resolved != default:
        raise ValueError(
            "refusing non-canonical render output root; additional or revised "
            "outputs require a new explicit gate"
        )


def assert_safe_temp_root(path: Path) -> None:
    """Limit removable temp files to this script's private temp subtree."""
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


def concat_audio(output_root: Path) -> dict[str, object]:
    audio_out = output_root / "audio" / f"{EPISODE_ID}.timeline-41m43s28.wav"
    prepare_output(audio_out)

    first = project_path(TRACKS[0].audio_path)
    with wave.open(str(first), "rb") as wav:
        params = wav.getparams()
    if params.nchannels != 2 or params.sampwidth != 2 or params.framerate != 48000:
        raise ValueError(f"unexpected first WAV params: {params}")

    total_frames = 0
    gap_frames = int(GAP_SECONDS * params.framerate)
    silence = b"\x00" * gap_frames * params.nchannels * params.sampwidth
    track_summaries: list[dict[str, object]] = []

    with wave.open(str(audio_out), "wb") as out:
        out.setparams(params)
        for index, track in enumerate(TRACKS):
            path = project_path(track.audio_path)
            with wave.open(str(path), "rb") as wav:
                if wav.getparams()[:3] != params[:3] or wav.getframerate() != params.framerate:
                    raise ValueError(f"WAV params mismatch for {path}: {wav.getparams()}")
                frames = wav.getnframes()
                out.writeframes(wav.readframes(frames))
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
                out.writeframes(silence)
                total_frames += gap_frames

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
    }


def copy_sidecars(output_root: Path) -> list[str]:
    subtitle_dir = output_root / "subtitles"
    subtitle_dir.mkdir(parents=True, exist_ok=True)
    copied: list[str] = []
    for source in (SOURCE_SRT, SOURCE_VTT):
        src = project_path(source)
        dest = subtitle_dir / src.name
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
    subtitle = "none" if cue is None else re.sub(r"[^a-z0-9]+", "-", cue.text.lower()).strip("-")[:60]
    return f"t{track.number:02d}-{subtitle or 'subtitle'}"


def draw_overlay_frame(path: Path, track: Track, cue: SubtitleCue | None, header: Image.Image) -> None:
    fonts = v6.fonts()
    image = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    image.alpha_composite(header)
    track_text = f"{track.number:02d} - {track.title}"
    v6.text_soft(image, (224, 168), track_text, fonts["track"], (62, 48, 38, 238), stroke_width=1)

    if cue is not None:
        layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        draw = ImageDraw.Draw(layer, "RGBA")
        bbox = draw.multiline_textbbox((0, 0), cue.text, font=fonts["subtitle"], spacing=10, stroke_width=1)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        cx = 430
        cy = 500
        haze = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        hz = ImageDraw.Draw(haze, "RGBA")
        hz.rounded_rectangle(
            (cx - text_w / 2 - 34, cy - text_h / 2 - 22, cx + text_w / 2 + 34, cy + text_h / 2 + 22),
            radius=30,
            fill=(255, 238, 211, 28),
        )
        layer.alpha_composite(haze.filter(ImageFilter.GaussianBlur(14)))
        v6.text_soft(
            layer,
            (cx, int(cy - text_h / 2)),
            cue.text,
            fonts["subtitle"],
            (55, 44, 36, 236),
            anchor="ma",
            align="center",
            spacing=10,
        )
        image.alpha_composite(layer)

    image.save(path)


def quote_concat_path(path: Path) -> str:
    return str(path).replace("'", "'\\''")


def build_overlay_concat(cues: list[SubtitleCue], duration: float, temp_root: Path) -> tuple[Path, dict[str, object]]:
    frame_dir = temp_root / "overlay-frames"
    frame_dir.mkdir(parents=True, exist_ok=True)
    concat_path = temp_root / "overlay.ffconcat"
    header = v6.header_static_layer()
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


def run_ffmpeg_render(audio_path: Path, overlay_concat: Path, output_root: Path, duration: float) -> Path:
    video_out = output_root / "video" / f"{EPISODE_ID}.v6-subtitled-1080p24-qa.mp4"
    prepare_output(video_out)
    bg = project_path(BACKGROUND)

    filter_graph = ";".join(
        [
            "[1:a]asplit=2[aout][aw]",
            "[0:v]scale=1928:1085:force_original_aspect_ratio=increase,"
            "crop=1920:1080:x='(in_w-out_w)/2+sin(t*0.055)*1.1':"
            "y='(in_h-out_h)/2+cos(t*0.045)*0.6',fps=24,format=rgba[bg]",
            "[aw]showwaves=s=430x140:mode=line:rate=24:colors=0xB27E3890,format=rgba,"
            "colorkey=0x000000:0.10:0.05[wave]",
            "[bg][wave]overlay=1452:850:format=auto[withwave]",
            "[2:v]fps=24,format=rgba[ov]",
            "[withwave][ov]overlay=0:0:format=auto,format=yuv420p[v]",
        ]
    )
    command = [
        "ffmpeg",
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
        str(video_out),
    ]
    subprocess.run(command, check=True)
    return video_out


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
    assert_default_output_root(output_root)
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
    overlay_concat, overlay_summary = build_overlay_concat(cues, duration, temp_root)
    video_path = run_ffmpeg_render(project_path(audio_summary["path"]), overlay_concat, output_root, duration)
    summary = {
        "episode_id": EPISODE_ID,
        "duration_target_seconds": round(duration, 3),
        "audio_master": audio_summary,
        "rendered_video": summarize_probe(video_path),
        "copied_sidecars": sidecars,
        "overlay": overlay_summary,
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
