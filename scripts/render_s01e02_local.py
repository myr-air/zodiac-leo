#!/usr/bin/env python3
"""Create local S01E02 render/export QA evidence.

This helper is local-only. It reads user-supplied S01E02 audio/image
candidates, organizes selected/pool evidence without deleting originals, writes
draft subtitle sidecars from approved source lyrics, and renders a local QA MP4
under candidates/. It never calls providers, browsers, external APIs, upload
surfaces, account tools, or release tooling.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
import subprocess
import tempfile
import wave
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFilter, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EPISODE_ID = "s01e02-classroom-window-longplay"
EPISODE_DIR = Path("channel/episodes") / EPISODE_ID
CANDIDATE_ROOT = Path("candidates") / EPISODE_ID
AUDIO_ROOT = CANDIDATE_ROOT / "audio"
VISUAL_ROOT = CANDIDATE_ROOT / "visual"
SELECTED_AUDIO_ROOT = AUDIO_ROOT / "selected"
POOL_AUDIO_ROOT = AUDIO_ROOT / "pool"
SELECTED_VISUAL_ROOT = VISUAL_ROOT / "selected"
SUBTITLE_DRAFT_ROOT = CANDIDATE_ROOT / "subtitles" / "draft"
SOURCE_SUBTITLE_ROOT = EPISODE_DIR / "subtitles"
DEFAULT_OUTPUT_ROOT = CANDIDATE_ROOT / "render" / "local-render-01"
ALLOWED_OUTPUT_ROOTS = (DEFAULT_OUTPUT_ROOT,)
DEFAULT_TEMP_ROOT = Path(tempfile.gettempdir()) / "opencode" / "s01e02-render"
SONG_SOURCE_ROOT = EPISODE_DIR / "source" / "suno-tracks"
BACKGROUND_SOURCE = VISUAL_ROOT / "ChatGPT Image May 27, 2026, 12_21_46 AM.png"
SELECTED_BACKGROUND = SELECTED_VISUAL_ROOT / "vis-c01--classroom-window-night-mode.png"

WIDTH = 1920
HEIGHT = 1080
FPS = 24
GAP_SECONDS = 1.0
MAX_LINE_CHARS = 37
HEADER_CANVAS_WIDTH = 920
HEADER_CANVAS_HEIGHT = 240
SUBTITLE_CANVAS_WIDTH = 920
SUBTITLE_CANVAS_HEIGHT = 260
HEADER_OVERLAY_X = 0
HEADER_OVERLAY_Y = 54
SUBTITLE_OVERLAY_X = 0
SUBTITLE_OVERLAY_Y = 370


@dataclass(frozen=True)
class TrackSpec:
    number: int
    title: str
    raw_a: Path
    raw_b: Path
    selected_candidate: str = "c01"

    @property
    def slug(self) -> str:
        value = re.sub(r"[^a-z0-9]+", "-", self.title.lower()).strip("-")
        return value or f"track-{self.number:02d}"

    @property
    def selected_raw(self) -> Path:
        return self.raw_a if self.selected_candidate == "c01" else self.raw_b

    @property
    def pool_raw(self) -> Path:
        return self.raw_b if self.selected_candidate == "c01" else self.raw_a

    @property
    def selected_path(self) -> Path:
        return SELECTED_AUDIO_ROOT / f"aud-t{self.number:02d}_{self.selected_candidate}--{self.slug}.wav"

    @property
    def pool_candidate(self) -> str:
        return "c02" if self.selected_candidate == "c01" else "c01"

    @property
    def pool_path(self) -> Path:
        return POOL_AUDIO_ROOT / f"aud-t{self.number:02d}_{self.pool_candidate}--{self.slug}.wav"

    @property
    def source_pack(self) -> Path:
        exact = SONG_SOURCE_ROOT / f"{self.number:02d}-{self.slug}.md"
        if exact.exists():
            return exact
        matches = sorted(SONG_SOURCE_ROOT.glob(f"{self.number:02d}-*.md"))
        if len(matches) == 1:
            return matches[0]
        return exact


@dataclass(frozen=True)
class TimelineTrack:
    spec: TrackSpec
    start: float
    end: float
    frames: int

    @property
    def duration(self) -> float:
        return self.end - self.start


@dataclass(frozen=True)
class Cue:
    slot: str
    start: float
    end: float
    text: str


TRACKS: tuple[TrackSpec, ...] = (
    TrackSpec(1, "Chalk Dust on the Window Rail", AUDIO_ROOT / "Chalk Dust on the Window Rail.wav", AUDIO_ROOT / "Chalk Dust on the Window Rail (1).wav"),
    TrackSpec(2, "Second Seat from the Sun", AUDIO_ROOT / "Second Seat from the Sun.wav", AUDIO_ROOT / "Second Seat from the Sun (1).wav"),
    TrackSpec(3, "Pencil Tap Before the Bell", AUDIO_ROOT / "Pencil Tap Before the Bell.wav", AUDIO_ROOT / "Pencil Tap Before the Bell (1).wav"),
    TrackSpec(4, "Folded Quiz at the Corner", AUDIO_ROOT / "Folded Quiz at the Corner.wav", AUDIO_ROOT / "Folded Quiz at the Corner (1).wav"),
    TrackSpec(5, "Library Stamp at 3:10", AUDIO_ROOT / "Library Stamp at 3_10.wav", AUDIO_ROOT / "Library Stamp at 3_10 (1).wav"),
    TrackSpec(6, "Study Room Reservation", AUDIO_ROOT / "Study Room Reservation.wav", AUDIO_ROOT / "Study Room Reservation (1).wav"),
    TrackSpec(7, "Highlighter Under Monday", AUDIO_ROOT / "Highlighter Under Monday.wav", AUDIO_ROOT / "Highlighter Under Monday (1).wav"),
    TrackSpec(8, "Campus Map Turned Sideways", AUDIO_ROOT / "Campus Map Turned Sideways.wav", AUDIO_ROOT / "Campus Map Turned Sideways (1).wav"),
    TrackSpec(9, "Notebook Margin, Left Blank", AUDIO_ROOT / "Notebook Margin, Left Blank.wav", AUDIO_ROOT / "Notebook Margin, Left Blank (1).wav"),
    TrackSpec(10, "Notice Pin by the Stairs", AUDIO_ROOT / "Notice Pin by the Stairs.wav", AUDIO_ROOT / "Notice Pin by the Stairs (1).wav"),
    TrackSpec(11, "Projector Cord Across the Floor", AUDIO_ROOT / "Projector Cord Across the Floor.wav", AUDIO_ROOT / "Projector Cord Across the Floor (1).wav"),
    TrackSpec(12, "Last Slide Before Dismissal", AUDIO_ROOT / "Last Slide Before Dismissal.wav", AUDIO_ROOT / "Last Slide Before Dismissal (1).wav"),
    TrackSpec(13, "Window Latch After Class", AUDIO_ROOT / "Window Latch After Class.wav", AUDIO_ROOT / "Window Latch After Class (1).wav"),
)


def project_path(path: Path | str) -> Path:
    path = Path(path)
    return path if path.is_absolute() else PROJECT_ROOT / path


def assert_under(path: Path, root: Path) -> None:
    resolved = path.resolve()
    root_resolved = root.resolve()
    if root_resolved not in [resolved, *resolved.parents]:
        raise ValueError(f"refusing path outside {root}: {path}")


def assert_under_candidates(path: Path) -> None:
    assert_under(path, PROJECT_ROOT / "candidates")


def assert_safe_temp_root(path: Path) -> None:
    safe = DEFAULT_TEMP_ROOT.resolve()
    resolved = path.resolve()
    if safe not in [resolved, *resolved.parents]:
        raise ValueError(f"refusing temp root outside {safe}: {path}")


def assert_allowed_output_root(path: Path) -> None:
    resolved = path.resolve()
    allowed = {project_path(root).resolve() for root in ALLOWED_OUTPUT_ROOTS}
    if resolved not in allowed:
        raise ValueError("refusing non-canonical render output root without a new explicit gate")


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def prepare_output(path: Path) -> None:
    assert_under_candidates(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(f"output exists and would be overwritten: {path}")


def write_text_if_changed(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return
    path.write_text(text, encoding="utf-8")


def copy_if_needed(src: Path, dest: Path) -> dict[str, object]:
    src = project_path(src)
    dest = project_path(dest)
    if not src.exists():
        raise FileNotFoundError(src)
    assert_under_candidates(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    src_hash = file_sha256(src)
    if dest.exists():
        dest_hash = file_sha256(dest)
        if dest_hash != src_hash:
            raise ValueError(f"existing destination differs from source: {dest}")
        reused = True
    else:
        shutil.copy2(src, dest)
        reused = False
    return {
        "source": str(src.relative_to(PROJECT_ROOT)),
        "path": str(dest.relative_to(PROJECT_ROOT)),
        "sha256": src_hash,
        "reused_existing": reused,
    }


def ensure_inputs_exist() -> None:
    required = [BACKGROUND_SOURCE, *(track.raw_a for track in TRACKS), *(track.raw_b for track in TRACKS), *(track.source_pack for track in TRACKS)]
    missing = [str(path) for path in required if not project_path(path).exists()]
    if missing:
        raise FileNotFoundError("missing required S01E02 input(s): " + ", ".join(missing))


def organize_candidates() -> dict[str, object]:
    selected = []
    pool = []
    for track in TRACKS:
        selected.append(copy_if_needed(track.selected_raw, track.selected_path) | {"track": track.number, "candidate_id": track.selected_candidate, "title": track.title})
        pool.append(copy_if_needed(track.pool_raw, track.pool_path) | {"track": track.number, "candidate_id": track.pool_candidate, "title": track.title})
    visual = copy_if_needed(BACKGROUND_SOURCE, SELECTED_BACKGROUND) | {"candidate_id": "vis-c01", "status": "selected_visual_direction_source_only"}
    return {"selected_audio": selected, "pool_audio": pool, "selected_visual": visual}


def wav_metadata(path: Path) -> dict[str, object]:
    with wave.open(str(project_path(path)), "rb") as wav:
        params = wav.getparams()
        return {
            "channels": params.nchannels,
            "sample_width_bytes": params.sampwidth,
            "sample_rate": params.framerate,
            "frames": params.nframes,
            "duration_seconds": round(params.nframes / params.framerate, 3),
        }


def expected_audio_plan() -> tuple[wave._wave_params, int, list[TimelineTrack], list[dict[str, object]]]:
    first = project_path(TRACKS[0].selected_path)
    with wave.open(str(first), "rb") as wav:
        params = wav.getparams()
    if params.nchannels != 2 or params.sampwidth != 2 or params.framerate != 48000:
        raise ValueError(f"unexpected first WAV params: {params}")
    total_frames = 0
    gap_frames = int(GAP_SECONDS * params.framerate)
    current_frames = 0
    timeline: list[TimelineTrack] = []
    summaries: list[dict[str, object]] = []
    for index, track in enumerate(TRACKS):
        path = project_path(track.selected_path)
        with wave.open(str(path), "rb") as wav:
            if wav.getparams()[:3] != params[:3] or wav.getframerate() != params.framerate:
                raise ValueError(f"WAV params mismatch for {path}: {wav.getparams()}")
            frames = wav.getnframes()
        start = current_frames / params.framerate
        end = (current_frames + frames) / params.framerate
        entry = TimelineTrack(track, round(start, 3), round(end, 3), frames)
        timeline.append(entry)
        summaries.append(
            {
                "track": track.number,
                "title": track.title,
                "selected_candidate": track.selected_candidate,
                "path": str(track.selected_path),
                "start_seconds": round(start, 3),
                "end_seconds": round(end, 3),
                "duration_seconds": round(frames / params.framerate, 3),
                "gap_after_seconds": 0.0 if index == len(TRACKS) - 1 else GAP_SECONDS,
            }
        )
        total_frames += frames
        current_frames += frames
        if index < len(TRACKS) - 1:
            total_frames += gap_frames
            current_frames += gap_frames
    return params, total_frames, timeline, summaries


def duration_label(seconds: float) -> str:
    minutes = int(seconds // 60)
    rem = seconds - minutes * 60
    return f"{minutes:02d}m{rem:05.2f}s".replace(".", "")


def concat_audio(output_root: Path) -> dict[str, object]:
    params, total_frames, timeline, summaries = expected_audio_plan()
    duration = total_frames / params.framerate
    audio_out = output_root / "audio" / f"{EPISODE_ID}.timeline-{duration_label(duration)}.wav"
    if audio_out.exists():
        with wave.open(str(audio_out), "rb") as existing:
            if existing.getparams()[:3] != params[:3] or existing.getframerate() != params.framerate:
                raise ValueError(f"existing audio timeline params mismatch: {existing.getparams()}")
            if existing.getnframes() != total_frames:
                raise ValueError(f"existing audio timeline frame count mismatch: {existing.getnframes()} != {total_frames}")
        reused = True
    else:
        prepare_output(audio_out)
        gap_frames = int(GAP_SECONDS * params.framerate)
        silence = b"\x00" * gap_frames * params.nchannels * params.sampwidth
        with wave.open(str(audio_out), "wb") as out:
            out.setparams(params)
            for index, track in enumerate(TRACKS):
                with wave.open(str(project_path(track.selected_path)), "rb") as wav:
                    out.writeframes(wav.readframes(wav.getnframes()))
                if index < len(TRACKS) - 1:
                    out.writeframes(silence)
        reused = False
    return {
        "path": str(audio_out.relative_to(PROJECT_ROOT)),
        "sample_rate": params.framerate,
        "channels": params.nchannels,
        "sample_width_bytes": params.sampwidth,
        "duration_seconds": round(duration, 3),
        "track_count": len(TRACKS),
        "gap_count": len(TRACKS) - 1,
        "gap_seconds": GAP_SECONDS,
        "tracks": summaries,
        "timeline_tracks": timeline,
        "reused_existing": reused,
    }


def extract_lyrics(track: TrackSpec) -> list[str]:
    text = project_path(track.source_pack).read_text(encoding="utf-8")
    match = re.search(r"\*\*Lyrics:\*\*\s*\n\s*```text\n(.*?)\n```", text, flags=re.DOTALL)
    if not match:
        raise ValueError(f"lyrics block not found: {track.source_pack}")
    lines: list[str] = []
    for raw in match.group(1).splitlines():
        line = raw.strip()
        if not line or (line.startswith("[") and line.endswith("]")):
            continue
        lines.append(re.sub(r"\s+", " ", line))
    if not lines:
        raise ValueError(f"no subtitle lines extracted: {track.source_pack}")
    return lines


def wrap_text(text: str, max_line_chars: int = MAX_LINE_CHARS) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= max_line_chars:
        return text
    words = text.split()
    best_index = None
    best_score = float("inf")
    for index in range(1, len(words)):
        left = " ".join(words[:index])
        right = " ".join(words[index:])
        if len(left) <= max_line_chars and len(right) <= max_line_chars:
            score = abs(len(left) - len(right))
            if score < best_score:
                best_index = index
                best_score = score
    if best_index is None:
        return text
    return " ".join(words[:best_index]) + "\n" + " ".join(words[best_index:])


def q3(value: float) -> float:
    return round(value + 0.0, 3)


def generate_draft_cues(timeline: list[TimelineTrack]) -> list[Cue]:
    cues: list[Cue] = []
    for entry in timeline:
        lines = extract_lyrics(entry.spec)
        start_pad = max(1.2, min(8.0, entry.duration * 0.045))
        end_pad = max(1.4, min(8.0, entry.duration * 0.050))
        window_start = entry.start + start_pad
        window_end = max(window_start + 1.0, entry.end - end_pad)
        step = (window_end - window_start) / max(1, len(lines))
        for idx, line in enumerate(lines):
            start = window_start + idx * step
            next_start = window_start + (idx + 1) * step if idx + 1 < len(lines) else window_end
            duration = min(4.4, max(1.25, step * 0.82))
            end = min(next_start - 0.08, start + duration, entry.end - 0.05)
            if end <= start:
                end = min(entry.end - 0.05, start + 0.75)
            if end <= start:
                continue
            cues.append(Cue(f"T{entry.spec.number:02d}", q3(start), q3(end), wrap_text(line)))
    cues.sort(key=lambda cue: (cue.start, cue.end, cue.slot))
    validate_cues(cues, timeline)
    return cues


def seconds_to_srt(seconds: float) -> str:
    millis = int(round(max(0.0, seconds) * 1000))
    hours, rem = divmod(millis, 3_600_000)
    minutes, rem = divmod(rem, 60_000)
    secs, ms = divmod(rem, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"


def seconds_to_vtt(seconds: float) -> str:
    return seconds_to_srt(seconds).replace(",", ".")


def seconds_to_ass(seconds: float) -> str:
    centis = int(round(max(0.0, seconds) * 100))
    hours, rem = divmod(centis, 360_000)
    minutes, rem = divmod(rem, 6_000)
    secs, cs = divmod(rem, 100)
    return f"{hours}:{minutes:02d}:{secs:02d}.{cs:02d}"


def serialize_srt(cues: Iterable[Cue]) -> str:
    return "\n\n".join(f"{idx}\n{seconds_to_srt(cue.start)} --> {seconds_to_srt(cue.end)}\n{cue.text}" for idx, cue in enumerate(cues, start=1)) + "\n"


def serialize_vtt(cues: Iterable[Cue]) -> str:
    blocks = ["WEBVTT", "", "NOTE LOCAL DRAFT TIMING ONLY. Generated mechanically from approved lyrics and selected local audio; requires human sung-lyric watch review."]
    for cue in cues:
        blocks.extend(["", f"{seconds_to_vtt(cue.start)} --> {seconds_to_vtt(cue.end)}", cue.text])
    return "\n".join(blocks) + "\n"


def ass_escape(text: str) -> str:
    return text.replace("\\", "＼").replace("{", "｛").replace("}", "｝").replace("\n", r"\N")


def serialize_ass(cues: list[Cue], timeline: list[TimelineTrack], duration: float) -> str:
    lines = [
        "[Script Info]",
        f"Title: {EPISODE_ID} local QA burn-in",
        "ScriptType: v4.00+",
        "WrapStyle: 2",
        "ScaledBorderAndShadow: yes",
        f"PlayResX: {WIDTH}",
        f"PlayResY: {HEIGHT}",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        "Style: Header,Chalkboard SE,29,&H002A2F3D,&H002A2F3D,&H00F4E6D4,&H00000000,0,0,0,0,100,100,0,0,1,1,0,7,0,0,0,1",
        "Style: Now,Chalkboard SE,23,&H704A5C81,&H704A5C81,&H00F4E6D4,&H00000000,0,0,0,0,100,100,0,0,1,1,0,7,0,0,0,1",
        "Style: TrackTitle,Chalkboard SE,34,&H002A2F3D,&H002A2F3D,&H00F4E6D4,&H00000000,0,0,0,0,100,100,0,0,1,1,0,7,0,0,0,1",
        "Style: Lyric,Chalkboard SE,42,&H00242C37,&H00242C37,&H00F6EBDD,&H00000000,0,0,0,0,100,100,0,0,1,1,0,5,0,0,0,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
        f"Dialogue: 0,{seconds_to_ass(0)},{seconds_to_ass(duration)},Header,,0,0,0,,{{\\pos(224,88)}}MELLOW LONGPLAY  •  S01 - E02",
        f"Dialogue: 0,{seconds_to_ass(0)},{seconds_to_ass(duration)},Now,,0,0,0,,{{\\pos(224,130)}}Now Playing",
    ]
    for entry in timeline:
        title = f"{entry.spec.number:02d} - {entry.spec.title}"
        lines.append(
            f"Dialogue: 0,{seconds_to_ass(entry.start)},{seconds_to_ass(entry.end)},TrackTitle,,0,0,0,,{{\\pos(224,168)\\fad(350,350)}}{ass_escape(title)}"
        )
    for cue in cues:
        duration_ms = max(1, int(round((cue.end - cue.start) * 1000)))
        fade_ms = min(420, max(120, int(duration_ms * 0.22)))
        lines.append(
            f"Dialogue: 1,{seconds_to_ass(cue.start)},{seconds_to_ass(cue.end)},Lyric,,0,0,0,,{{\\pos(430,540)\\fad({fade_ms},{fade_ms})}}{ass_escape(cue.text)}"
        )
    return "\n".join(lines) + "\n"


def validate_cues(cues: list[Cue], timeline: list[TimelineTrack]) -> dict[str, object]:
    timeline_by_slot = {f"T{entry.spec.number:02d}": entry for entry in timeline}
    max_line_chars = 0
    previous: Cue | None = None
    gap_cues = 0
    for cue in cues:
        entry = timeline_by_slot[cue.slot]
        if cue.start < entry.start - 0.001 or cue.end > entry.end + 0.001:
            raise ValueError(f"cue outside track window: {cue}")
        if cue.end <= cue.start:
            raise ValueError(f"cue end before start: {cue}")
        if previous and cue.start < previous.end - 0.001:
            raise ValueError(f"cue overlap: {previous} -> {cue}")
        for line in cue.text.splitlines():
            max_line_chars = max(max_line_chars, len(line))
        previous = cue
    for prev_entry, next_entry in zip(timeline, timeline[1:]):
        for cue in cues:
            if cue.start < next_entry.start and cue.end > prev_entry.end:
                gap_cues += 1
    return {
        "cue_count": len(cues),
        "max_line_chars": max_line_chars,
        "gap_cue_count": gap_cues,
        "overlap_count": 0,
        "timing_method": "mechanical_even_distribution_from_source_lyrics_needs_human_watch",
    }


def write_subtitles(cues: list[Cue], timeline: list[TimelineTrack], duration: float, output_root: Path) -> dict[str, object]:
    srt = serialize_srt(cues)
    vtt = serialize_vtt(cues)
    ass = serialize_ass(cues, timeline, duration)
    candidate_srt = SUBTITLE_DRAFT_ROOT / f"{EPISODE_ID}.draft.en.srt"
    candidate_vtt = SUBTITLE_DRAFT_ROOT / f"{EPISODE_ID}.draft.en.vtt"
    source_srt = SOURCE_SUBTITLE_ROOT / f"{EPISODE_ID}.draft.en.srt"
    source_vtt = SOURCE_SUBTITLE_ROOT / f"{EPISODE_ID}.draft.en.vtt"
    render_srt = output_root / "subtitles" / candidate_srt.name
    render_vtt = output_root / "subtitles" / candidate_vtt.name
    render_ass = output_root / "subtitles" / f"{EPISODE_ID}.burnin.ass"
    for path, text in ((candidate_srt, srt), (candidate_vtt, vtt), (source_srt, srt), (source_vtt, vtt), (render_srt, srt), (render_vtt, vtt), (render_ass, ass)):
        write_text_if_changed(project_path(path), text)
    summary = validate_cues(cues, timeline)
    return summary | {
        "candidate_srt": str(candidate_srt),
        "candidate_vtt": str(candidate_vtt),
        "source_srt": str(source_srt),
        "source_vtt": str(source_vtt),
        "render_ass": str(render_ass),
        "boundary": "draft mechanical timing for local QA render; not transcript certification or final human-watch-passed sidecar",
    }


def image_summary(path: Path) -> dict[str, object]:
    with Image.open(project_path(path)) as image:
        return {
            "path": str(path),
            "format": image.format,
            "width": image.width,
            "height": image.height,
            "mode": image.mode,
            "aspect": round(image.width / image.height, 5),
            "sha256": file_sha256(project_path(path)),
        }


def escape_filter_value(path: Path) -> str:
    text = str(project_path(path))
    for char in ("\\", "'", ":", ",", "[", "]"):
        text = text.replace(char, f"\\{char}")
    return text


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for font_path in (
        "/System/Library/Fonts/Supplemental/ChalkboardSE.ttc",
        "/System/Library/Fonts/Avenir Next.ttc",
        "/System/Library/Fonts/HelveticaNeue.ttc",
    ):
        path = Path(font_path)
        if not path.exists():
            continue
        try:
            return ImageFont.truetype(str(path), size)
        except OSError:
            continue
    return ImageFont.load_default(size=size)


def text_soft(
    image: Image.Image,
    xy: tuple[int, int],
    text: str,
    font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
    fill: tuple[int, int, int, int],
    *,
    anchor: str | None = None,
    align: str = "left",
    spacing: int = 8,
) -> None:
    shadow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow, "RGBA")
    sd.multiline_text((xy[0] + 1, xy[1] + 2), text, font=font, fill=(255, 238, 211, 88), anchor=anchor, align=align, spacing=spacing, stroke_width=1, stroke_fill=(255, 238, 211, 88))
    image.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(2.2)))
    draw = ImageDraw.Draw(image, "RGBA")
    draw.multiline_text(xy, text, font=font, fill=fill, anchor=anchor, align=align, spacing=spacing, stroke_width=1, stroke_fill=(255, 244, 226, 130))


def quote_concat_path(path: Path) -> str:
    return str(path).replace("'", "'\\''")


def render_header_frame(path: Path, entry: TimelineTrack) -> None:
    image = Image.new("RGBA", (HEADER_CANVAS_WIDTH, HEADER_CANVAS_HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image, "RGBA")
    brown = (48, 42, 34, 238)
    soft = (132, 91, 61, 190)
    gold = (184, 132, 62, 150)
    # Small original rounded mark; intentionally not a logo copy.
    draw.rounded_rectangle((48, 36, 124, 112), radius=24, outline=(104, 79, 59, 178), width=3, fill=(255, 238, 211, 28))
    draw.arc((64, 54, 108, 102), 190, 530, fill=(104, 79, 59, 210), width=4)
    draw.line((86, 56, 86, 96), fill=gold, width=3)
    draw.ellipse((78, 92, 94, 108), outline=gold, width=3)
    draw.line((158, 30, 158, 144), fill=gold, width=2)
    text_soft(image, (190, 42), "MELLOW LONGPLAY  •  S01 - E02", load_font(29), brown)
    text_soft(image, (190, 84), "Now Playing", load_font(23), soft)
    text_soft(image, (190, 122), f"{entry.spec.number:02d} - {entry.spec.title}", load_font(34), brown)
    draw.line((190, 190, 706, 190), fill=gold, width=2)
    draw.ellipse((716, 185, 726, 195), fill=gold)
    image.save(path)


def build_header_overlay_concat(timeline: list[TimelineTrack], duration: float, temp_root: Path) -> tuple[Path, dict[str, object]]:
    frame_dir = temp_root / "header-frames"
    frame_dir.mkdir(parents=True, exist_ok=True)
    concat_path = temp_root / "s01e02-header-overlay.ffconcat"
    sequence: list[tuple[Path, float]] = []
    for index, entry in enumerate(timeline):
        frame_path = frame_dir / f"header-track-{entry.spec.number:02d}.png"
        if not frame_path.exists():
            render_header_frame(frame_path, entry)
        next_start = timeline[index + 1].start if index + 1 < len(timeline) else duration
        sequence.append((frame_path, max(0.001, next_start - entry.start)))
    with concat_path.open("w", encoding="utf-8") as handle:
        handle.write("ffconcat version 1.0\n")
        for frame_path, frame_duration in sequence:
            handle.write(f"file '{quote_concat_path(frame_path)}'\n")
            handle.write(f"duration {frame_duration:.6f}\n")
        if sequence:
            handle.write(f"file '{quote_concat_path(sequence[-1][0])}'\n")
    return concat_path, {"interval_count": len(sequence), "canvas": f"{HEADER_CANVAS_WIDTH}x{HEADER_CANVAS_HEIGHT}", "position": {"x": HEADER_OVERLAY_X, "y": HEADER_OVERLAY_Y}}


def active_cue(cues: list[Cue], t: float, start_index: int) -> tuple[Cue | None, int]:
    index = start_index
    while index < len(cues) and cues[index].end <= t:
        index += 1
    if index < len(cues) and cues[index].start <= t < cues[index].end:
        return cues[index], index
    return None, index


def render_subtitle_base(cue: Cue) -> Image.Image:
    image = Image.new("RGBA", (SUBTITLE_CANVAS_WIDTH, SUBTITLE_CANVAS_HEIGHT), (0, 0, 0, 0))
    font = load_font(42)
    draw = ImageDraw.Draw(image, "RGBA")
    bbox = draw.multiline_textbbox((0, 0), cue.text, font=font, spacing=10, stroke_width=1)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    cx, cy = 430, 170
    haze = Image.new("RGBA", image.size, (0, 0, 0, 0))
    hz = ImageDraw.Draw(haze, "RGBA")
    hz.rounded_rectangle((cx - text_w / 2 - 34, cy - text_h / 2 - 22, cx + text_w / 2 + 34, cy + text_h / 2 + 22), radius=30, fill=(255, 238, 211, 30))
    image.alpha_composite(haze.filter(ImageFilter.GaussianBlur(14)))
    text_soft(image, (cx, int(cy - text_h / 2)), cue.text, font, (55, 44, 36, 236), anchor="ma", align="center", spacing=10)
    return image


def cue_alpha_and_offset(cue: Cue, t: float) -> tuple[float, float, float]:
    duration = max(0.001, cue.end - cue.start)
    fade = min(0.52, max(0.14, duration * 0.25))
    fade_in = min(1.0, max(0.0, (t - cue.start) / fade))
    fade_out = min(1.0, max(0.0, (cue.end - t) / fade))
    alpha = min(fade_in, fade_out)
    alpha = alpha * alpha * (3 - 2 * alpha)
    progress = min(1.0, max(0.0, (t - cue.start) / min(1.15, max(0.22, duration * 0.55))))
    eased = progress * progress * (3 - 2 * progress)
    return alpha, -2 * (1.0 - eased), 8 * (1.0 - eased)


def apply_alpha(layer: Image.Image, alpha: float) -> Image.Image:
    alpha = max(0.0, min(1.0, alpha))
    if alpha >= 0.999:
        return layer
    result = layer.copy()
    result.putalpha(result.getchannel("A").point(lambda value: int(value * alpha)))
    return result


def build_subtitle_overlay(cues: list[Cue], duration: float, temp_root: Path) -> tuple[Path, dict[str, object]]:
    output = temp_root / "s01e02-subtitle-overlay.mov"
    if output.exists():
        output.unlink()
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
    frame_count = math.ceil(duration * FPS)
    for frame in range(frame_count):
        t = frame / FPS
        cue, cue_index = active_cue(cues, t, cue_index)
        image = Image.new("RGBA", (SUBTITLE_CANVAS_WIDTH, SUBTITLE_CANVAS_HEIGHT), (0, 0, 0, 0))
        if cue is not None:
            key = id(cue)
            if key not in cache:
                cache[key] = render_subtitle_base(cue)
            alpha, dx, dy = cue_alpha_and_offset(cue, t)
            shifted = apply_alpha(cache[key], alpha).transform(
                (SUBTITLE_CANVAS_WIDTH, SUBTITLE_CANVAS_HEIGHT),
                Image.Transform.AFFINE,
                (1, 0, -dx, 0, 1, -dy),
                resample=Image.Resampling.BICUBIC,
            )
            image.alpha_composite(shifted)
        process.stdin.write(image.tobytes())
    process.stdin.close()
    result = process.wait()
    if result != 0:
        raise RuntimeError(f"ffmpeg subtitle overlay exited with {result}")
    return output, {"cue_count": len(cues), "canvas": f"{SUBTITLE_CANVAS_WIDTH}x{SUBTITLE_CANVAS_HEIGHT}", "position": {"x": SUBTITLE_OVERLAY_X, "y": SUBTITLE_OVERLAY_Y}}


def render_video(audio_path: Path, output_root: Path, duration: float, temp_root: Path, cues: list[Cue], timeline: list[TimelineTrack]) -> tuple[Path, dict[str, object]]:
    video_out = output_root / "video" / f"{EPISODE_ID}.local-render-01-draft-subtitled-1080p24-qa.mp4"
    if video_out.exists():
        return video_out, {"reused_existing": True}
    prepare_output(video_out)
    temp_video = temp_root / "s01e02-local-render-01.tmp.mp4"
    if temp_video.exists():
        temp_video.unlink()
    header_concat, header_summary = build_header_overlay_concat(timeline, duration, temp_root)
    subtitle_overlay, subtitle_summary = build_subtitle_overlay(cues, duration, temp_root)
    bg = project_path(SELECTED_BACKGROUND)
    filter_graph = ";".join(
        [
            "[1:a]asplit=2[aout][aw]",
            "[0:v]scale=1928:1085:force_original_aspect_ratio=increase,crop=1920:1080,fps=24,format=rgba[bg]",
            "[aw]showwaves=s=430x140:mode=line:rate=24:colors=0xB8833E99,format=rgba[waves]",
            "[bg][waves]overlay=1450:850:format=auto[vis]",
            "[2:v]fps=24,format=rgba[head]",
            f"[vis][head]overlay={HEADER_OVERLAY_X}:{HEADER_OVERLAY_Y}:format=auto[withhead]",
            "[3:v]format=rgba[sub]",
            f"[withhead][sub]overlay={SUBTITLE_OVERLAY_X}:{SUBTITLE_OVERLAY_Y}:format=auto,format=yuv420p[v]",
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
        str(project_path(audio_path)),
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(header_concat),
        "-i",
        str(subtitle_overlay),
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
    return video_out, {"reused_existing": False, "header_overlay": header_summary, "subtitle_overlay": subtitle_summary, "equalizer": "ffmpeg_showwaves_line_overlay"}


def ffprobe_json(path: Path) -> dict[str, object]:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(project_path(path))],
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
        "path": str(project_path(path).relative_to(PROJECT_ROOT)),
        "bytes": project_path(path).stat().st_size,
        "duration_seconds": round(float(probe.get("format", {}).get("duration", 0.0)), 3),
        "video": {"codec": video_stream.get("codec_name"), "width": video_stream.get("width"), "height": video_stream.get("height"), "frame_rate": video_stream.get("r_frame_rate")},
        "audio": {"codec": audio_stream.get("codec_name"), "sample_rate": audio_stream.get("sample_rate"), "channels": audio_stream.get("channels")},
    }


def extract_snapshots(video_path: Path, output_root: Path, duration: float) -> list[str]:
    specs = [
        ("s01e02-render-01-sample-01-open.png", 2.0),
        ("s01e02-render-01-sample-02-track03.png", 370.0),
        ("s01e02-render-01-sample-03-track06.png", 900.0),
        ("s01e02-render-01-sample-04-track09.png", 1450.0),
        ("s01e02-render-01-sample-05-track12.png", 2090.0),
        ("s01e02-render-01-sample-06-ending.png", max(1.0, duration - 8.0)),
    ]
    snapshot_dir = output_root / "qa" / "snapshots"
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[str] = []
    for name, timestamp in specs:
        path = snapshot_dir / name
        if path.exists():
            Image.open(path).verify()
            outputs.append(str(path.relative_to(PROJECT_ROOT)))
            continue
        prepare_output(path)
        subprocess.run(
            ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{timestamp:.3f}", "-i", str(project_path(video_path)), "-frames:v", "1", str(path)],
            check=True,
        )
        Image.open(path).verify()
        outputs.append(str(path.relative_to(PROJECT_ROOT)))
    return outputs


def decode_check(video_path: Path) -> str:
    subprocess.run(["ffmpeg", "-v", "error", "-i", str(project_path(video_path)), "-f", "null", "-"], check=True)
    return "ffmpeg_decode_no_errors"


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
    temp_root = args.temp_root if args.temp_root.is_absolute() else DEFAULT_TEMP_ROOT / args.temp_root
    assert_safe_temp_root(temp_root)
    if temp_root.exists() and not args.keep_temp:
        shutil.rmtree(temp_root)
    temp_root.mkdir(parents=True, exist_ok=True)

    intake = organize_candidates()
    audio_summary = concat_audio(output_root)
    timeline: list[TimelineTrack] = audio_summary.pop("timeline_tracks")  # type: ignore[assignment]
    duration = float(audio_summary["duration_seconds"])
    cues = generate_draft_cues(timeline)
    subtitle_summary = write_subtitles(cues, timeline, duration, output_root)
    video_path, render_summary = render_video(Path(audio_summary["path"]), output_root, duration, temp_root, cues, timeline)
    snapshots = extract_snapshots(video_path, output_root, duration)
    decode = decode_check(video_path)
    summary = {
        "episode_id": EPISODE_ID,
        "status": "local_render_01_created_with_draft_mechanical_subtitles_needs_human_watch",
        "intake": intake,
        "selected_visual": image_summary(SELECTED_BACKGROUND),
        "audio_master": audio_summary,
        "subtitle_draft": subtitle_summary,
        "rendered_video": summarize_probe(video_path),
        "render_pipeline": render_summary,
        "decode_check": decode,
        "snapshots": snapshots,
        "visual_policy": "mandatory soft watercolor semi-realistic anime playlist-cover style with soft lifelike recurring woman and varied pose; selected local image accepted as candidate evidence only",
        "boundary": "local ignored render evidence only; no upload, provider, account, release, transcript certification, or rights/platform claim",
    }
    if not args.keep_temp:
        shutil.rmtree(temp_root)
    if args.print_json:
        print(json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True))
    else:
        print(summary["rendered_video"]["path"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
