#!/usr/bin/env python3
"""Shared subtitle lane policy helpers for local render scripts.

The policy is simple and global:
- production lane defaults to final `.en.srt/.en.vtt` files
- draft lane is only used when `--allow-draft-subtitles` is set
- when final lane is partially missing, preview/render fails fast
"""

from __future__ import annotations

import json
from dataclasses import dataclass
import re
from pathlib import Path
from difflib import SequenceMatcher
from statistics import mean, median
from typing import Any

TIMING_METHOD_FINAL = "track-aligned_episode_source_srt"
TIMING_METHOD_DRAFT = "track-aligned_episode_source_draft_srt"
TIMING_METHOD_MECHANICAL = "mechanical_even_distribution_from_source_lyrics_needs_human_watch"
TIMING_METHOD_STABLE_TS = "track-aligned_stable_ts_drift"
ONSET_WINDOW_SECONDS_CANDIDATES = (0.45, 0.75, 1.0)
ONSET_MIN_DELTA_COUNT = 6
ONSET_MIN_SLOT_DELTA_COUNT = 4
EPISODE_ID_PATTERN = re.compile(r"^s\d{2}e\d{2}-[a-z0-9-]+$")
TRACK_ALIGNMENT_JSON_PATTERN = re.compile(
    r"^(?P<episode>s\d{2}e\d{2}(?:-[a-z0-9-]+)?)-track-(?P<track>\d{2})-subtitle-alignment(?:-draft-01)?\.json$"
)


def _normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", (value or "").strip().lower())


def _safe_text_match(left: str, right: str) -> bool:
    return _text_similarity_ratio(left, right) >= 0.82


def _text_similarity_ratio(left: str, right: str) -> float:
    left_norm = _normalize_text(left)
    right_norm = _normalize_text(right)
    if not left_norm or not right_norm:
        return 0.0
    if left_norm == right_norm:
        return 1.0
    return SequenceMatcher(None, left_norm, right_norm, autojunk=False).ratio()


def _find_best_source_match_for_proof(
    source_cues: list[Any],
    start_index: int,
    proof_text: str,
    *,
    min_ratio: float = 0.82,
    max_lookahead: int = 24,
) -> tuple[int, float] | None:
    if not proof_text:
        return None
    if start_index >= len(source_cues):
        return None
    end_index = min(len(source_cues), start_index + max(8, max_lookahead))
    best_index = None
    best_ratio = 0.0
    for candidate_index in range(start_index, end_index):
        source_text = _cue_text(source_cues[candidate_index])
        ratio = _text_similarity_ratio(source_text, proof_text)
        if ratio <= best_ratio:
            continue
        best_index = candidate_index
        best_ratio = ratio
        if ratio == 1.0:
            break
    if best_ratio < min_ratio or best_index is None:
        return None
    return best_index, best_ratio


def _cue_slot(value: Any) -> str | None:
    slot = getattr(value, "slot", None)
    if isinstance(slot, str):
        slot = slot.strip()
        if slot:
            return slot
    return None


def _cue_start(value: Any) -> float | None:
    raw = getattr(value, "start", None)
    if isinstance(raw, int | float):
        return float(raw)
    return None


def _cue_end(value: Any) -> float | None:
    raw = getattr(value, "end", None)
    if isinstance(raw, int | float):
        return float(raw)
    return None


def _cue_text(value: Any) -> str:
    raw = getattr(value, "text", "")
    return str(raw or "")


