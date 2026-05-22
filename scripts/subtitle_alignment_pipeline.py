#!/usr/bin/env python3
"""Local subtitle alignment helpers for Mellow Longplay episodes.

This script is intentionally local-only. It does not upload, call provider APIs,
or mutate external accounts. Generated evidence should stay under outputs/ unless
the caller explicitly promotes reviewed sidecars into source-controlled subtitle
paths.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable, NamedTuple


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = Path("outputs/subtitle-alignment-prototype")
DEFAULT_TRACK1_AUDIO = Path("candidates/s01e01-campus-cafe-longplay/audio/selected/aud-t01_c02--margin-notes-at-table-three.wav")
DEFAULT_TRACK1_PROOF_DIR = Path("candidates/s01e01-campus-cafe-longplay/subtitles/proofs/track-01")
DEFAULT_SONG_SOURCE = Path("channel/episodes/s01e01-campus-cafe-longplay/source/songs.md")


class Cue(NamedTuple):
    slot: str
    start: float
    end: float
    text: str
    section: str | None = None
    line_index: int | None = None
    confidence: float | None = None
    source: str | None = None
    vocal_start: float | None = None
    vocal_end: float | None = None


def q3(value: float) -> float:
    return round(float(value) + 0.0, 3)


def clamp01(value: float) -> float:
    return min(1.0, max(0.0, value))


def smootherstep(value: float) -> float:
    value = clamp01(value)
    return value * value * value * (value * (value * 6.0 - 15.0) + 10.0)


def subtitle_motion_alpha_and_offset(
    t: float,
    start: float,
    end: float,
    *,
    fade_in: float,
    fade_out: float,
    slide_pixels: float = 18.0,
    slide_out_pixels: float = 0.0,
) -> tuple[float, float]:
    fade_in_progress = smootherstep((t - start) / max(0.001, fade_in))
    fade_out_progress = smootherstep((end - t) / max(0.001, fade_out))
    alpha = min(fade_in_progress, fade_out_progress)
    if fade_in_progress <= fade_out_progress:
        y_offset = slide_pixels * (1.0 - fade_in_progress)
    else:
        y_offset = slide_out_pixels * (1.0 - fade_out_progress)
    return alpha, y_offset


def project_path(path: Path | str) -> Path:
    path = Path(path)
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


def episode_slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "episode"


def assert_safe_generated_path(path: Path) -> None:
    """Keep generated prototype files under ignored local evidence roots."""
    resolved = path.resolve()
    allowed_roots = [
        (PROJECT_ROOT / "outputs").resolve(),
        (PROJECT_ROOT / "candidates").resolve(),
    ]
    if not any(root in [resolved, *resolved.parents] for root in allowed_roots):
        raise ValueError(f"refusing to write generated prototype outside outputs/ or candidates/: {path}")


def load_json(path: Path | str) -> Any:
    return json.loads(project_path(path).read_text(encoding="utf-8"))


def clean_subtitle_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    return text


def is_stage_direction(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("[") and stripped.endswith("]")


def parse_track_from_song_source(source_path: Path | str, track_number: int) -> dict[str, Any]:
    source = project_path(source_path).read_text(encoding="utf-8")
    pattern = re.compile(
        rf"^### Track {track_number}(?:\s+Bonus)?\s+—\s+(.*?)\n```text\n(.*?)\n```",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(source)
    if not match:
        raise ValueError(f"track {track_number} lyric block not found in {source_path}")
    title = match.group(1).strip()
    body = match.group(2)
    sections: list[dict[str, Any]] = []
    current_section = "lyrics"
    current_lines: list[str] = []
    for raw_line in body.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if is_stage_direction(line):
            if current_lines:
                sections.append({"section": current_section, "lines": current_lines})
                current_lines = []
            current_section = line.strip("[]")
            continue
        current_lines.append(line)
    if current_lines:
        sections.append({"section": current_section, "lines": current_lines})
    return {
        "slot": f"T{track_number:02d}",
        "working_title": title,
        "sections": sections,
    }


def find_track(segments: dict[str, Any], slot: str) -> dict[str, Any]:
    for track in segments.get("tracks", []):
        if track.get("slot") == slot:
            return track
    raise KeyError(f"track slot not found: {slot}")


def normalized_section_name(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def build_track_text(track: dict[str, Any], excluded_sections: Iterable[str] = ()) -> tuple[str, list[dict[str, Any]]]:
    lines: list[str] = []
    meta: list[dict[str, Any]] = []
    excluded = {normalized_section_name(section) for section in excluded_sections}
    for section in track.get("sections", []):
        section_name = section.get("section")
        if normalized_section_name(section_name or "") in excluded:
            continue
        for index, line in enumerate(section.get("lines", [])):
            cleaned = clean_subtitle_text(line)
            if not cleaned:
                continue
            lines.append(cleaned)
            meta.append(
                {
                    "slot": track.get("slot"),
                    "working_title": track.get("working_title"),
                    "section": section_name,
                    "line_index": index,
                    "text": cleaned,
                }
            )
    return "\n".join(lines), meta


def wrap_subtitle_text(text: str, max_line_chars: int = 37) -> str:
    text = clean_subtitle_text(text)
    if len(text) <= max_line_chars:
        return text
    words = text.split()
    if len(words) <= 2:
        return text
    best_index = None
    best_score = float("inf")
    for index in range(1, len(words)):
        left = " ".join(words[:index])
        right = " ".join(words[index:])
        if len(left) > max_line_chars or len(right) > max_line_chars:
            continue
        score = abs(len(left) - len(right))
        if score < best_score:
            best_index = index
            best_score = score
    if best_index is None:
        return text
    return " ".join(words[:best_index]) + "\n" + " ".join(words[best_index:])


def track_title_to_audio_path(audio_root: Path | str, track: dict[str, Any]) -> Path:
    title = track["working_title"]
    return project_path(audio_root) / f"{title}.wav"


def audio_duration_seconds(audio_path: Path | str) -> float:
    audio_path = project_path(audio_path)
    try:
        import soundfile as sf  # type: ignore

        info = sf.info(str(audio_path))
        return q3(info.frames / float(info.samplerate))
    except Exception:
        import wave

        with wave.open(str(audio_path), "rb") as wav:
            return q3(wav.getnframes() / float(wav.getframerate()))


def compute_track_timeline(track_durations: Iterable[tuple[str, float]], gap_seconds: float) -> list[dict[str, Any]]:
    if gap_seconds < 0:
        raise ValueError("gap_seconds must be non-negative")
    entries = list(track_durations)
    current = 0.0
    timeline: list[dict[str, Any]] = []
    for index, (slot, duration) in enumerate(entries):
        if duration <= 0:
            raise ValueError(f"duration must be positive for {slot}: {duration}")
        start = q3(current)
        end = q3(start + duration)
        is_last = index == len(entries) - 1
        gap_start = None if is_last else end
        gap_end = None if is_last else q3(end + gap_seconds)
        timeline.append(
            {
                "slot": slot,
                "track_start": start,
                "track_end": end,
                "duration": q3(duration),
                "gap_start": gap_start,
                "gap_end": gap_end,
            }
        )
        current = end if is_last or gap_end is None else gap_end
    return timeline


def shift_track_cues(
    local_cues: Iterable[Cue],
    track_start: float,
    track_end: float,
    early_offset: float,
    end_padding: float = 0.0,
    min_duration: float = 0.25,
    min_gap: float = 0.02,
) -> list[Cue]:
    if early_offset < 0:
        raise ValueError("early_offset must be non-negative")
    if end_padding < 0:
        raise ValueError("end_padding must be non-negative")
    shifted: list[Cue] = []
    prev_end: float | None = None
    sorted_cues = sorted(local_cues, key=lambda c: (c.start, c.end))
    for index, cue in enumerate(sorted_cues):
        start = max(track_start, track_start + cue.start - early_offset)
        next_boundary = track_end
        if index + 1 < len(sorted_cues):
            next_cue = sorted_cues[index + 1]
            next_start = max(track_start, track_start + next_cue.start - early_offset)
            next_boundary = min(track_end, next_start - min_gap)
        end = min(track_end, next_boundary, track_start + cue.end + end_padding)
        if prev_end is not None and start < prev_end + min_gap:
            start = prev_end + min_gap
        if end <= start:
            end = min(track_end, next_boundary, start + min_duration)
        if end <= start or start >= track_end:
            continue
        shifted_cue = Cue(
            slot=cue.slot,
            start=q3(start),
            end=q3(end),
            text=cue.text,
            section=cue.section,
            line_index=cue.line_index,
            confidence=cue.confidence,
            source=cue.source,
            vocal_start=cue.vocal_start,
            vocal_end=cue.vocal_end,
        )
        shifted.append(shifted_cue)
        prev_end = shifted_cue.end
    return shifted


def apply_subtitle_display_timing(
    local_cues: Iterable[Cue],
    *,
    track_start: float = 0.0,
    track_end: float | None = None,
    lead_in: float = 0.20,
    tail_hold: float = 0.24,
    fade_out: float = 0.16,
    min_gap: float = 0.08,
    min_duration: float = 0.62,
) -> list[Cue]:
    """Convert vocal cue bounds into subtitle display bounds.

    `start`/`end` in the returned cue are display timings. The original sung
    bounds stay in `vocal_start`/`vocal_end`. Display timing leads the vocal a
    little for fade-in, holds briefly after the sung phrase, and clamps before
    the next cue so subtitles never overlap.
    """
    if lead_in < 0 or tail_hold < 0 or fade_out < 0 or min_gap < 0:
        raise ValueError("subtitle timing padding values must be non-negative")
    sorted_cues = sorted(local_cues, key=lambda c: ((c.vocal_start if c.vocal_start is not None else c.start), c.end))
    if track_end is None:
        track_end = max((cue.vocal_end if cue.vocal_end is not None else cue.end) for cue in sorted_cues) if sorted_cues else track_start
    adjusted: list[Cue] = []
    for index, cue in enumerate(sorted_cues):
        vocal_start = cue.vocal_start if cue.vocal_start is not None else cue.start
        vocal_end = cue.vocal_end if cue.vocal_end is not None else cue.end
        display_start = max(track_start, vocal_start - lead_in)
        display_end = min(track_end, vocal_end + tail_hold + fade_out)
        if index + 1 < len(sorted_cues):
            next_cue = sorted_cues[index + 1]
            next_vocal_start = next_cue.vocal_start if next_cue.vocal_start is not None else next_cue.start
            next_display_start = max(track_start, next_vocal_start - lead_in)
            display_end = min(display_end, next_display_start - min_gap)
        if adjusted and display_start < adjusted[-1].end + min_gap:
            display_start = adjusted[-1].end + min_gap
        if display_end < display_start + min_duration:
            display_end = min(track_end, display_start + min_duration)
        if index + 1 < len(sorted_cues):
            next_cue = sorted_cues[index + 1]
            next_vocal_start = next_cue.vocal_start if next_cue.vocal_start is not None else next_cue.start
            display_end = min(display_end, max(track_start, next_vocal_start - lead_in) - min_gap)
        if display_end <= display_start:
            continue
        adjusted.append(
            Cue(
                slot=cue.slot,
                start=q3(display_start),
                end=q3(display_end),
                text=wrap_subtitle_text(cue.text),
                section=cue.section,
                line_index=cue.line_index,
                confidence=cue.confidence,
                source=cue.source,
                vocal_start=q3(vocal_start),
                vocal_end=q3(vocal_end),
            )
        )
    return adjusted


def seconds_to_srt_timestamp(seconds: float) -> str:
    seconds = max(0.0, seconds)
    millis = int(round(seconds * 1000))
    hours, rem = divmod(millis, 3_600_000)
    minutes, rem = divmod(rem, 60_000)
    secs, ms = divmod(rem, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"


def seconds_to_vtt_timestamp(seconds: float) -> str:
    return seconds_to_srt_timestamp(seconds).replace(",", ".")


def serialize_srt(cues: Iterable[Cue]) -> str:
    blocks: list[str] = []
    for idx, cue in enumerate(cues, start=1):
        blocks.append(
            f"{idx}\n{seconds_to_srt_timestamp(cue.start)} --> {seconds_to_srt_timestamp(cue.end)}\n{cue.text}"
        )
    return "\n\n".join(blocks) + "\n"


def serialize_vtt(cues: Iterable[Cue]) -> str:
    blocks = ["WEBVTT", "", "NOTE LOCAL ALIGNMENT DRAFT ONLY. Requires human sung-lyric watch pass."]
    for cue in cues:
        blocks.append("")
        blocks.append(f"{seconds_to_vtt_timestamp(cue.start)} --> {seconds_to_vtt_timestamp(cue.end)}")
        blocks.append(cue.text)
    return "\n".join(blocks) + "\n"


def cue_to_dict(cue: Cue) -> dict[str, Any]:
    return {
        "slot": cue.slot,
        "start": q3(cue.start),
        "end": q3(cue.end),
        "text": cue.text,
        "section": cue.section,
        "line_index": cue.line_index,
        "confidence": cue.confidence,
        "source": cue.source,
        "vocal_start": None if cue.vocal_start is None else q3(cue.vocal_start),
        "vocal_end": None if cue.vocal_end is None else q3(cue.vocal_end),
    }


def dict_to_cue(data: dict[str, Any]) -> Cue:
    return Cue(
        slot=data["slot"],
        start=float(data["start"]),
        end=float(data["end"]),
        text=data["text"],
        section=data.get("section"),
        line_index=data.get("line_index"),
        confidence=data.get("confidence"),
        source=data.get("source"),
        vocal_start=data.get("vocal_start"),
        vocal_end=data.get("vocal_end"),
    )


def word_probability(word: dict[str, Any]) -> float | None:
    value = word.get("probability")
    return None if value is None else float(value)


def adjusted_segment_bounds(segment: dict[str, Any], *, max_stretched_word: float = 3.0, low_probability: float = 0.20) -> tuple[float, float, bool]:
    words = segment.get("words") or []
    start = float(segment.get("start", 0.0))
    end = float(segment.get("end", start))
    corrected = False
    if words:
        first = words[0]
        last = words[-1]
        start = float(first.get("start", start))
        end = float(last.get("end", end))
        first_duration = float(first.get("end", start)) - float(first.get("start", start))
        probability = word_probability(first)
        if len(words) > 1 and first_duration > max_stretched_word and (probability is None or probability < low_probability):
            second_start = float(words[1].get("start", start))
            start = max(0.0, second_start - 1.0)
            corrected = True
    return q3(start), q3(end), corrected


def stable_result_to_local_cues(result: Any, slot: str, line_meta: list[dict[str, Any]]) -> list[Cue]:
    if hasattr(result, "to_dict"):
        data = result.to_dict()
    elif isinstance(result, dict):
        data = result
    else:
        data = json.loads(result.to_json())
    segments = data.get("segments", [])
    cues: list[Cue] = []
    for index, segment in enumerate(segments):
        start, end, corrected = adjusted_segment_bounds(segment)
        meta = line_meta[index] if index < len(line_meta) else {}
        text = clean_subtitle_text(meta.get("text") or segment.get("text") or "")
        if not text or end <= start:
            continue
        avg_logprob = segment.get("avg_logprob")
        words = segment.get("words") or []
        probabilities = [word_probability(word) for word in words]
        probabilities = [value for value in probabilities if value is not None]
        confidence = q3(sum(probabilities) / len(probabilities)) if probabilities else (None if avg_logprob is None else q3(math.exp(float(avg_logprob))))
        cues.append(
            Cue(
                slot=slot,
                start=q3(start),
                end=q3(end),
                text=text,
                section=meta.get("section"),
                line_index=meta.get("line_index"),
                confidence=confidence,
                source="stable-ts-align+stretched-word-correction" if corrected else "stable-ts-align",
                vocal_start=q3(start),
                vocal_end=q3(end),
            )
        )
    return cues


def seconds_to_ass_timestamp(seconds: float) -> str:
    seconds = max(0.0, seconds)
    centis = int(round(seconds * 100))
    hours, rem = divmod(centis, 360_000)
    minutes, rem = divmod(rem, 6_000)
    secs, cs = divmod(rem, 100)
    return f"{hours}:{minutes:02d}:{secs:02d}.{cs:02d}"


def ass_escape(text: str) -> str:
    return text.replace("\\", r"\\").replace("{", r"\{").replace("}", r"\}").replace("\n", r"\N")


def serialize_ass(cues: Iterable[Cue], *, title: str, fade_in_ms: int = 1500, fade_out_ms: int = 1000) -> str:
    header = f"""[Script Info]
