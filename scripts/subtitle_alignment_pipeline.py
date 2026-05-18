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
import sys
from pathlib import Path
from typing import Any, Iterable, NamedTuple


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = Path("outputs/subtitle-alignment-prototype")


class Cue(NamedTuple):
    slot: str
    start: float
    end: float
    text: str
    section: str | None = None
    line_index: int | None = None
    confidence: float | None = None
    source: str | None = None


def q3(value: float) -> float:
    return round(float(value) + 0.0, 3)


def project_path(path: Path | str) -> Path:
    path = Path(path)
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


def episode_slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "episode"


def assert_safe_generated_path(path: Path) -> None:
    """Keep generated prototype files under outputs/."""
    resolved = path.resolve()
    outputs_root = (PROJECT_ROOT / "outputs").resolve()
    if outputs_root not in [resolved, *resolved.parents]:
        raise ValueError(f"refusing to write generated prototype outside outputs/: {path}")


def load_json(path: Path | str) -> Any:
    return json.loads(project_path(path).read_text(encoding="utf-8"))


def clean_subtitle_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    return text


def find_track(segments: dict[str, Any], slot: str) -> dict[str, Any]:
    for track in segments.get("tracks", []):
        if track.get("slot") == slot:
            return track
    raise KeyError(f"track slot not found: {slot}")


def build_track_text(track: dict[str, Any]) -> tuple[str, list[dict[str, Any]]]:
    lines: list[str] = []
    meta: list[dict[str, Any]] = []
    for section in track.get("sections", []):
        section_name = section.get("section")
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
        )
        shifted.append(shifted_cue)
        prev_end = shifted_cue.end
    return shifted


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
    )


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
        start = float(segment.get("start", 0.0))
        end = float(segment.get("end", start))
        meta = line_meta[index] if index < len(line_meta) else {}
        text = clean_subtitle_text(segment.get("text") or meta.get("text") or "")
        if not text or end <= start:
            continue
        avg_logprob = segment.get("avg_logprob")
        confidence = None if avg_logprob is None else q3(math.exp(float(avg_logprob)))
        cues.append(
            Cue(
                slot=slot,
                start=q3(start),
                end=q3(end),
                text=text,
                section=meta.get("section"),
                line_index=meta.get("line_index"),
                confidence=confidence,
                source="stable-ts-align",
            )
        )
    return cues


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