def _iter_timeline_slots(timeline: Any) -> dict[str, dict[str, float]]:
    if not timeline:
        return {}
    slots: dict[str, dict[str, float]] = {}
    for entry in timeline:
        slot_value = None
        start = None
        end = None
        number = None

        if isinstance(entry, dict):
            slot_value = entry.get("slot")
            start = entry.get("start")
            end = entry.get("end")
            if start is None:
                spec = entry.get("spec")
                if isinstance(spec, dict):
                    slot_value = spec.get("slot") if slot_value is None else slot_value
                    if slot_value is None:
                        number = spec.get("number")
                    else:
                        number = None
                else:
                    number = None
            else:
                number = None
            if slot_value is None and isinstance(number, int):
                slot_value = f"T{number:02d}"
        else:
            slot_value = getattr(entry, "slot", None)
            start = getattr(entry, "start", None)
            end = getattr(entry, "end", None)
            number = getattr(getattr(entry, "spec", None), "number", None)
            if number is None:
                number = getattr(getattr(entry, "track", None), "number", None)
            if slot_value is None and isinstance(number, int):
                slot_value = f"T{number:02d}"

        if slot_value is None:
            continue
        slot = str(slot_value).strip()
        if not slot.startswith("T") and slot.isdigit():
            slot = f"T{int(slot):02d}"
        if not isinstance(start, int | float) or not isinstance(end, int | float):
            continue
        if not slot:
            continue
        slots[slot] = {"start": float(start), "end": float(end)}
    return slots


def _infer_slot_for_time(value: float, timeline_slots: dict[str, dict[str, float]]) -> str | None:
    for slot, bounds in timeline_slots.items():
        if value >= bounds["start"] and value <= bounds["end"]:
            return slot
    return None


def _infer_episode_and_proof_root(audio_path: Path) -> tuple[str, Path] | None:
    if audio_path is None:
        return None
    path = audio_path.resolve()
    if not path.exists():
        return None
    for parent in (path, *path.parents):
        if parent.parent is not None and parent.parent.name == "candidates":
            episode_id = parent.name
            if EPISODE_ID_PATTERN.match(episode_id):
                proof_root = parent / "subtitles" / "proofs"
                if proof_root.exists():
                    return episode_id, proof_root
    return None


def _collect_stable_ts_track_files(audio_path: Path) -> tuple[str | None, list[tuple[str, Path]]]:
    location = _infer_episode_and_proof_root(audio_path)
    if location is None:
        return None, []
    episode_id, proof_root = location
    episode_prefix = episode_id.split("-", 1)[0]
    files: list[tuple[str, Path]] = []
    for path in sorted(proof_root.rglob("*.json")):
        if "fast-check" in path.name:
            continue
        match = TRACK_ALIGNMENT_JSON_PATTERN.match(path.name)
        if not match:
            continue
        if match.group("episode") not in {episode_id, episode_prefix}:
            continue
        slot = f"T{int(match.group('track')):02d}"
        files.append((slot, path))
    return episode_id, files