Title: {title} subtitle timing proof
ScriptType: v4.00+
WrapStyle: 2
ScaledBorderAndShadow: yes
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: ProofSub,Avenir Next,64,&H00F6E8D8,&H00F6E8D8,&H80261712,&H70261712,0,0,0,0,100,100,0,0,1,3,1,2,190,190,150,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = [header.rstrip()]
    for cue in cues:
        text = ass_escape(wrap_subtitle_text(cue.text))
        lines.append(
            f"Dialogue: 0,{seconds_to_ass_timestamp(cue.start)},{seconds_to_ass_timestamp(cue.end)},ProofSub,,0,0,0,,{{\\fad({fade_in_ms},{fade_out_ms})}}{text}"
        )
    return "\n".join(lines) + "\n"


def assert_no_overlap(cues: list[Cue], min_gap: float = 0.0) -> None:
    for previous, current in zip(cues, cues[1:]):
        if previous.end + min_gap > current.start + 0.0005:
            raise ValueError(f"subtitle overlap: {previous.end} -> {current.start}")


def cue_review_summary(cues: list[Cue], *, min_gap: float) -> dict[str, Any]:
    gaps = [q3(current.start - previous.end) for previous, current in zip(cues, cues[1:])]
    max_line_chars = 0
    for cue in cues:
        max_line_chars = max(max_line_chars, *(len(line) for line in cue.text.split("\n")))
    return {
        "cue_count": len(cues),
        "min_gap_seconds": min(gaps) if gaps else None,
        "requested_min_gap_seconds": min_gap,
        "max_line_chars": max_line_chars,
        "low_confidence_cues": [index + 1 for index, cue in enumerate(cues) if cue.confidence is not None and cue.confidence < 0.55],
        "stretched_word_corrections": [index + 1 for index, cue in enumerate(cues) if cue.source and "stretched-word-correction" in cue.source],
    }


