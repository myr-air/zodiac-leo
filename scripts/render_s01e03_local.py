#!/usr/bin/env python3
"""Create local S01E03 render/export QA evidence.

This helper is local-only. It reads user-supplied S01E03 audio/image
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

from PIL import Image, ImageDraw, ImageFilter, ImageFont
from leo_resource_paths import resolve_candidates_root
from subtitle_lane_policy import TIMING_METHOD_MECHANICAL
from subtitle_lane_policy import infer_subtitle_drift_with_fallback
from subtitle_lane_policy import lane_summary
from subtitle_lane_policy import resolve_subtitle_lane

with warnings.catch_warnings():
    warnings.simplefilter("ignore", DeprecationWarning)
    import audioop


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EPISODE_ID = "s01e03-rooftop-golden-hour-longplay"
EPISODE_DIR = Path("channel/episodes") / EPISODE_ID
LEO_CANDIDATES_ROOT = resolve_candidates_root(PROJECT_ROOT)
CANDIDATE_ROOT = LEO_CANDIDATES_ROOT / EPISODE_ID
AUDIO_ROOT = CANDIDATE_ROOT / "audio"
VISUAL_ROOT = CANDIDATE_ROOT / "visual"
SELECTED_AUDIO_ROOT = AUDIO_ROOT / "selected"
POOL_AUDIO_ROOT = AUDIO_ROOT / "pool"
SELECTED_VISUAL_ROOT = VISUAL_ROOT / "selected"
SUBTITLE_DRAFT_ROOT = CANDIDATE_ROOT / "subtitles" / "draft"
SOURCE_SUBTITLE_ROOT = EPISODE_DIR / "subtitles"
PROMOTED_SRT = SOURCE_SUBTITLE_ROOT / f"{EPISODE_ID}.en.srt"
PROMOTED_VTT = SOURCE_SUBTITLE_ROOT / f"{EPISODE_ID}.en.vtt"
DRAFT_SRT = SOURCE_SUBTITLE_ROOT / f"{EPISODE_ID}.draft.en.srt"
DRAFT_VTT = SOURCE_SUBTITLE_ROOT / f"{EPISODE_ID}.draft.en.vtt"
DEFAULT_OUTPUT_ROOT = CANDIDATE_ROOT / "render" / "local-render-02"
ALLOWED_OUTPUT_ROOTS = (DEFAULT_OUTPUT_ROOT,)
DEFAULT_TEMP_ROOT = Path(tempfile.gettempdir()) / "opencode" / "s01e03-render"
SONG_SOURCE_ROOT = EPISODE_DIR / "source" / "suno-tracks"
BACKGROUND_SOURCE = VISUAL_ROOT / "ChatGPT Image May 29, 2026, 09_23_02 PM.png"
SELECTED_BACKGROUND = SELECTED_VISUAL_ROOT / "vis-c01--rooftop-golden-hour-playlist-cover.png"

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
SUBTITLE_EARLY_OFFSET_SECONDS = 0.0
HEADPHONE_ICON_POS = (48, 34)
MUSIC_NOTE_OVERLAY_X = 46
MUSIC_NOTE_OVERLAY_Y = 62
MUSIC_NOTE_CANVAS_WIDTH = 136
MUSIC_NOTE_CANVAS_HEIGHT = 132
MUSIC_NOTE_LOOP_SECONDS = 5.4
EQ_WIDTH = 430
EQ_HEIGHT = 140


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
class RenderSegment:
    index: int
    entry: TimelineTrack
    start: float
    end: float

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
    TrackSpec(1, "Breeze on the Concrete Edge", AUDIO_ROOT / "Breeze on the Concrete Edge.wav", AUDIO_ROOT / "Breeze on the Concrete Edge (1).wav"),
    TrackSpec(2, "Shifting Peach and Violet", AUDIO_ROOT / "Shifting Peach and Violet.wav", AUDIO_ROOT / "Shifting Peach and Violet (1).wav"),
    TrackSpec(3, "Shared Wired Earbuds", AUDIO_ROOT / "Shared Wired Earbuds.wav", AUDIO_ROOT / "Shared Wired Earbuds (1).wav"),
    TrackSpec(4, "Cold Soda Can on the Rail", AUDIO_ROOT / "Cold Soda Can on the Rail.wav", AUDIO_ROOT / "Cold Soda Can on the Rail (1).wav"),
    TrackSpec(5, "Sunlight Refraction", AUDIO_ROOT / "Sunlight Refraction.wav", AUDIO_ROOT / "Sunlight Refraction (1).wav"),
    TrackSpec(6, "The Brick Wall's Holding Heat", AUDIO_ROOT / "The Brick Wall's Holding Heat.wav", AUDIO_ROOT / "The Brick Wall's Holding Heat (1).wav"),
    TrackSpec(7, "Blinking City Below", AUDIO_ROOT / "Blinking City Below.wav", AUDIO_ROOT / "Blinking City Below (1).wav"),
    TrackSpec(8, "Wind-Tangled Hair", AUDIO_ROOT / "Wind-Tangled Hair.wav", AUDIO_ROOT / "Wind-Tangled Hair (1).wav"),
    TrackSpec(9, "Silence Between Two Words", AUDIO_ROOT / "Silence Between Two Words.wav", AUDIO_ROOT / "Silence Between Two Words (1).wav"),
    TrackSpec(10, "Golden Hour Silhouette", AUDIO_ROOT / "Golden Hour Silhouette.wav", AUDIO_ROOT / "Golden Hour Silhouette (1).wav"),
    TrackSpec(11, "Warm Horizon Line", AUDIO_ROOT / "Warm Horizon Line.wav", AUDIO_ROOT / "Warm Horizon Line (1).wav"),
    TrackSpec(12, "Comfort of Just Staying", AUDIO_ROOT / "Comfort of Just Staying.wav", AUDIO_ROOT / "Comfort of Just Staying (1).wav"),
    TrackSpec(13, "Twilight on the Metal Stairs", AUDIO_ROOT / "Twilight on the Metal Stairs.wav", AUDIO_ROOT / "Twilight on the Metal Stairs (1).wav"),
)


def project_path(path: Path | str) -> Path:
    path = Path(path)
    return path if path.is_absolute() else PROJECT_ROOT / path


def as_output_path(path: Path) -> str:
    return str(path.relative_to(PROJECT_ROOT)) if PROJECT_ROOT in [path, *path.parents] else str(path)


def assert_under(path: Path, root: Path) -> None:
    resolved = path.resolve()
    root_resolved = root.resolve()
    if root_resolved not in [resolved, *resolved.parents]:
        raise ValueError(f"refusing path outside {root}: {path}")


def assert_under_candidates(path: Path) -> None:
    assert_under(path, Path(LEO_CANDIDATES_ROOT))


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
        "source": str(as_output_path(src)),
        "path": str(as_output_path(dest)),
        "sha256": src_hash,
        "reused_existing": reused,
    }


def ensure_inputs_exist() -> None:
    required = [BACKGROUND_SOURCE, *(track.raw_a for track in TRACKS), *(track.raw_b for track in TRACKS), *(track.source_pack for track in TRACKS)]
    missing = [str(path) for path in required if not project_path(path).exists()]
    if missing:
        raise FileNotFoundError("missing required S01E03 input(s): " + ", ".join(missing))


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
        "path": str(as_output_path(audio_out)),
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


def parse_srt_time(value: str) -> float:
    match = re.fullmatch(r"(\d{2}):(\d{2}):(\d{2}),(\d{3})", value.strip())
    if not match:
        raise ValueError(f"invalid SRT timestamp: {value!r}")
    hours, minutes, seconds, millis = map(int, match.groups())
    return hours * 3600 + minutes * 60 + seconds + millis / 1000


def parse_srt(path: Path) -> list[Cue]:
    text = path.read_text(encoding="utf-8-sig")
    cues: list[Cue] = []
    for block in re.split(r"\n\s*\n", text.strip()):
        lines = [line.rstrip() for line in block.splitlines() if line.strip()]
        if len(lines) < 3:
            continue
        timing = lines[1]
        if "-->" not in timing:
            continue
        start_text, end_text = [part.strip() for part in timing.split("-->", 1)]
        # We temporarily set slot as empty, will resolve it in main
        cues.append(Cue("", parse_srt_time(start_text), parse_srt_time(end_text), "\n".join(lines[2:])))
    return cues


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


def apply_onset_drift_to_cues(
    cues: list[Cue],
    drift_ms: float | dict[str, float] | None,
    timeline: list[TimelineTrack],
    *,
    min_gap_seconds: float = 0.001,
) -> tuple[list[Cue], dict[str, object]]:
    if drift_ms is None or not cues:
        return cues, {"applied": False, "reason": "insufficient_evidence"}
    slot_drift_ms: dict[str, float] = {}
    slot_fallback_delta_ms = 0.0
    drift_mode = "global"
    if isinstance(drift_ms, dict):
        drift_mode = "slotwise"
        slot_drift_ms = {
            str(slot): float(value) for slot, value in drift_ms.items() if isinstance(slot, str) and isinstance(value, (int, float))
        }
        if not slot_drift_ms:
            return cues, {"applied": False, "reason": "insufficient_evidence"}
        sorted_slot_values = sorted(slot_drift_ms.values())
        slot_fallback_delta_ms = sorted_slot_values[len(sorted_slot_values) // 2]
        global_delta_ms = 0.0
    else:
        global_delta_ms = float(drift_ms)
        if abs(global_delta_ms) < 0.5:
            return cues, {"applied": False, "drift_ms": 0.0, "reason": "drift_below_rounding"}
    timeline_by_slot = {f"T{entry.spec.number:02d}": entry for entry in timeline}
    adjusted: list[Cue] = []
    clipped_count = 0
    unmapped_slots = 0
    applied_slot_count = 0
    applied_count = 0
    fallback_used_count = 0
    for cue in cues:
        entry = timeline_by_slot.get(cue.slot)
        if drift_mode == "slotwise":
            slot_delta_ms = slot_drift_ms.get(cue.slot)
            if slot_delta_ms is None:
                unmapped_slots += 1
                slot_delta_ms = slot_fallback_delta_ms
                fallback_used_count += 1
            else:
                applied_slot_count += 1
        else:
            slot_delta_ms = global_delta_ms
        if abs(slot_delta_ms) >= 0.5:
            applied_count += 1
        delta = slot_delta_ms / 1000.0

        start = cue.start + delta
        end = cue.end + delta
        if entry is not None:
            if start < entry.start:
                start = entry.start
                clipped_count += 1
            if end > entry.end:
                end = entry.end
                clipped_count += 1
            if end <= start:
                end = start + min_gap_seconds
                clipped_count += 1
                if end > entry.end:
                    end = entry.end
                    start = max(entry.start, end - min_gap_seconds)
                    clipped_count += 1
        if end <= start:
            continue
        adjusted.append(Cue(cue.slot, q3(start), q3(end), cue.text))
    adjusted.sort(key=lambda cue: (cue.start, cue.end, cue.slot))
    summary: dict[str, object] = {
        "applied": applied_count > 0,
        "drift_mode": drift_mode,
        "clipped_cues": clipped_count,
        "cue_count": len(adjusted),
    }
    if drift_mode == "slotwise":
        summary |= {
            "drift_ms": dict(sorted(slot_drift_ms.items())),
            "applied_slot_count": applied_slot_count,
            "unmapped_slot_count": unmapped_slots,
            "slot_fallback_ms": round(slot_fallback_delta_ms, 3),
            "fallback_used_count": fallback_used_count,
        }
    else:
        summary |= {
            "drift_ms": round(global_delta_ms, 3),
            "drift_seconds": round(delta, 3),
        }
    return adjusted, summary


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
    ]
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
        "timing_method": TIMING_METHOD_MECHANICAL,
    }


def assign_slots_from_timeline(raw_srt_cues: list[Cue], timeline: list[TimelineTrack]) -> list[Cue]:
    if not timeline:
        return []
    cues: list[Cue] = []
    for raw in raw_srt_cues:
        slot = f"T{timeline[0].spec.number:02d}"
        for entry in timeline:
            if entry.start - 0.5 <= raw.start < entry.end + 0.5:
                slot = f"T{entry.spec.number:02d}"
                break
        cues.append(Cue(slot, raw.start, raw.end, raw.text))
    return cues


def write_subtitles(
    cues: list[Cue],
    timeline: list[TimelineTrack],
    duration: float,
    output_root: Path,
    source_srt: Path,
    source_vtt: Path,
    timing_method: str,
    subtitle_lane: dict[str, object],
) -> dict[str, object]:
    srt = serialize_srt(cues)
    vtt = serialize_vtt(cues)
    ass = serialize_ass(cues, timeline, duration)
    candidate_srt = SUBTITLE_DRAFT_ROOT / f"{EPISODE_ID}.draft.en.srt"
    candidate_vtt = SUBTITLE_DRAFT_ROOT / f"{EPISODE_ID}.draft.en.vtt"
    render_srt = output_root / "subtitles" / candidate_srt.name
    render_vtt = output_root / "subtitles" / candidate_vtt.name
    render_ass = output_root / "subtitles" / f"{EPISODE_ID}.burnin.ass"
    source_srt = project_path(source_srt)
    source_vtt = project_path(source_vtt)
    for path, text in ((candidate_srt, srt), (candidate_vtt, vtt), (source_srt, srt), (source_vtt, vtt), (render_srt, srt), (render_vtt, vtt), (render_ass, ass)):
        write_text_if_changed(project_path(path), text)
    summary = validate_cues(cues, timeline)
    summary["timing_method"] = timing_method
    return summary | {
        "candidate_srt": str(candidate_srt),
        "candidate_vtt": str(candidate_vtt),
        "source_srt": str(source_srt),
        "source_vtt": str(source_vtt),
        "subtitle_lane": subtitle_lane,
        "render_ass": str(render_ass),
        "boundary": f"{timing_method}; not transcript certification or final human-watch-passed sidecar",
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


def cubic_bezier_points(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    *,
    steps: int,
) -> list[tuple[float, float]]:
    points: list[tuple[float, float]] = []
    for index in range(steps + 1):
        t = index / steps
        mt = 1.0 - t
        x = mt**3 * p0[0] + 3 * mt**2 * t * p1[0] + 3 * mt * t**2 * p2[0] + t**3 * p3[0]
        y = mt**3 * p0[1] + 3 * mt**2 * t * p1[1] + 3 * mt * t**2 * p2[1] + t**3 * p3[1]
        points.append((x, y))
    return points


def draw_round_polyline(draw: ImageDraw.ImageDraw, points: list[tuple[float, float]], scale: int, fill: tuple[int, int, int, int], width: float) -> None:
    scaled = [(round(x * scale), round(y * scale)) for x, y in points]
    scaled_width = max(1, round(width * scale))
    if len(scaled) >= 2:
        draw.line(scaled, fill=fill, width=scaled_width, joint="curve")
    cap_radius = scaled_width / 2
    for x, y in (scaled[0], scaled[-1]):
        draw.ellipse((x - cap_radius, y - cap_radius, x + cap_radius, y + cap_radius), fill=fill)


def draw_round_polyline_pixels(draw: ImageDraw.ImageDraw, points: list[tuple[float, float]], fill: tuple[int, int, int, int], width: float) -> None:
    rounded = [(round(x), round(y)) for x, y in points]
    scaled_width = max(1, round(width))
    if len(rounded) >= 2:
        draw.line(rounded, fill=fill, width=scaled_width, joint="curve")
    cap_radius = scaled_width / 2
    for x, y in (rounded[0], rounded[-1]):
        draw.ellipse((x - cap_radius, y - cap_radius, x + cap_radius, y + cap_radius), fill=fill)


def refined_headphone_icon() -> Image.Image:
    """Canonical EP1 render-05 Bézier headphone mark for video overlays."""
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

    outer_band = cubic_bezier_points((18, 53), (21, 17), (73, 17), (76, 53), steps=64)
    draw_round_polyline(draw, outer_band, scale, soft, 9.0)
    draw_round_polyline(draw, outer_band, scale, main, 4.6)

    inner_band = cubic_bezier_points((29, 50), (32, 29), (62, 29), (65, 50), steps=48)
    draw_round_polyline(draw, inner_band, scale, inner, 1.8)

    highlight_band = cubic_bezier_points((34, 43), (38, 32), (56, 32), (60, 43), steps=34)
    draw_round_polyline(draw, highlight_band, scale, (255, 236, 205, 42), 1.3)

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

    draw.ellipse(box((42.0, 77.0, 46.0, 81.0)), fill=gold)
    draw_round_polyline(draw, [(46, 78.7), (53, 78.7), (57, 76.8)], scale, (180, 129, 62, 118), 1.1)
    return icon.resize((base_w, base_h), Image.Resampling.LANCZOS)


def draw_music_note_mark(draw: ImageDraw.ImageDraw, x: float, y: float, size: float, alpha: int, *, double: bool = False) -> None:
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
        draw_round_polyline_pixels(draw, [stem_top_1, (stem_top_1[0] + size * 0.36, stem_top_1[1] - size * 0.06), stem_top_2], warm, stroke * 1.28)
        draw_round_polyline_pixels(draw, [(stem_top_1[0], stem_top_1[1] + size * 0.22), (stem_top_2[0], stem_top_2[1] + size * 0.22)], main, stroke * 0.88)
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


def ease(value: float) -> float:
    value = max(0.0, min(1.0, value))
    return value * value * (3.0 - 2.0 * value)


def render_music_note_frame(t: float) -> Image.Image:
    antialias = 3
    frame = Image.new("RGBA", (MUSIC_NOTE_CANVAS_WIDTH * antialias, MUSIC_NOTE_CANVAS_HEIGHT * antialias), (0, 0, 0, 0))
    draw = ImageDraw.Draw(frame, "RGBA")
    specs = ((88.0, 46.0, 16.0, 0.0, False), (105.0, 76.0, 13.0, 1.8, True), (69.0, 32.0, 11.0, 3.4, False))
    for base_x, base_y, size, phase, double in specs:
        local = ((t + phase) % MUSIC_NOTE_LOOP_SECONDS) / MUSIC_NOTE_LOOP_SECONDS
        alpha = int(78 * math.sin(math.pi * local) ** 0.92)
        if alpha < 4:
            continue
        x = (base_x + 1.2 * math.sin(math.tau * local + phase)) * antialias
        y = (base_y - 12.0 * ease(local)) * antialias
        draw_music_note_mark(draw, x, y, size * antialias, alpha, double=double)
    return frame.resize((MUSIC_NOTE_CANVAS_WIDTH, MUSIC_NOTE_CANVAS_HEIGHT), Image.Resampling.LANCZOS)


def build_music_note_overlay(duration: float, temp_root: Path, *, start_seconds: float = 0.0) -> tuple[Path, dict[str, object]]:
    output = temp_root / "s01e03-render-02-music-note-overlay.mov"
    if output.exists() and output.stat().st_size > 0:
        return output, {
            "renderer": "generated_rgba_qtrle_overlay",
            "canvas": f"{MUSIC_NOTE_CANVAS_WIDTH}x{MUSIC_NOTE_CANVAS_HEIGHT}",
            "position": {"x": MUSIC_NOTE_OVERLAY_X, "y": MUSIC_NOTE_OVERLAY_Y},
            "note_count": 3,
            "motion": "EP1 render-05 tiny warm vector notes adapted to the S01E03 header zone",
            "start_seconds": round(start_seconds, 3),
            "reused_existing": True,
        }
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
        "note_count": 3,
        "motion": "EP1 render-05 tiny warm vector notes adapted to the S01E03 header zone",
        "start_seconds": round(start_seconds, 3),
    }


def quote_concat_path(path: Path) -> str:
    return str(path).replace("'", "'\\''")


def global_time_expr(start_seconds: float = 0.0) -> str:
    return f"(t+{start_seconds:.6f})"


def particle_motion_expr(gt: str) -> tuple[str, str]:
    """Slow random-looking dust drift; not a one-direction upward scroll."""
    return (
        f"sin({gt}*0.019)*12+cos({gt}*0.031)*5",
        f"-540+sin({gt}*0.013)*18+cos({gt}*0.021)*9",
    )


def render_segments(timeline: list[TimelineTrack], duration: float) -> tuple[RenderSegment, ...]:
    """Return one resumable render segment per song, including its following gap."""
    segments: list[RenderSegment] = []
    for index, entry in enumerate(timeline):
        end = timeline[index + 1].start if index + 1 < len(timeline) else duration
        segments.append(RenderSegment(index=index + 1, entry=entry, start=entry.start, end=end))
    return tuple(segments)


def render_header_frame(path: Path, entry: TimelineTrack) -> None:
    image = Image.new("RGBA", (HEADER_CANVAS_WIDTH, HEADER_CANVAS_HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image, "RGBA")
    brown = (48, 42, 34, 238)
    soft = (132, 91, 61, 190)
    gold = (184, 132, 62, 150)
    image.alpha_composite(refined_headphone_icon(), HEADPHONE_ICON_POS)
    draw.line((190, 24, 190, 148), fill=(178, 126, 56, 112), width=2)
    text_soft(image, (224, 34), "MELLOW LONGPLAY  •  S01 - E03", load_font(29), brown)
    text_soft(image, (224, 76), "Now Playing", load_font(23), soft)
    text_soft(image, (224, 114), f"{entry.spec.number:02d} - {entry.spec.title}", load_font(34), brown)
    draw.line((224, 182, 740, 182), fill=gold, width=2)
    draw.ellipse((748, 177, 758, 187), fill=gold)
    image.save(path)


def build_header_overlay_concat(timeline: list[TimelineTrack], duration: float, temp_root: Path) -> tuple[Path, dict[str, object]]:
    frame_dir = temp_root / "header-frames"
    frame_dir.mkdir(parents=True, exist_ok=True)
    concat_path = temp_root / "s01e03-header-overlay.ffconcat"
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


def current_track(timeline: list[TimelineTrack], t: float) -> TimelineTrack:
    for entry in reversed(timeline):
        if t >= entry.start:
            return entry
    return timeline[0]


def render_combined_overlay_frame(path: Path, header: Image.Image, cue: Cue | None) -> None:
    image = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    image.alpha_composite(header, (HEADER_OVERLAY_X, HEADER_OVERLAY_Y))
    if cue is not None:
        image.alpha_composite(render_subtitle_base(cue), (SUBTITLE_OVERLAY_X, SUBTITLE_OVERLAY_Y))
    image.save(path)


def build_combined_overlay_concat(timeline: list[TimelineTrack], cues: list[Cue], duration: float, temp_root: Path) -> tuple[Path, dict[str, object]]:
    """Build event-based header/subtitle overlay without full-duration raw RGBA video.

    The earlier render-02 draft tried to pre-render a per-frame subtitle QTRLE
    movie, which created multi-GB temp files for a 39m45s longplay. This concat
    keeps static event frames only; motion remains in the background, particle,
    music-note, and equalizer layers.
    """
    frame_dir = temp_root / "combined-overlay-frames"
    frame_dir.mkdir(parents=True, exist_ok=True)
    concat_path = temp_root / "s01e03-combined-overlay.ffconcat"
    points = {0.0, round(duration, 3)}
    for entry in timeline:
        if 0.0 <= entry.start <= duration:
            points.add(round(entry.start, 3))
        if 0.0 <= entry.end <= duration:
            points.add(round(entry.end, 3))
    for cue in cues:
        if cue.start < duration and cue.end > 0:
            points.add(round(max(0.0, cue.start), 3))
            points.add(round(min(duration, cue.end), 3))
    # Use a tiny epsilon so that round(duration, 3) always survives the filter even when
    # duration has sub-millisecond floating-point imprecision (e.g. 153.3999… rounds to
    # 153.4 but 153.4 <= 153.3999… is False, producing a single-element ordered list and
    # therefore an empty sequence).
    ordered = sorted(point for point in points if 0.0 <= point <= duration + 1e-9)
    import sys as _sys
    print(f"[DEBUG concat] temp_root={temp_root.name} dur={duration:.3f} ordered_len={len(ordered)} tl_len={len(timeline)} cues_len={len(cues)}", flush=True, file=_sys.stderr)

    header_cache: dict[int, Image.Image] = {}
    frame_cache: dict[tuple[int, int], Path] = {}
    sequence: list[tuple[Path, float]] = []
    for start, end in zip(ordered, ordered[1:]):
        if end - start < 0.01:
            continue
        mid = (start + end) / 2
        entry = current_track(timeline, mid)
        cue, cue_index = active_cue(cues, mid, 0)
        key = (entry.spec.number, cue_index if cue is not None else -1)
        if key not in frame_cache:
            header_path = frame_dir / f"header-track-{entry.spec.number:02d}.png"
            if entry.spec.number not in header_cache:
                if not header_path.exists():
                    render_header_frame(header_path, entry)
                header_cache[entry.spec.number] = Image.open(header_path).convert("RGBA")
            frame_path = frame_dir / f"overlay-track-{entry.spec.number:02d}-cue-{key[1]:04d}.png"
            if not frame_path.exists():
                render_combined_overlay_frame(frame_path, header_cache[entry.spec.number], cue)
            frame_cache[key] = frame_path
        sequence.append((frame_cache[key], end - start))

    # Defensive fallback: if sequence is somehow empty (e.g., duration rounds to same
    # as start point causing a single-element ordered list), build one static frame
    # covering the full duration so FFmpeg always gets a valid concat input.
    if not sequence:
        print(f"[WARN concat] sequence empty for dur={duration:.3f} ordered={ordered}; using static fallback", flush=True, file=_sys.stderr)
        fallback_entry = timeline[0] if timeline else None
        if fallback_entry is not None:
            fallback_key = (fallback_entry.spec.number, -1)
            if fallback_key not in frame_cache:
                header_path = frame_dir / f"header-track-{fallback_entry.spec.number:02d}.png"
                if fallback_entry.spec.number not in header_cache:
                    if not header_path.exists():
                        render_header_frame(header_path, fallback_entry)
                    header_cache[fallback_entry.spec.number] = Image.open(header_path).convert("RGBA")
                frame_path = frame_dir / f"overlay-track-{fallback_entry.spec.number:02d}-cue--001.png"
                if not frame_path.exists():
                    render_combined_overlay_frame(frame_path, header_cache[fallback_entry.spec.number], None)
                frame_cache[fallback_key] = frame_path
            sequence.append((frame_cache[fallback_key], max(duration, 0.1)))

    with concat_path.open("w", encoding="utf-8") as handle:
        handle.write("ffconcat version 1.0\n")
        for frame_path, frame_duration in sequence:
            handle.write(f"file '{quote_concat_path(frame_path)}'\n")
            handle.write(f"duration {frame_duration:.6f}\n")
        if sequence:
            handle.write(f"file '{quote_concat_path(sequence[-1][0])}'\n")

    print(f"[DEBUG concat] wrote {len(sequence)} entries to {concat_path.name}", flush=True, file=_sys.stderr)
    return concat_path, {
        "interval_count": len(sequence),
        "unique_overlay_frame_count": len(frame_cache),
        "subtitle_cue_count": len(cues),
        "renderer": "event_png_concat_no_full_duration_subtitle_qtrle",
    }


def segment_cues(cues: list[Cue], segment: RenderSegment) -> list[Cue]:
    shifted: list[Cue] = []
    for cue in cues:
        if cue.start < segment.end and cue.end > segment.start:
            shifted.append(
                Cue(
                    cue.slot,
                    max(0.0, cue.start - segment.start),
                    min(segment.duration, cue.end - segment.start),
                    cue.text,
                )
            )
    return shifted


def segment_timeline(segment: RenderSegment) -> list[TimelineTrack]:
    return [TimelineTrack(segment.entry.spec, 0.0, segment.duration, segment.entry.frames)]


def make_particle_texture(path: Path) -> None:
    """Night-rooftop dust layer with random-looking drift groups.

    The filter graph moves this double-height texture with slow mixed sine/cosine
    offsets, so the particles float around the room instead of only rising.
    """
    rng = random.Random(702)
    base = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(base, "RGBA")
    for _ in range(250):
        x = rng.triangular(16, WIDTH - 16, 520)
        y = rng.triangular(10, HEIGHT - 10, 360)
        r = rng.uniform(0.6, 2.6)
        alpha = int(rng.uniform(10, 48))
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(255, 224, 174, alpha))
    for _ in range(42):
        x = rng.triangular(120, 1280, 500)
        y = rng.triangular(36, 620, 230)
        r = rng.uniform(3.6, 10.5)
        alpha = int(rng.uniform(6, 20))
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(255, 238, 198, alpha))
    for _ in range(36):
        x = rng.triangular(1180, WIDTH - 20, 1540)
        y = rng.triangular(80, 720, 280)
        r = rng.uniform(0.8, 2.4)
        alpha = int(rng.uniform(6, 20))
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(166, 181, 224, alpha))
    base = base.filter(ImageFilter.GaussianBlur(0.32))
    texture = Image.new("RGBA", (WIDTH, HEIGHT * 2), (0, 0, 0, 0))
    texture.alpha_composite(base, (0, 0))
    texture.alpha_composite(base, (0, HEIGHT))
    texture.save(path)


def make_star_texture(path: Path) -> None:
    rng = random.Random(729)
    layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    for _ in range(80):
        x = rng.triangular(1110, WIDTH - 40, 1510)
        y = rng.triangular(40, 500, 170)
        r = rng.uniform(0.7, 2.2)
        alpha = int(rng.uniform(16, 58))
        color = (190, 205, 255, alpha) if rng.random() < 0.72 else (255, 231, 181, alpha)
        draw.ellipse((x - r, y - r, x + r, y + r), fill=color)
        if rng.random() < 0.22:
            draw.line((x - r * 2.2, y, x + r * 2.2, y), fill=color, width=1)
            draw.line((x, y - r * 2.2, x, y + r * 2.2), fill=color, width=1)
    for _ in range(14):
        x = rng.triangular(1180, WIDTH - 60, 1580)
        y = rng.triangular(70, 540, 240)
        r = rng.uniform(5.0, 14.0)
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(154, 171, 232, int(rng.uniform(5, 13))))
    layer = layer.filter(ImageFilter.GaussianBlur(0.18))
    layer.save(path)


def make_lamp_glow_texture(path: Path) -> None:
    layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    for index in range(9):
        inset = index * 72
        alpha = max(4, 30 - index * 3)
        draw.ellipse((210 - inset, 170 - inset, 1050 + inset, 820 + inset), fill=(255, 214, 150, alpha))
    draw.polygon([(260, 120), (520, 90), (1180, 870), (870, 930)], fill=(255, 221, 163, 11))
    draw.polygon([(420, 90), (590, 84), (1240, 830), (1020, 910)], fill=(255, 245, 205, 7))
    layer = layer.filter(ImageFilter.GaussianBlur(72))
    layer.save(path)


def make_light_sweep(path: Path) -> None:
    sweep_width = 2400
    layer = Image.new("RGBA", (sweep_width, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    draw.polygon([(-80, -120), (145, -120), (760, HEIGHT + 120), (520, HEIGHT + 120)], fill=(255, 226, 172, 13))
    draw.polygon([(150, -120), (260, -120), (880, HEIGHT + 120), (746, HEIGHT + 120)], fill=(255, 244, 210, 7))
    layer = layer.filter(ImageFilter.GaussianBlur(64))
    layer.save(path)


def make_night_glow_texture(path: Path) -> None:
    layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    for index in range(7):
        inset = index * 72
        draw.ellipse((40 - inset, -10 - inset, 940 + inset, 610 + inset), fill=(255, 224, 170, max(4, 22 - index * 3)))
    draw.polygon([(-100, -80), (220, -80), (760, HEIGHT + 120), (510, HEIGHT + 120)], fill=(255, 232, 188, 8))
    draw.polygon([(1180, 20), (WIDTH + 60, -80), (WIDTH + 60, 540), (1320, 420)], fill=(116, 136, 206, 7))
    layer = layer.filter(ImageFilter.GaussianBlur(68))
    layer.save(path)


def make_reflection_texture(path: Path) -> None:
    layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    for index, (x0, y0, x1, y1) in enumerate(((900, 720, 1450, 752), (1040, 790, 1600, 820), (1210, 856, 1760, 884), (230, 690, 740, 722))):
        draw.rounded_rectangle((x0, y0, x1, y1), radius=16, fill=(255, 232, 188, max(6, 16 - index * 3)))
    for index in range(4):
        y = 744 + index * 38
        draw.line((1010 + index * 50, y, 1690 - index * 35, y + 16), fill=(255, 248, 222, 7), width=5)
    layer = layer.filter(ImageFilter.GaussianBlur(20))
    layer.save(path)


def make_shadow_texture(path: Path) -> None:
    layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    draw.ellipse((1120, 620, 2050, 1210), fill=(24, 28, 48, 22))
    draw.ellipse((-220, 720, 720, 1240), fill=(72, 50, 34, 12))
    draw.polygon([(1500, -80), (2020, -40), (1940, 480), (1680, 390)], fill=(22, 28, 54, 9))
    layer = layer.filter(ImageFilter.GaussianBlur(58))
    layer.save(path)


def audio_energy(path: Path, fps: int, duration: float, *, start_seconds: float = 0.0, pre_roll_seconds: float = 2.0) -> list[float]:
    frame_count = math.ceil(duration * fps)
    analysis_start = max(0.0, start_seconds - pre_roll_seconds)
    pre_roll_actual = max(0.0, start_seconds - analysis_start)
    analysis_duration = duration + pre_roll_actual
    analysis_frame_count = math.ceil(analysis_duration * fps)
    with wave.open(str(path), "rb") as wav:
        sample_width = wav.getsampwidth()
        rate = wav.getframerate()
        start_frame = min(wav.getnframes(), max(0, int(round(analysis_start * rate))))
        wav.setpos(start_frame)
        total_frames = min(wav.getnframes(), start_frame + int(math.ceil(analysis_duration * rate)))
        values: list[float] = []
        last_frame = start_frame
        for frame in range(analysis_frame_count):
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
        coeff = 0.070 if value > prev else 0.034
        prev += (value - prev) * coeff
        smoothed.append(prev)
    averaged: list[float] = []
    radius = max(1, int(fps * 0.30))
    for index in range(len(smoothed)):
        start = max(0, index - radius)
        end = min(len(smoothed), index + radius + 1)
        averaged.append(sum(smoothed[start:end]) / (end - start))
    drop = min(len(averaged), int(round(pre_roll_actual * fps)))
    sliced = averaged[drop : drop + frame_count]
    if len(sliced) < frame_count:
        sliced.extend([sliced[-1] if sliced else 0.0] * (frame_count - len(sliced)))
    return sliced


def make_equalizer_frame(energy: float, t: float) -> Image.Image:
    layer = Image.new("RGBA", (EQ_WIDTH, EQ_HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    base_y = 70
    phase = t * 0.30
    amp = 5.0 + 16.0 * max(0.0, min(1.0, energy))
    for band, offset in enumerate((-15, 0, 15)):
        points = []
        for index in range(170):
            u = index / 169
            x = EQ_WIDTH * u
            arc = 30 * math.sin(u * math.pi * 0.78)
            wave = amp * math.sin(u * math.tau * 2.0 + phase + band * 0.55)
            points.append((x, base_y + arc + offset + wave))
        draw.line(points, fill=(186, 134, 68, 56 + band * 12), width=2 if band != 1 else 3)
    for index in range(18):
        u = index / 17
        x = EQ_WIDTH * u
        arc = 30 * math.sin(u * math.pi * 0.78)
        y = base_y + arc + amp * math.sin(u * math.tau * 2.0 + phase)
        r = 2.3 + 3.0 * energy * (0.65 + 0.35 * math.sin(phase + index * 0.8))
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(190, 137, 68, int(98 + 52 * energy)))
    return layer.filter(ImageFilter.GaussianBlur(0.28))


def build_equalizer_overlay(audio_path: Path, duration: float, temp_root: Path, *, start_seconds: float = 0.0) -> Path:
    output = temp_root / "s01e03-render-02-ribbon-equalizer-overlay.mov"
    if output.exists() and output.stat().st_size > 0:
        return output
    energies = audio_energy(project_path(audio_path), FPS, duration, start_seconds=start_seconds)
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


def build_visual_assets(audio_path: Path, duration: float, temp_root: Path, *, start_seconds: float = 0.0) -> dict[str, Path]:
    particle_path = temp_root / "s01e03-render-02-particles.png"
    star_path = temp_root / "s01e03-render-02-star-light.png"
    lamp_path = temp_root / "s01e03-render-02-lamp-glow.png"
    light_path = temp_root / "s01e03-render-02-light-sweep.png"
    glow_path = temp_root / "s01e03-render-02-night-glow.png"
    reflection_path = temp_root / "s01e03-render-02-reflection.png"
    shadow_path = temp_root / "s01e03-render-02-shadow.png"
    make_particle_texture(particle_path)
    make_star_texture(star_path)
    make_lamp_glow_texture(lamp_path)
    make_light_sweep(light_path)
    make_night_glow_texture(glow_path)
    make_reflection_texture(reflection_path)
    make_shadow_texture(shadow_path)
    return {
        "particles": particle_path,
        "stars": star_path,
        "lamp": lamp_path,
        "light": light_path,
        "glow": glow_path,
        "reflection": reflection_path,
        "shadow": shadow_path,
        "equalizer": build_equalizer_overlay(audio_path, duration, temp_root, start_seconds=start_seconds),
    }


def active_cue(cues: list[Cue], t: float, start_index: int) -> tuple[Cue | None, int]:
    index = start_index
    while index < len(cues) and cues[index].end <= t:
        index += 1
    if index < len(cues) and cues[index].start <= t < cues[index].end:
        return cues[index], index
    return None, index


def cue_signature(cues: list[Cue]) -> str:
    payload = json.dumps(
        [{"slot": cue.slot, "start": round(cue.start, 3), "end": round(cue.end, 3), "text": cue.text} for cue in cues],
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:12]


def subtitle_overlay_signature(cues: list[Cue], duration: float, time_offset_seconds: float) -> str:
    payload = json.dumps(
        {
            "cue_signature": cue_signature(cues),
            "duration_seconds": round(duration, 3),
            "subtitle_offset": round(time_offset_seconds, 3),
        },
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:14]


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
    # Lift up (slides up from +8 to 0) and slightly rightward slide (slides right from -4 to 0)
    return alpha, -4 * (1.0 - eased), 8 * (1.0 - eased)


def apply_alpha(layer: Image.Image, alpha: float) -> Image.Image:
    alpha = max(0.0, min(1.0, alpha))
    if alpha >= 0.999:
        return layer
    result = layer.copy()
    result.putalpha(result.getchannel("A").point(lambda value: int(value * alpha)))
    return result


def build_subtitle_overlay(
    cues: list[Cue],
    duration: float,
    temp_root: Path,
    *,
    signature: str | None = None,
    time_offset_seconds: float = SUBTITLE_EARLY_OFFSET_SECONDS,
) -> tuple[Path, dict[str, object]]:
    overlay_signature = signature or subtitle_overlay_signature(cues, duration, time_offset_seconds)
    output = temp_root / f"s01e03-subtitle-overlay-{overlay_signature}.mov"
    if output.exists() and output.stat().st_size > 0:
        return output, {"cue_count": len(cues), "canvas": f"{SUBTITLE_CANVAS_WIDTH}x{SUBTITLE_CANVAS_HEIGHT}", "position": {"x": SUBTITLE_OVERLAY_X, "y": SUBTITLE_OVERLAY_Y}, "reused_existing": True}
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
        t = frame / FPS + time_offset_seconds
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
    return output, {
        "cue_count": len(cues),
        "canvas": f"{SUBTITLE_CANVAS_WIDTH}x{SUBTITLE_CANVAS_HEIGHT}",
        "position": {"x": SUBTITLE_OVERLAY_X, "y": SUBTITLE_OVERLAY_Y},
        "time_offset_seconds": round(time_offset_seconds, 3),
    }


def render_video(
    audio_path: Path,
    output_root: Path,
    duration: float,
    temp_root: Path,
    cues: list[Cue],
    timeline: list[TimelineTrack],
    subtitle_early_offset: float = SUBTITLE_EARLY_OFFSET_SECONDS,
    *,
    visual_proof_seconds: float | None = None,
) -> tuple[Path, dict[str, object]]:
    subtitle_signature = subtitle_overlay_signature(cues, duration, subtitle_early_offset)
    if visual_proof_seconds is None:
        video_name = f"{EPISODE_ID}.local-render-02-draft-subtitled-{subtitle_signature}-1080p24-qa.mp4"
    else:
        safe_seconds = max(1, int(round(visual_proof_seconds)))
        video_name = f"{EPISODE_ID}.local-render-02-visual-proof-{safe_seconds}s-{subtitle_signature}.mp4"
    video_out = output_root / "video" / video_name
    if video_out.exists():
        return video_out, {"reused_existing": True}
    prepare_output(video_out)
    temp_suffix = "full" if visual_proof_seconds is None else f"proof-{max(1, int(round(visual_proof_seconds)))}s"
    temp_video = temp_root / f"s01e03-local-render-02-{temp_suffix}.tmp.mp4"
    if temp_video.exists():
        temp_video.unlink()
    overlay_concat, overlay_summary = build_combined_overlay_concat(timeline, [], duration, temp_root)
    subtitle_overlay, subtitle_summary = build_subtitle_overlay(
        cues,
        duration,
        temp_root,
        signature=subtitle_signature,
        time_offset_seconds=subtitle_early_offset,
    )
    music_note_overlay, music_note_summary = build_music_note_overlay(duration, temp_root)
    visual_assets = build_visual_assets(audio_path, duration, temp_root)
    bg = project_path(SELECTED_BACKGROUND)
    gt = global_time_expr(0.0)
    particle_x, particle_y = particle_motion_expr(gt)
    filter_graph = ";".join(
        [
            "[1:a]anull[aout]",
            "[0:v]scale=1928:1085:force_original_aspect_ratio=increase,"
            f"crop=1920:1080:x='(in_w-out_w)/2+sin({gt}*0.018)*0.30':"
            f"y='(in_h-out_h)/2+cos({gt}*0.016)*0.20',fps=24,format=rgba[bg]",
            "[9:v]format=rgba[shadow]",
            f"[bg][shadow]overlay=x='sin({gt}*0.030)*1.8':y='cos({gt}*0.027)*1.0':format=auto[withshadow]",
            "[3:v]format=rgba[pt]",
            f"[withshadow][pt]overlay=x='{particle_x}':y='{particle_y}':format=auto[withparticles]",
            "[4:v]format=rgba[stars]",
            f"[withparticles][stars]overlay=x='sin({gt}*0.015)*5':y='cos({gt}*0.019)*4':format=auto[withstars]",
            "[5:v]format=rgba[lamp]",
            f"[withstars][lamp]overlay=x='sin({gt}*0.050)*3':y='cos({gt}*0.043)*2':format=auto[withlamp]",
            "[6:v]format=rgba[light]",
            f"[withlamp][light]overlay=x='mod({gt}*5.8,2400)-520':y='sin({gt}*0.041)*8':format=auto[withlight]",
            "[7:v]format=rgba[glow]",
            f"[withlight][glow]overlay=x='sin({gt}*0.024)*10':y='cos({gt}*0.021)*6':format=auto[withglow]",
            "[8:v]format=rgba[ref]",
            f"[withglow][ref]overlay=x='sin({gt}*0.049)*7':y='cos({gt}*0.043)*4':format=auto[withref]",
            "[10:v]format=rgba[eq]",
            "[withref][eq]overlay=1452:850:format=auto[vis]",
            "[2:v]fps=24,format=rgba[ov]",
            "[vis][ov]overlay=0:0:format=auto[withheader]",
            "[12:v]fps=24,format=rgba[sub]",
            f"[withheader][sub]overlay={SUBTITLE_OVERLAY_X}:{SUBTITLE_OVERLAY_Y}:format=auto[withsub]",
            "[11:v]format=rgba[notes]",
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
        str(project_path(audio_path)),
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
        str(visual_assets["stars"]),
        "-loop",
        "1",
        "-framerate",
        str(FPS),
        "-i",
        str(visual_assets["lamp"]),
        "-loop",
        "1",
        "-framerate",
        str(FPS),
        "-i",
        str(visual_assets["light"]),
        "-loop",
        "1",
        "-framerate",
        str(FPS),
        "-i",
        str(visual_assets["glow"]),
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
        str(visual_assets["equalizer"]),
        "-i",
        str(music_note_overlay),
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
    return video_out, {
        "reused_existing": False,
        "combined_header_overlay": overlay_summary,
        "subtitle": subtitle_summary,
        "music_notes": music_note_summary,
        "equalizer": "ep1_render05_style_custom_ribbon_dot_overlay",
        "motion_atmosphere": "night-adapted random-drift particles, star/window bokeh, lamp glow, soft light sweep, glow, reflection, shadow, and near-still parallax",
        "render_mode": "full_local_qa" if visual_proof_seconds is None else "short_visual_proof",
    }


def segment_video_path(output_root: Path, segment: RenderSegment, *, cache_key: str) -> Path:
    return output_root / "video" / "segments" / f"{EPISODE_ID}.render-02-segment-{segment.index:02d}-track-{segment.entry.spec.number:02d}-{cache_key}.mp4"


def video_probe_matches(path: Path, expected_duration: float, tolerance: float = 0.16) -> bool:
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
    audio_path: Path,
    output_root: Path,
    temp_root: Path,
    cues: list[Cue],
    subtitle_early_offset: float = SUBTITLE_EARLY_OFFSET_SECONDS,
) -> tuple[Path, dict[str, object]]:
    """Render one video-only segment with all motion keyed to global time."""
    local_cues = segment_cues(cues, segment)
    segment_signature = f"{cue_signature(local_cues)}-{segment.entry.spec.number:02d}-{segment.index:02d}-{round(subtitle_early_offset,3)}-{round(segment.start,3)}"
    video_out = segment_video_path(output_root, segment, cache_key=segment_signature)
    if video_probe_matches(video_out, segment.duration):
        return video_out, {"reused_existing": True, "path": str(as_output_path(video_out))}
    prepare_output(video_out)
    temp_video = temp_root / f"s01e03-render-02-segment-{segment.index:02d}.tmp.mp4"
    if temp_video.exists():
        temp_video.unlink()
    local_timeline = segment_timeline(segment)
    overlay_concat, overlay_summary = build_combined_overlay_concat(local_timeline, [], segment.duration, temp_root)
    subtitle_signature = subtitle_overlay_signature(local_cues, segment.duration, subtitle_early_offset)
    subtitle_overlay, subtitle_summary = build_subtitle_overlay(
        local_cues,
        segment.duration,
        temp_root,
        signature=subtitle_signature,
        time_offset_seconds=subtitle_early_offset,
    )
    music_note_overlay, music_note_summary = build_music_note_overlay(segment.duration, temp_root, start_seconds=segment.start)
    visual_assets = build_visual_assets(audio_path, segment.duration, temp_root, start_seconds=segment.start)
    bg = project_path(SELECTED_BACKGROUND)
    gt = global_time_expr(segment.start)
    particle_x, particle_y = particle_motion_expr(gt)
    filter_graph = ";".join(
        [
            "[0:v]scale=1928:1085:force_original_aspect_ratio=increase,"
            f"crop=1920:1080:x='(in_w-out_w)/2+sin({gt}*0.018)*0.30':"
            f"y='(in_h-out_h)/2+cos({gt}*0.016)*0.20',fps=24,format=rgba[bg]",
            "[8:v]format=rgba[shadow]",
            f"[bg][shadow]overlay=x='sin({gt}*0.030)*1.8':y='cos({gt}*0.027)*1.0':format=auto[withshadow]",
            "[2:v]format=rgba[pt]",
            f"[withshadow][pt]overlay=x='{particle_x}':y='{particle_y}':format=auto[withparticles]",
            "[3:v]format=rgba[stars]",
            f"[withparticles][stars]overlay=x='sin({gt}*0.015)*5':y='cos({gt}*0.019)*4':format=auto[withstars]",
            "[4:v]format=rgba[lamp]",
            f"[withstars][lamp]overlay=x='sin({gt}*0.050)*3':y='cos({gt}*0.043)*2':format=auto[withlamp]",
            "[5:v]format=rgba[light]",
            f"[withlamp][light]overlay=x='mod({gt}*5.8,2400)-520':y='sin({gt}*0.041)*8':format=auto[withlight]",
            "[6:v]format=rgba[glow]",
            f"[withlight][glow]overlay=x='sin({gt}*0.024)*10':y='cos({gt}*0.021)*6':format=auto[withglow]",
            "[7:v]format=rgba[ref]",
            f"[withglow][ref]overlay=x='sin({gt}*0.049)*7':y='cos({gt}*0.043)*4':format=auto[withref]",
            "[9:v]format=rgba[eq]",
            "[withref][eq]overlay=1452:850:format=auto[vis]",
            "[1:v]fps=24,format=rgba[ov]",
            "[vis][ov]overlay=0:0:format=auto[withheader]",
            "[11:v]fps=24,format=rgba[sub]",
            f"[withheader][sub]overlay={SUBTITLE_OVERLAY_X}:{SUBTITLE_OVERLAY_Y}:format=auto[withsub]",
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
        str(visual_assets["stars"]),
        "-loop",
        "1",
        "-framerate",
        str(FPS),
        "-i",
        str(visual_assets["lamp"]),
        "-loop",
        "1",
        "-framerate",
        str(FPS),
        "-i",
        str(visual_assets["light"]),
        "-loop",
        "1",
        "-framerate",
        str(FPS),
        "-i",
        str(visual_assets["glow"]),
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
        str(visual_assets["equalizer"]),
        "-i",
        str(music_note_overlay),
        "-i",
        str(subtitle_overlay),
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
    return video_out, {
        "reused_existing": False,
        "path": str(as_output_path(video_out)),
        "overlay": overlay_summary,
        "music_notes": music_note_summary,
        "global_time_start_seconds": round(segment.start, 3),
        "subtitle_cue_count": len(local_cues),
    }


def write_concat_file(paths: list[Path], concat_path: Path) -> None:
    concat_path.parent.mkdir(parents=True, exist_ok=True)
    with concat_path.open("w", encoding="utf-8") as handle:
        handle.write("ffconcat version 1.0\n")
        for path in paths:
            handle.write(f"file '{quote_concat_path(path)}'\n")


def assemble_chunked_video(
    segment_paths: list[Path],
    audio_path: Path,
    output_root: Path,
    temp_root: Path,
    duration: float,
    video_signature: str,
) -> tuple[Path, dict[str, object]]:
    video_out = output_root / "video" / f"{EPISODE_ID}.local-render-02-draft-subtitled-{video_signature}-1080p24-qa.mp4"
    if video_probe_matches(video_out, duration, tolerance=0.22):
        return video_out, {"reused_existing": True, "segment_count": len(segment_paths)}
    prepare_output(video_out)
    concat_path = temp_root / "s01e03-render-02-segments.ffconcat"
    write_concat_file(segment_paths, concat_path)
    temp_video = temp_root / "s01e03-render-02-final.tmp.mp4"
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
        f"{duration:.3f}",
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


def render_chunked_video(
    audio_path: Path,
    output_root: Path,
    duration: float,
    temp_root: Path,
    cues: list[Cue],
    timeline: list[TimelineTrack],
    subtitle_early_offset: float = SUBTITLE_EARLY_OFFSET_SECONDS,
) -> tuple[Path, dict[str, object]]:
    audio_abs = project_path(audio_path)
    video_signature = subtitle_overlay_signature(cues, duration, subtitle_early_offset)
    segment_paths: list[Path] = []
    segment_summaries: list[dict[str, object]] = []
    for segment in render_segments(timeline, duration):
        segment_temp = temp_root / "segments" / f"segment-{segment.index:02d}"
        segment_temp.mkdir(parents=True, exist_ok=True)
        segment_path, segment_summary = run_ffmpeg_segment_render(
            segment,
            audio_abs,
            output_root,
            segment_temp,
            cues,
            subtitle_early_offset=subtitle_early_offset,
        )
        segment_paths.append(segment_path)
        segment_summaries.append(
            {
                "index": segment.index,
                "track": segment.entry.spec.number,
                "start_seconds": round(segment.start, 3),
                "duration_seconds": round(segment.duration, 3),
            }
            | segment_summary
        )
    video_path, assembly_summary = assemble_chunked_video(
        segment_paths,
        audio_abs,
        output_root,
        temp_root,
        duration,
        video_signature,
    )
    return video_path, {
        "render_mode": "chunked_per_song_global_time",
        "segment_count": len(segment_summaries),
        "segments": segment_summaries,
        "assembly": assembly_summary,
        "continuity": "segment effects use t + segment_start and final audio is one continuous WAV master",
        "particle_motion": "deterministic random-looking drift with slow mixed x/y motion, not upward-only scrolling; includes star/window bokeh and lamp glow sway",
    }


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
        "path": str(as_output_path(project_path(path))),
        "bytes": project_path(path).stat().st_size,
        "duration_seconds": round(float(probe.get("format", {}).get("duration", 0.0)), 3),
        "video": {"codec": video_stream.get("codec_name"), "width": video_stream.get("width"), "height": video_stream.get("height"), "frame_rate": video_stream.get("r_frame_rate")},
        "audio": {"codec": audio_stream.get("codec_name"), "sample_rate": audio_stream.get("sample_rate"), "channels": audio_stream.get("channels")},
    }


def extract_snapshots(video_path: Path, output_root: Path, duration: float) -> list[str]:
    specs = [
        ("s01e03-render-02-sample-01-open.png", 2.0),
        ("s01e03-render-02-sample-02-track03.png", 370.0),
        ("s01e03-render-02-sample-03-track06.png", 900.0),
        ("s01e03-render-02-sample-04-track09.png", 1450.0),
        ("s01e03-render-02-sample-05-track12.png", 2090.0),
        ("s01e03-render-02-sample-06-ending.png", max(1.0, duration - 8.0)),
    ]
    snapshot_dir = output_root / "qa" / "snapshots"
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[str] = []
    for name, timestamp in specs:
        path = snapshot_dir / name
        if path.exists():
            Image.open(path).verify()
            outputs.append(str(as_output_path(path)))
            continue
        prepare_output(path)
        subprocess.run(
            ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{timestamp:.3f}", "-i", str(project_path(video_path)), "-frames:v", "1", str(path)],
            check=True,
        )
        Image.open(path).verify()
        outputs.append(str(as_output_path(path)))
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
    parser.add_argument(
        "--subtitle-early-offset",
        type=float,
        default=SUBTITLE_EARLY_OFFSET_SECONDS,
        help="Shift subtitle render time in seconds (positive = earlier than cue start, default 0.00).",
    )
    parser.add_argument(
        "--visual-proof-seconds",
        type=float,
        default=None,
        help="Render a short visual proof with the render-02 overlay/motion stack instead of the full longplay.",
    )
    parser.add_argument(
        "--allow-draft-subtitles",
        action="store_true",
        help=(
            "Permit draft subtitle sidecars for manual preview only. "
            "Local production path should use final .en.srt/.en.vtt and keep this flag off."
        ),
    )
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
    render_duration = duration
    if args.visual_proof_seconds is not None:
        render_duration = min(duration, max(1.0, float(args.visual_proof_seconds)))
    subtitle_source = resolve_subtitle_lane(
        episode_id=EPISODE_ID,
        promoted_srt=PROMOTED_SRT,
        promoted_vtt=PROMOTED_VTT,
        draft_srt=DRAFT_SRT,
        draft_vtt=DRAFT_VTT,
        fallback_srt=SOURCE_SUBTITLE_ROOT / f"{EPISODE_ID}.draft.en.srt",
        fallback_vtt=SOURCE_SUBTITLE_ROOT / f"{EPISODE_ID}.draft.en.vtt",
        allow_draft_subtitles=args.allow_draft_subtitles,
        require_final_lane=not args.allow_draft_subtitles,
    )
    print(f"Loading {subtitle_source.lane} subtitle lane from {subtitle_source.source_srt}...")
    if subtitle_source.lane in {"final", "draft"}:
        raw_srt_cues = parse_srt(project_path(subtitle_source.source_srt))
        cues = assign_slots_from_timeline(raw_srt_cues, timeline)
    else:
        cues = generate_draft_cues(timeline)
    subtitle_timing_method = subtitle_source.timing_method
    subtitle_onset_evidence = []
    subtitle_timing_evidence = {"status": "insufficient"}
    subtitle_onset_window_seconds = 0.45
    subtitle_drift_ms = None
    if subtitle_source.lane in {"final", "draft"}:
        subtitle_drift_ms, subtitle_onset_evidence, subtitle_timing_evidence, subtitle_onset_window_seconds = infer_subtitle_drift_with_fallback(
            Path(audio_summary["path"]),
            cues,
            timeline=timeline,
        )
        if isinstance(subtitle_timing_evidence, dict):
            if subtitle_timing_evidence.get("timing_method") in {"track-aligned_stable_ts_drift", "track-aligned_episode_source_srt", "track-aligned_episode_source_draft_srt"}:
                subtitle_timing_method = str(subtitle_timing_evidence.get("timing_method"))
    cues, subtitle_timing_drift = apply_onset_drift_to_cues(cues, subtitle_drift_ms, timeline)
    if subtitle_timing_evidence["status"] == "ok":
        subtitle_timing_summary = {
            "mean_abs_delta_ms": subtitle_timing_evidence.get("mean_abs_delta_ms"),
            "max_abs_delta_ms": subtitle_timing_evidence.get("max_abs_delta_ms"),
            "delta_count": subtitle_timing_evidence.get("delta_count"),
        }
    else:
        subtitle_timing_summary = {"status": subtitle_timing_evidence.get("status")}
    subtitle_summary = write_subtitles(
        cues,
        timeline,
        duration,
        output_root,
        source_srt=subtitle_source.source_srt,
        source_vtt=subtitle_source.source_vtt,
        timing_method=subtitle_timing_method,
        subtitle_lane=lane_summary(subtitle_source),
    )
    if args.visual_proof_seconds is None:
        video_path, render_summary = render_chunked_video(
            Path(audio_summary["path"]),
            output_root,
            duration,
            temp_root,
            cues,
            timeline,
            args.subtitle_early_offset,
        )
    else:
        video_path, render_summary = render_video(
            Path(audio_summary["path"]),
            output_root,
            render_duration,
            temp_root,
            cues,
            timeline,
            args.subtitle_early_offset,
            visual_proof_seconds=args.visual_proof_seconds,
        )
    snapshots = [] if args.visual_proof_seconds is not None else extract_snapshots(video_path, output_root, duration)
    decode = decode_check(video_path)
    summary = {
        "episode_id": EPISODE_ID,
        "status": "local_render_02_visual_revision_created_with_ep1_render05_overlay_motion_standard_needs_human_watch",
        "intake": intake,
        "selected_visual": image_summary(SELECTED_BACKGROUND),
        "audio_master": audio_summary,
        "render_duration_seconds": round(render_duration, 3),
        "subtitle_draft": subtitle_summary,
        "subtitle_timing_method": subtitle_timing_method,
        "subtitle_timing_drift": subtitle_timing_drift,
        "subtitle_timing_evidence": subtitle_timing_evidence,
        "subtitle_timing_window_seconds": round(subtitle_onset_window_seconds, 3),
        "subtitle_timing_summary": subtitle_timing_summary,
        "rendered_video": summarize_probe(video_path),
        "render_pipeline": render_summary,
        "decode_check": decode,
        "snapshots": snapshots,
        "visual_policy": "EP1 render-05 headphone icon, music notes, particles/light, custom ribbon-dot equalizer, and near-still motion are the canonical video overlay standard; S01E03 adapts them to the rooftop golden hour image",
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