def _load_stable_ts_reference_evidence(audio_path: Path, cues: list[Any], timeline: Any | None = None) -> tuple[list[dict[str, Any]], dict[str, object]]:
    episode_id, proof_files = _collect_stable_ts_track_files(audio_path)
    if not proof_files:
        return [], {
            "status": "insufficient",
            "status_reason": "no_stable_ts_alignment_json_found",
            "proof_candidate_count": 0,
            "episode_id": episode_id,
            "total_cues": len(cues),
        }
    proof_by_slot: dict[str, Path] = {}
    for slot, path in proof_files:
        if slot not in proof_by_slot:
            proof_by_slot[slot] = path
    timeline_slots = _iter_timeline_slots(timeline)
    cues_by_slot: dict[str, list[Any]] = {}
    for cue in cues:
        slot = _cue_slot(cue)
        if not slot:
            if timeline_slots:
                start = _cue_start(cue) or 0.0
                end = _cue_end(cue) or start
                slot = _infer_slot_for_time((start + end) / 2, timeline_slots)
            if not slot:
                continue
        cues_by_slot.setdefault(slot, []).append(cue)
    for cue_list in cues_by_slot.values():
        cue_list.sort(key=lambda item: _cue_start(item) or 0.0)

    evidence: list[dict[str, Any]] = []
    used_slots: set[str] = set()
    used_track_files = 0
    total_display_cues = 0
    for slot, proof_path in sorted(proof_by_slot.items()):
        source_cues = cues_by_slot.get(slot, [])
        if not source_cues:
            continue
        source_cues = sorted(source_cues, key=lambda item: _cue_start(item) or 0.0)
        try:
            data = json.loads(proof_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        proof_cues = data.get("display_cues") or []
        if not isinstance(proof_cues, list):
            continue
        total_display_cues += len(proof_cues)
        if len(proof_cues) == 0:
            continue
        used_track_files += 1
        used_slots.add(slot)
        track_start = timeline_slots.get(slot, {}).get("start")
        if track_start is None:
            continue
        source_cursor = 0
        previous_delta_ms: float | None = None
        total_lookahead = max(12, 24, int(len(source_cues) * 0.18))
        for proof_index, raw_proof in enumerate(proof_cues):
            if not isinstance(raw_proof, dict):
                continue
            proof_text = str(raw_proof.get("text") or "")
            if not proof_text.strip():
                continue
            proof_start = raw_proof.get("start")
            if not isinstance(proof_start, int | float):
                continue
            source_match = _find_best_source_match_for_proof(
                source_cues,
                source_cursor,
                proof_text,
                min_ratio=0.74,
                max_lookahead=total_lookahead,
            )
            if source_match is None:
                continue
            source_index, match_ratio = source_match
            source = source_cues[source_index]
            source_text = _cue_text(source)
            source_start = _cue_start(source)
            if source_start is None:
                continue

            proof_start_float = float(proof_start)
            delta_ms = (source_start - (track_start + proof_start_float)) * 1000.0
            if previous_delta_ms is not None and abs(delta_ms - previous_delta_ms) > 12500.0:
                continue

            source_cursor = source_index + 1
            previous_delta_ms = delta_ms
            evidence.append(
                {
                    "slot": slot,
                    "cue_start": round(source_start, 3),
                    "proof_start": round(proof_start_float, 3),
                    "proof_file": str(proof_path),
                    "track_start": round(track_start, 3),
                    "proof_index": proof_index,
                    "source_index": source_index,
                    "proof_text": proof_text,
                    "cue_text": source_text,
                    "match_ratio": round(match_ratio, 3),
                    "delta_ms": round(delta_ms, 3),
                    "source": "stable-ts-track-alignment",
                }
            )

    if not evidence:
        return [], {
            "status": "insufficient",
            "status_reason": "stable_ts_data_found_but_no_alignable_pairs",
            "proof_slot_count": len(used_slots),
            "proof_candidate_count": used_track_files,
            "total_display_cues": total_display_cues,
            "delta_count": 0,
            "total_cues": len(cues),
            "episode_id": episode_id,
        }
    return evidence, {
        "status": "available",
        "proof_slot_count": len(used_slots),
        "proof_candidate_count": used_track_files,
        "total_display_cues": total_display_cues,
        "delta_count": len(evidence),
        "total_cues": len(cues),
        "episode_id": episode_id,
        "evidence_source": "stable-ts-track-json",
    }


@dataclass(frozen=True)
class SubtitleLaneDecision:
    lane: str
    source_srt: Path
    source_vtt: Path
    timing_method: str
    allow_draft_subtitles: bool
    final_srt_exists: bool
    final_vtt_exists: bool
    draft_srt_exists: bool
    draft_vtt_exists: bool


def resolve_subtitle_lane(
    *,
    episode_id: str,
    promoted_srt: Path,
    promoted_vtt: Path,
    draft_srt: Path | None,
    draft_vtt: Path | None,
    fallback_srt: Path,
    fallback_vtt: Path,
    allow_draft_subtitles: bool,
    require_final_lane: bool = True,
) -> SubtitleLaneDecision:
    """Resolve subtitle lane and return deterministic source paths.

    Args:
      promoted_*: canonical final lane paths in channel/episodes/<episode>/subtitles
      draft_*: optional draft lane paths in channel/episodes/<episode>/subtitles
      fallback_*: files to use when generated fallback is allowed
      allow_draft_subtitles: user explicitly allowed local draft preview
      require_final_lane: production mode gate (default: true)
    """

    final_srt_exists = promoted_srt.exists()
    final_vtt_exists = promoted_vtt.exists()
    draft_srt_exists = bool(draft_srt and draft_srt.exists())
    draft_vtt_exists = bool(draft_vtt and draft_vtt.exists())

    if final_srt_exists and final_vtt_exists:
        return SubtitleLaneDecision(
            lane="final",
            source_srt=promoted_srt,
            source_vtt=promoted_vtt,
            timing_method=TIMING_METHOD_FINAL,
            allow_draft_subtitles=allow_draft_subtitles,
            final_srt_exists=True,
            final_vtt_exists=True,
            draft_srt_exists=draft_srt_exists,
            draft_vtt_exists=draft_vtt_exists,
        )

    if final_srt_exists or final_vtt_exists:
        missing = []
        if not final_srt_exists:
            missing.append(f"{promoted_srt.name}")
        if not final_vtt_exists:
            missing.append(f"{promoted_vtt.name}")
        raise FileNotFoundError(
            f"Final subtitle lane incomplete for {episode_id}: expected channel/episodes/{episode_id}/subtitles/{episode_id}.en.srt and .en.vtt, missing: {', '.join(missing)}"
        )

    if allow_draft_subtitles and draft_srt_exists and draft_vtt_exists:
        return SubtitleLaneDecision(
            lane="draft",
            source_srt=draft_srt,  # type: ignore[arg-type]
            source_vtt=draft_vtt,  # type: ignore[arg-type]
            timing_method=TIMING_METHOD_DRAFT,
            allow_draft_subtitles=True,
            final_srt_exists=False,
            final_vtt_exists=False,
            draft_srt_exists=True,
            draft_vtt_exists=True,
        )

    if not require_final_lane:
        return SubtitleLaneDecision(
            lane="generated_fallback",
            source_srt=fallback_srt,
            source_vtt=fallback_vtt,
            timing_method=TIMING_METHOD_MECHANICAL,
            allow_draft_subtitles=allow_draft_subtitles,
            final_srt_exists=False,
            final_vtt_exists=False,
            draft_srt_exists=draft_srt_exists,
            draft_vtt_exists=draft_vtt_exists,
        )

    if allow_draft_subtitles:
        raise FileNotFoundError(
            "No final subtitle sidecars found. Production render requires subtitles/"
            f"{episode_id}.en.srt and .en.vtt. If this is a local QA smoke-test, run with --allow-draft-subtitles."
        )

    raise FileNotFoundError(
        "No final subtitle sidecars found. Production render requires subtitles/"
        f"{episode_id}.en.srt and .en.vtt."
    )


def lane_summary(decision: SubtitleLaneDecision) -> dict[str, object]:
    return {
        "lane": decision.lane,
        "timing_method": decision.timing_method,
        "source_srt": str(decision.source_srt),
        "source_vtt": str(decision.source_vtt),
        "final_exists": {
            "srt": decision.final_srt_exists,
            "vtt": decision.final_vtt_exists,
        },
        "draft_exists": {
            "srt": decision.draft_srt_exists,
            "vtt": decision.draft_vtt_exists,
        },
    }


def estimate_subtitle_onset_evidence(audio_path: Path, cues: list[Any], *, window_seconds: float = 0.45) -> list[dict[str, Any]]:
    """Return optional onset alignment evidence. This is advisory only."""
    try:
        from subtitle_alignment_pipeline import estimate_onset_deltas
    except Exception:
        return []
    try:
        evidence = estimate_onset_deltas(audio_path, cues, window_seconds=window_seconds)
    except Exception:
        return []

    if not evidence or not isinstance(evidence, list) or len(evidence) != len(cues):
        return evidence if isinstance(evidence, list) else []

    enriched: list[dict[str, Any]] = []
    for cue, sample in zip(cues, evidence):
        if not isinstance(sample, dict):
            enriched.append({})
            continue
        slot = getattr(cue, "slot", None)
        if isinstance(slot, str) and slot:
            sample = dict(sample)
            sample.setdefault("slot", slot)
        enriched.append(sample)
    return enriched


def _collect_deltas(evidence: list[dict[str, Any]]) -> list[float]:
    return [float(item.get("delta_ms")) for item in evidence if isinstance(item, dict) and isinstance(item.get("delta_ms"), int | float)]


def _collect_slot_deltas(evidence: list[dict[str, Any]]) -> dict[str, list[float]]:
    deltas_by_slot: dict[str, list[float]] = {}
    for entry in evidence:
        slot = entry.get("slot")
        delta = entry.get("delta_ms")
        if not isinstance(slot, str) or not slot:
            continue
        if not isinstance(delta, int | float):
            continue
        deltas_by_slot.setdefault(slot, []).append(float(delta))
    return deltas_by_slot


def _trim_sorted(values: list[float], trim_ratio: float) -> list[float]:
    if not values:
        return []
    values = sorted(values)
    trim = int(len(values) * trim_ratio)
    if trim:
        values = values[trim:-trim]
    return values


def _infer_drift_from_deltas(
    deltas: list[float],
    *,
    min_delta_count: int,
    trim_ratio: float,
    min_abs_ms: float,
    max_abs_ms: float,
    max_span_ms: float,
    max_outlier_ratio: float,
) -> float | None:
    deltas = _trim_sorted(deltas, trim_ratio)
    if len(deltas) < min_delta_count:
        return None

    median_delta = deltas[len(deltas) // 2]
    if abs(median_delta) < min_abs_ms:
        return None
    if abs(median_delta) > max_abs_ms:
        return None

    span_ms = deltas[-1] - deltas[0]
    if span_ms > max_span_ms:
        return None

    median_abs_residual = median([abs(item - median_delta) for item in deltas])
    outlier_threshold = max(min_abs_ms, median_abs_residual * 3.2)
    outlier_count = sum(1 for item in deltas if abs(item - median_delta) > outlier_threshold)
    if outlier_count / max(1, len(deltas)) > max_outlier_ratio:
        return None

    return round(median_delta, 3)


def infer_slotwise_drift_ms(
    evidence: list[dict[str, Any]],
    *,
    min_delta_count: int = ONSET_MIN_DELTA_COUNT,
    min_slot_delta_count: int = ONSET_MIN_SLOT_DELTA_COUNT,
    trim_ratio: float = 0.2,
    min_abs_ms: float = 22.0,
    max_abs_ms: float = 1500.0,
    max_span_ms: float = 600.0,
    max_outlier_ratio: float = 0.5,
) -> dict[str, float]:
    slot_drifts, _ = infer_slotwise_drift_ms_with_counts(
        evidence,
        min_delta_count=min_delta_count,
        min_slot_delta_count=min_slot_delta_count,
        trim_ratio=trim_ratio,
        min_abs_ms=min_abs_ms,
        max_abs_ms=max_abs_ms,
        max_span_ms=max_span_ms,
        max_outlier_ratio=max_outlier_ratio,
    )
    return slot_drifts


def infer_slotwise_drift_ms_with_counts(
    evidence: list[dict[str, Any]],
    *,
    min_delta_count: int = ONSET_MIN_DELTA_COUNT,
    min_slot_delta_count: int = ONSET_MIN_SLOT_DELTA_COUNT,
    trim_ratio: float = 0.2,
    min_abs_ms: float = 22.0,
    max_abs_ms: float = 1500.0,
    max_span_ms: float = 600.0,
    max_outlier_ratio: float = 0.5,
) -> tuple[dict[str, float], dict[str, int]]:
    deltas_by_slot = _collect_slot_deltas(evidence)

    slot_drifts: dict[str, float] = {}
    slot_support_counts: dict[str, int] = {}
    for slot, deltas in deltas_by_slot.items():
        if len(deltas) < min_slot_delta_count:
            continue
        drift_ms = _infer_drift_from_deltas(
            deltas,
            min_delta_count=min_slot_delta_count,
            trim_ratio=trim_ratio,
            min_abs_ms=min_abs_ms,
            max_abs_ms=max_abs_ms,
            max_span_ms=max_span_ms,
            max_outlier_ratio=max_outlier_ratio,
        )
        if drift_ms is None:
            continue
        slot_drifts[slot] = drift_ms
        slot_support_counts[slot] = len(deltas)
    return slot_drifts, slot_support_counts


def summarize_onset_evidence(evidence: list[dict[str, Any]]) -> dict[str, object]:
    deltas = _collect_deltas(evidence)
    if not deltas:
        return {
            "status": "insufficient",
            "total_cues": len(evidence),
            "delta_count": 0,
            "coverage_ratio": 0.0,
            "mean_delta_ms": None,
            "median_delta_ms": None,
            "span_delta_ms": None,
        }
    abs_deltas = [abs(float(item)) for item in deltas]
    deltas_sorted = sorted(float(item) for item in deltas)
    hottest = sorted(
        [entry for entry in evidence if isinstance(entry, dict) and entry.get("delta_ms") is not None],
        key=lambda item: abs(float(item.get("delta_ms") or 0.0)),
        reverse=True,
    )[:8]
    slot_map: dict[str, int] = {}
    for entry in evidence:
        slot = entry.get("slot")
        delta = entry.get("delta_ms")
        if isinstance(slot, str) and isinstance(delta, int | float):
            slot_map[slot] = slot_map.get(slot, 0) + 1
    slot_deltas = sorted((entry[1] for entry in slot_map.items()), reverse=True)
    median_delta_ms = deltas_sorted[len(deltas_sorted) // 2]
    span_ms = max(deltas_sorted) - min(deltas_sorted)
    return {
        "status": "available",
        "total_cues": len(evidence),
        "delta_count": len(deltas),
        "max_abs_delta_ms": round(max(abs_deltas), 3),
        "mean_abs_delta_ms": round(mean(abs_deltas), 3),
        "mean_delta_ms": round(mean(deltas), 3),
        "median_delta_ms": round(median_delta_ms, 3),
        "span_delta_ms": round(span_ms, 3),
        "coverage_ratio": round(len(deltas) / len(evidence), 3),
        "slot_count": len(slot_map),
        "slot_delta_top_counts": slot_deltas[:4],
        "largest_deltas": [
            {
                "cue_start": float(entry.get("cue_start", 0.0)),
                "nearest_onset": entry.get("nearest_onset"),
                "delta_ms": int(entry.get("delta_ms", 0)),
            }
            for entry in hottest
            if entry.get("delta_ms") is not None
        ],
    }


def infer_subtitle_drift_ms(
    evidence: list[dict[str, Any]],
    *,
    min_delta_count: int = ONSET_MIN_DELTA_COUNT,
    trim_ratio: float = 0.2,
    min_abs_ms: float = 22.0,
    max_abs_ms: float = 1500.0,
    max_span_ms: float = 600.0,
    max_outlier_ratio: float = 0.5,
) -> float | None:
    """Infer a global subtitle drift from onset evidence in milliseconds.

    Returns a median delta with edge trimming to ignore outliers. `None` means
    drift is not confidently inferable.
    """

    return _infer_drift_from_deltas(
        _collect_deltas(evidence),
        min_delta_count=min_delta_count,
        trim_ratio=trim_ratio,
        min_abs_ms=min_abs_ms,
        max_abs_ms=max_abs_ms,
        max_span_ms=max_span_ms,
        max_outlier_ratio=max_outlier_ratio,
    )


def infer_subtitle_drift_with_fallback(
    audio_path: Path,
    cues: list[Any],
    timeline: Any | None = None,
    *,
    window_seconds_candidates: tuple[float, ...] = ONSET_WINDOW_SECONDS_CANDIDATES,
    min_delta_count: int = ONSET_MIN_DELTA_COUNT,
    min_slot_delta_count: int = ONSET_MIN_SLOT_DELTA_COUNT,
    trim_ratio: float = 0.2,
    min_abs_ms: float = 22.0,
    max_abs_ms: float = 1500.0,
    max_span_ms: float = 600.0,
    max_outlier_ratio: float = 0.5,
    slotwise_span_threshold_ms: float = 30.0,
    slotwise_coverage_ratio_min: float = 0.35,
) -> tuple[float | dict[str, float] | None, list[dict[str, Any]], dict[str, object], float]:
    """Estimate drift and return the first high-enough confidence window result.

    The result tuple is ``(drift_ms or None, evidence, evidence_summary, used_window_seconds)``.
    """

    used_window_seconds = window_seconds_candidates[0] if window_seconds_candidates else 0.45
    best_summary: dict[str, object] = {
        "status": "insufficient",
        "total_cues": 0,
        "delta_count": 0,
        "coverage_ratio": 0.0,
    }
    best_evidence: list[dict[str, Any]] = []

    stable_ts_evidence, stable_ts_summary = _load_stable_ts_reference_evidence(audio_path, cues, timeline=timeline)
    if stable_ts_evidence:
        stable_ts_summary = summarize_onset_evidence(stable_ts_evidence) | stable_ts_summary | {
            "timing_method": TIMING_METHOD_STABLE_TS,
            "evidence_source": "stable-ts-track-json",
            "window_seconds": 0.0,
        }
        stable_slot_drift_ms, stable_slot_drift_counts = infer_slotwise_drift_ms_with_counts(
            stable_ts_evidence,
            min_delta_count=min_delta_count,
            min_slot_delta_count=min_slot_delta_count,
            trim_ratio=trim_ratio,
            min_abs_ms=min_abs_ms,
            max_abs_ms=max_abs_ms,
            max_span_ms=max_span_ms,
            max_outlier_ratio=max_outlier_ratio,
        )
        stable_summary = stable_ts_summary | {
            "slot_drift_count": len(stable_slot_drift_ms),
            "slot_drift_support_counts": dict(sorted(stable_slot_drift_counts.items())),
        }
        if stable_slot_drift_ms:
            stable_slot_values = sorted(stable_slot_drift_ms.values())
            stable_slot_span_ms = stable_slot_values[-1] - stable_slot_values[0]
            stable_drift_coverage_count = int(sum(stable_slot_drift_counts.values()))
            stable_drift_total_count = int(stable_summary.get("delta_count", 0))
            stable_slot_coverage_ratio = round(
                stable_drift_coverage_count / max(1, stable_drift_total_count),
                3,
            )
            stable_summary = stable_summary | {
                "slot_drift_span_ms": round(stable_slot_span_ms, 3),
                "slot_drift_coverage_ratio": stable_slot_coverage_ratio,
            }
            if (
                len(stable_slot_values) >= 2
                and stable_slot_span_ms >= slotwise_span_threshold_ms
                and stable_slot_coverage_ratio >= slotwise_coverage_ratio_min
            ):
                return (
                    stable_slot_drift_ms,
                    stable_ts_evidence,
                    stable_summary
                    | {
                        "status": "ok",
                        "drift_mode": "slotwise",
                        "slot_drift_values_ms": dict(sorted(stable_slot_drift_ms.items())),
                        "slot_drift_fallback_ms": stable_slot_values[len(stable_slot_values) // 2],
                    },
                    0.0,
                )

        stable_drift_ms = infer_subtitle_drift_ms(
            stable_ts_evidence,
            min_delta_count=min_delta_count,
            trim_ratio=trim_ratio,
            min_abs_ms=min_abs_ms,
            max_abs_ms=max_abs_ms,
            max_span_ms=max_span_ms,
            max_outlier_ratio=max_outlier_ratio,
        )
        if stable_drift_ms is not None:
            return (
                stable_drift_ms,
                stable_ts_evidence,
                stable_summary
                | {
                    "status": "ok",
                    "drift_mode": "global",
                    "slot_drift_span_ms": round(
                        (max(stable_slot_drift_ms.values()) - min(stable_slot_drift_ms.values())) if len(stable_slot_drift_ms) > 1 else 0.0,
                        3,
                    ),
                },
                0.0,
            )

        if int(stable_summary.get("delta_count", 0)) >= min_delta_count:
            stable_summary = stable_summary | {
                "status": "low_confidence",
                "status_reason": "stable_ts_data_found_but_drift_not_confident",
            }
        best_summary = stable_summary
        best_evidence = stable_ts_evidence

    for window_seconds in window_seconds_candidates:
        used_window_seconds = window_seconds
        evidence = estimate_subtitle_onset_evidence(audio_path, cues, window_seconds=window_seconds)
        summary = summarize_onset_evidence(evidence) | {"window_seconds": round(window_seconds, 3)}
        if evidence and summary["delta_count"] >= best_summary.get("delta_count", 0):
            best_summary = summary
            best_evidence = evidence
        slot_drift_ms, slot_drift_counts = infer_slotwise_drift_ms_with_counts(
            evidence,
            min_delta_count=min_delta_count,
            min_slot_delta_count=min_slot_delta_count,
            trim_ratio=trim_ratio,
            min_abs_ms=min_abs_ms,
            max_abs_ms=max_abs_ms,
            max_span_ms=max_span_ms,
            max_outlier_ratio=max_outlier_ratio,
        )
        summary = summary | {
            "slot_drift_count": len(slot_drift_ms),
            "slot_drift_support_counts": dict(sorted(slot_drift_counts.items())),
        }
        if int(summary["delta_count"]) >= min_delta_count and slot_drift_ms:
            slot_values = sorted(slot_drift_ms.values())
            slot_span_ms = slot_values[-1] - slot_values[0]
            slot_drift_covered_count = int(sum(slot_drift_counts.values()))
            slot_drift_coverage_ratio = round(slot_drift_covered_count / max(1, int(summary["delta_count"])), 3)
            summary = summary | {
                "slot_drift_coverage_ratio": slot_drift_coverage_ratio,
                "slot_drift_span_ms": round(slot_span_ms, 3),
            }
            if (
                len(slot_values) >= 2
                and slot_span_ms >= slotwise_span_threshold_ms
                and slot_drift_coverage_ratio >= slotwise_coverage_ratio_min
            ):
                summary = summary | {
                    "status": "ok",
                    "drift_mode": "slotwise",
                    "slot_drift_values_ms": dict(sorted(slot_drift_ms.items())),
                    "slot_drift_fallback_ms": slot_values[len(slot_values) // 2],
                }
                return slot_drift_ms, evidence, summary, float(window_seconds)

        drift_ms = infer_subtitle_drift_ms(
            evidence,
            min_delta_count=min_delta_count,
            trim_ratio=trim_ratio,
            min_abs_ms=min_abs_ms,
            max_abs_ms=max_abs_ms,
            max_span_ms=max_span_ms,
            max_outlier_ratio=max_outlier_ratio,
        )
        if drift_ms is not None:
            summary = summary | {
                "status": "ok",
                "drift_mode": "global",
                "slot_drift_span_ms": round(
                    (max(slot_drift_ms.values()) - min(slot_drift_ms.values())) if len(slot_drift_ms) > 1 else 0.0,
                    3,
                ),
            }
            return drift_ms, evidence, summary, float(window_seconds)

        if int(summary["delta_count"]) >= min_delta_count:
            summary = summary | {
                "status": "low_confidence",
                "status_reason": "evidence_inconsistent_after_trim",
                "drift_mode": "none",
            }

    best_summary = best_summary | {"status": best_summary.get("status", "insufficient")}
    if best_summary.get("status") in {"available", "ok"}:
        best_summary = best_summary | {
            "status": "low_confidence" if int(best_summary.get("delta_count", 0)) >= min_delta_count else "insufficient",
            "status_reason": "drift_not_confident_enough_after_all_windows",
        }
    return None, best_evidence, best_summary, float(used_window_seconds)