def estimate_onset_deltas(audio_path: Path | str, cues: list[Cue], window_seconds: float = 0.40) -> list[dict[str, Any]]:
    """Return nearest onset around cue starts as supporting evidence, not authority.

    This is deliberately an optional confidence signal. Pitch/onset can help find
    phrase starts, but music transients can be false positives, so alignment still
    needs ASR/forced alignment plus human review.
    """
    try:
        import librosa  # type: ignore
        import numpy as np  # type: ignore
    except Exception as exc:  # pragma: no cover - optional dependency path
        return [{"status": "unavailable", "reason": str(exc)}]

    y, sr = librosa.load(str(project_path(audio_path)), sr=22050, mono=True)
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr, units="frames", backtrack=True)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)
    evidence: list[dict[str, Any]] = []
    for cue in cues:
        if len(onset_times) == 0:
            evidence.append({"cue_start": cue.start, "nearest_onset": None, "delta_ms": None})
            continue
        deltas = onset_times - cue.start
        mask = np.abs(deltas) <= window_seconds
        if not mask.any():
            evidence.append({"cue_start": cue.start, "nearest_onset": None, "delta_ms": None})
            continue
        nearest_index = int(np.argmin(np.abs(deltas)))
        evidence.append(
            {
                "cue_start": q3(cue.start),
                "nearest_onset": q3(float(onset_times[nearest_index])),
                "delta_ms": int(round(float(deltas[nearest_index]) * 1000)),
            }
        )
    return evidence


def align_track(args: argparse.Namespace) -> Path:
    import stable_whisper  # type: ignore

    segments = load_json(args.segments)
    track = find_track(segments, args.slot)
    text, line_meta = build_track_text(track)
    audio_path = track_title_to_audio_path(args.audio_root, track)
    out_dir = project_path(args.out_dir)
    assert_safe_generated_path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    model = stable_whisper.load_model(args.model)
    align = getattr(model, "align")
    result = align(
        str(audio_path),
        text,
        language=args.language,
        original_split=True,
        nonspeech_skip=args.nonspeech_skip,
        verbose=args.verbose,
    )
    cues = stable_result_to_local_cues(result, args.slot, line_meta)
    onset_evidence = estimate_onset_deltas(audio_path, cues) if args.onset_evidence else []

    output = {
        "schema_version": "0.1.0",
        "status": "prototype_alignment_requires_human_watch_pass",
        "slot": args.slot,
        "working_title": track.get("working_title"),
        "method": "stable-ts-align",
        "model": args.model,
        "language": args.language,
        "audio_path": str(audio_path.relative_to(PROJECT_ROOT)),
        "audio_duration_seconds": audio_duration_seconds(audio_path),
        "line_count_expected": len(line_meta),
        "cue_count_returned": len(cues),
        "line_count_matches": len(line_meta) == len(cues),
        "notes": [
            "Generated locally from planned lyrics and local audio; not a final caption claim.",
            "Onset/pitch-like evidence is advisory only; music transients can be false positives.",
        ],
        "cues": [cue_to_dict(cue) for cue in cues],
        "onset_evidence": onset_evidence,
    }
    slug = episode_slug(args.episode_id)
    out_path = out_dir / f"{slug}-{args.slot.lower()}-stable-ts-alignment.json"
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (out_dir / f"{slug}-{args.slot.lower()}-stable-ts.local.srt").write_text(serialize_srt(cues), encoding="utf-8")
    print(out_path.relative_to(PROJECT_ROOT))
    return out_path


def align_song_source_track(args: argparse.Namespace) -> Path:
    import stable_whisper  # type: ignore

    track = parse_track_from_song_source(args.song_source, args.track_number)
    slot = args.slot or track["slot"]
    excluded_sections = tuple(args.exclude_sections or ())
    text, line_meta = build_track_text(track | {"slot": slot}, excluded_sections=excluded_sections)
    audio_path = project_path(args.audio)
    out_dir = project_path(args.out_dir)
    assert_safe_generated_path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    model = stable_whisper.load_model(args.model)
    result = model.align(
        str(audio_path),
        text,
        language=args.language,
        original_split=True,
        nonspeech_skip=args.nonspeech_skip,
        fast_mode=args.fast_mode,
        verbose=args.verbose,
    )
    if result is None:
        raise RuntimeError("stable-ts returned no alignment result")
    raw_cues = stable_result_to_local_cues(result, slot, line_meta)
    duration = audio_duration_seconds(audio_path)
    display_cues = apply_subtitle_display_timing(
        raw_cues,
        track_start=0.0,
        track_end=duration,
        lead_in=args.lead_in,
        tail_hold=args.tail_hold,
        fade_out=args.fade_out,
        min_gap=args.min_gap,
        min_duration=args.min_duration,
    )
    assert_no_overlap(display_cues, min_gap=args.min_gap)
    onset_evidence = estimate_onset_deltas(audio_path, raw_cues) if args.onset_evidence else []

    prefix = args.prefix or f"s01e01-track-{args.track_number:02d}-subtitle-alignment-draft-01"
    json_path = out_dir / f"{prefix}.json"
    srt_path = out_dir / f"{prefix}.draft.srt"
    vtt_path = out_dir / f"{prefix}.draft.vtt"
    ass_path = out_dir / f"{prefix}.proof.ass"
    video_path = out_dir / f"{prefix}.proof.mp4"

    output = {
        "schema_version": "0.2.0",
        "status": "draft_alignment_requires_human_watch_pass",
        "boundary": "Local subtitle timing proof only. Not final sidecars, render/export, upload, release, or rights/platform-safety approval.",
        "slot": slot,
        "track_number": args.track_number,
        "working_title": track.get("working_title"),
        "method": "stable-ts-align-with-display-padding",
        "model": args.model,
        "language": args.language,
        "audio_path": str(audio_path.relative_to(PROJECT_ROOT)),
        "audio_duration_seconds": duration,
        "display_timing_rules": {
            "lead_in_seconds": args.lead_in,
            "tail_hold_seconds": args.tail_hold,
            "fade_in_seconds": args.fade_in,
            "fade_out_seconds": args.fade_out,
            "min_gap_seconds": args.min_gap,
            "min_duration_seconds": args.min_duration,
            "note": "Returned cue start/end are display bounds; vocal_start/vocal_end preserve aligned sung bounds.",
        },
        "excluded_sections": list(excluded_sections),
        "proof_motion_rules": {
            "motion_fade_in_seconds": args.motion_fade_in,
            "motion_fade_out_seconds": args.motion_fade_out,
            "slide_in_pixels": args.motion_slide_pixels,
            "slide_out_pixels": args.motion_slide_out_pixels,
            "note": "Proof video motion only; these values do not change subtitle cue start/end timings.",
        },
        "line_count_expected": len(line_meta),
        "raw_cue_count": len(raw_cues),
        "display_cue_count": len(display_cues),
        "line_count_matches": len(line_meta) == len(raw_cues),
        "review_summary": cue_review_summary(display_cues, min_gap=args.min_gap),
        "notes": [
            "Generated locally from approved source lyrics and selected local audio.",
            "First-word stretched silence corrections are applied where stable-ts assigns an implausibly long low-confidence first word over an instrumental intro/break.",
            "Draft SRT/VTT are proof sidecars only; final sidecars remain blocked until reviewed timing and final assembly timeline exist.",
        ],
        "raw_cues": [cue_to_dict(cue) for cue in raw_cues],
        "display_cues": [cue_to_dict(cue) for cue in display_cues],
        "onset_evidence": onset_evidence,
    }
    json_path.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    srt_path.write_text(serialize_srt(display_cues), encoding="utf-8")
    vtt_path.write_text(serialize_vtt(display_cues), encoding="utf-8")
    ass_path.write_text(serialize_ass(display_cues, title=track.get("working_title") or slot, fade_in_ms=int(args.motion_fade_in * 1000), fade_out_ms=int(args.motion_fade_out * 1000)), encoding="utf-8")

    if not args.no_render:
        render_subtitle_proof_video(
            audio_path,
            video_path,
            display_cues,
            duration=duration,
            fps=args.fps,
            fade_in=args.motion_fade_in,
            fade_out=args.motion_fade_out,
            slide_pixels=args.motion_slide_pixels,
            slide_out_pixels=args.motion_slide_out_pixels,
        )
    print(json_path.relative_to(PROJECT_ROOT))
    return json_path


def render_subtitle_proof_video(
    audio_path: Path,
    video_path: Path,
    cues: list[Cue],
    *,
    duration: float,
    fps: int = 24,
    fade_in: float = 1.50,
    fade_out: float = 1.00,
    slide_pixels: float = 18.0,
    slide_out_pixels: float = 0.0,
) -> None:
    from PIL import Image, ImageDraw, ImageFilter, ImageFont

    width = 1920
    height = 1080
    frames = int(math.ceil(duration * fps))
    font_paths = [
        "/System/Library/Fonts/Supplemental/ChalkboardSE.ttc",
        "/System/Library/Fonts/Avenir Next.ttc",
        "/System/Library/Fonts/HelveticaNeue.ttc",
    ]
    font = None
    for font_path in font_paths:
        path = Path(font_path)
        if not path.exists():
            continue
        try:
            font = ImageFont.truetype(str(path), 72)
            break
        except OSError:
            continue
    if font is None:
        font = ImageFont.load_default(size=72)

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
        f"{width}x{height}",
        "-r",
        str(fps),
        "-i",
        "-",
        "-i",
        str(audio_path),
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
        str(video_path),
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    assert process.stdin is not None
    for frame in range(frames):
        t = frame / fps
        image = Image.new("RGBA", (width, height), (36, 29, 25, 255))
        active = next((cue for cue in cues if cue.start <= t <= cue.end), None)
        if active is not None:
            alpha, y_offset = subtitle_motion_alpha_and_offset(
                t,
                active.start,
                active.end,
                fade_in=fade_in,
                fade_out=fade_out,
                slide_pixels=slide_pixels,
                slide_out_pixels=slide_out_pixels,
            )
            layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(layer, "RGBA")
            text = active.text
            bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=18, stroke_width=2)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
            cx = width // 2
            cy = 760 + y_offset
            draw.rounded_rectangle(
                (cx - text_w / 2 - 58, cy - text_h / 2 - 36, cx + text_w / 2 + 58, cy + text_h / 2 + 36),
                radius=34,
                fill=(18, 13, 10, int(88 * alpha)),
                outline=(246, 219, 180, int(80 * alpha)),
                width=2,
            )
            draw.multiline_text(
                (cx, cy - text_h / 2),
                text,
                font=font,
                fill=(250, 234, 213, int(255 * alpha)),
                anchor="ma",
                align="center",
                spacing=18,
                stroke_width=2,
                stroke_fill=(34, 24, 18, int(210 * alpha)),
            )
            image.alpha_composite(layer.filter(ImageFilter.GaussianBlur(0.05)))
        process.stdin.write(image.convert("RGB").tobytes())
    process.stdin.close()
    result = process.wait()
    if result != 0:
        raise RuntimeError(f"ffmpeg exited with {result}")


def build_longplay(args: argparse.Namespace) -> Path:
    segments = load_json(args.segments)
    slots = args.slots or [track["slot"] for track in segments.get("tracks", [])]
    track_entries: list[tuple[dict[str, Any], float]] = []
    for slot in slots:
        track = find_track(segments, slot)
        track_entries.append((track, audio_duration_seconds(track_title_to_audio_path(args.audio_root, track))))
    timeline = compute_track_timeline([(track["slot"], duration) for track, duration in track_entries], args.gap_seconds)

    all_cues: list[Cue] = []
    alignment_dir = project_path(args.alignment_dir)
    slug = episode_slug(args.episode_id)
    for entry in timeline:
        slot = entry["slot"]
        alignment_path = alignment_dir / f"{slug}-{slot.lower()}-stable-ts-alignment.json"
        if not alignment_path.exists():
            if args.require_all:
                raise FileNotFoundError(alignment_path)
            continue
        alignment = json.loads(alignment_path.read_text(encoding="utf-8"))
        local_cues = [dict_to_cue(cue) for cue in alignment.get("cues", [])]
        all_cues.extend(
            shift_track_cues(
                local_cues,
                track_start=float(entry["track_start"]),
                track_end=float(entry["track_end"]),
                early_offset=args.early_offset,
                end_padding=args.end_padding,
            )
        )
    all_cues.sort(key=lambda cue: (cue.start, cue.end))

    out_dir = project_path(args.out_dir)
    assert_safe_generated_path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    prefix = args.prefix or f"{slug}-aligned-draft-gap-prototype"
    srt_path = out_dir / f"{prefix}.srt"
    vtt_path = out_dir / f"{prefix}.vtt"
    timeline_path = out_dir / f"{prefix}-timeline.json"
    srt_path.write_text(serialize_srt(all_cues), encoding="utf-8")
    vtt_path.write_text(serialize_vtt(all_cues), encoding="utf-8")
    timeline_path.write_text(
        json.dumps(
            {
                "schema_version": "0.1.0",
                "status": "prototype_longplay_alignment_requires_human_watch_pass",
                "gap_seconds": args.gap_seconds,
                "early_offset_seconds": args.early_offset,
                "end_padding_seconds": args.end_padding,
                "timeline": timeline,
                "cue_count": len(all_cues),
                "coverage_slots": sorted({cue.slot for cue in all_cues}),
                "notes": [
                    "Inter-song gaps are intentionally blank: no subtitle cues are generated inside gap intervals.",
                    "This is not final/upload-ready; actual sung lyric match requires human watch pass.",
                ],
                "cues": [cue_to_dict(cue) for cue in all_cues],
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    print(timeline_path.relative_to(PROJECT_ROOT))
    return timeline_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    align_parser = subparsers.add_parser("align-track", help="Align one track with stable-ts")
    align_parser.add_argument("--slot", required=True)
    align_parser.add_argument("--episode-id", required=True)
    align_parser.add_argument("--segments", required=True)
    align_parser.add_argument("--audio-root", required=True)
    align_parser.add_argument("--out-dir", default=str(DEFAULT_OUTPUT_DIR))
    align_parser.add_argument("--model", default="base.en")
    align_parser.add_argument("--language", default="en")
    align_parser.add_argument("--nonspeech-skip", type=float, default=5.0)
    align_parser.add_argument("--onset-evidence", action="store_true")
    align_parser.add_argument("--verbose", action="store_true")
    align_parser.set_defaults(func=align_track)

    source_parser = subparsers.add_parser("align-song-source-track", help="Align one song-source track and render a subtitle-only proof")
    source_parser.add_argument("--track-number", type=int, default=1)
    source_parser.add_argument("--slot", default=None)
    source_parser.add_argument("--song-source", default=str(DEFAULT_SONG_SOURCE))
    source_parser.add_argument("--audio", default=str(DEFAULT_TRACK1_AUDIO))
    source_parser.add_argument("--out-dir", default=str(DEFAULT_TRACK1_PROOF_DIR))
    source_parser.add_argument("--prefix", default=None)
    source_parser.add_argument("--model", default="base.en")
    source_parser.add_argument("--language", default="en")
    source_parser.add_argument("--nonspeech-skip", type=float, default=5.0)
    source_parser.add_argument("--lead-in", type=float, default=0.20)
    source_parser.add_argument("--tail-hold", type=float, default=0.24)
    source_parser.add_argument("--fade-in", type=float, default=0.34)
    source_parser.add_argument("--fade-out", type=float, default=0.30)
    source_parser.add_argument("--motion-fade-in", type=float, default=1.50)
    source_parser.add_argument("--motion-fade-out", type=float, default=1.00)
    source_parser.add_argument("--motion-slide-pixels", type=float, default=18.0)
    source_parser.add_argument("--motion-slide-out-pixels", type=float, default=0.0)
    source_parser.add_argument("--exclude-sections", nargs="*", default=[])
    source_parser.add_argument("--min-gap", type=float, default=0.08)
    source_parser.add_argument("--min-duration", type=float, default=0.62)
    source_parser.add_argument("--fps", type=int, default=24)
    source_parser.add_argument("--fast-mode", action="store_true", default=False)
    source_parser.add_argument("--onset-evidence", action="store_true")
    source_parser.add_argument("--no-render", action="store_true")
    source_parser.add_argument("--verbose", action="store_true")
    source_parser.set_defaults(func=align_song_source_track)

    build_parser = subparsers.add_parser("build-longplay", help="Combine per-track alignment JSON files")
    build_parser.add_argument("--episode-id", required=True)
    build_parser.add_argument("--segments", required=True)
    build_parser.add_argument("--audio-root", required=True)
    build_parser.add_argument("--alignment-dir", default=str(DEFAULT_OUTPUT_DIR))
    build_parser.add_argument("--out-dir", default=str(DEFAULT_OUTPUT_DIR))
    build_parser.add_argument("--prefix", default=None)
    build_parser.add_argument("--gap-seconds", type=float, default=1.75)
    build_parser.add_argument("--early-offset", type=float, default=0.20)
    build_parser.add_argument("--end-padding", type=float, default=0.30)
    build_parser.add_argument("--slots", nargs="*")
    build_parser.add_argument("--require-all", action="store_true")
    build_parser.set_defaults(func=build_longplay)

    args = parser.parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
