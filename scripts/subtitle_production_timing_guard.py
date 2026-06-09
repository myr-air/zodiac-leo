#!/usr/bin/env python3
"""Helpers to keep subtitle source lane choices consistent across episode renders.

The production lane is final `.en.srt/.en.vtt`.
Preview lanes can use draft and fallback draft timing only when explicitly enabled.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


SubtitleLane = "final" | "draft" | "generated_fallback"


@dataclass(frozen=True)
class SubtitleSourceSelection:
    lane: SubtitleLane
    source_srt: Path
    source_vtt: Path
    timing_method: str
    requires_final: bool
    notes: str


def _missing_final_message(episode_id: str, *, suffix: str = "") -> str:
    base = (
        f"Final subtitle sidecars missing for {episode_id}: expected channel/episodes/<episode-id>/subtitles/<episode-id>.en.srt and <episode-id>.en.vtt. "
        "Run subtitle_alignment_pipeline promote flow before local production render."
    )
    if suffix:
        return f"{base} {suffix}"
    return base


def require_final_subtitles(promoted_srt: Path, promoted_vtt: Path, episode_id: str | None = None) -> None:
    if not promoted_srt.exists():
        raise FileNotFoundError(_missing_final_message(episode_id or promoted_srt.stem, suffix="Use --allow-draft-subtitles for manual preview only."))
    if not promoted_vtt.exists():
        raise FileNotFoundError(
            _missing_final_message(
                episode_id or promoted_srt.stem,
                suffix="Final VTT is required for preview-grade and production-grade subtitle burning.",
            )
        )


def pick_subtitle_source(
    episode_id: str,
    promoted_srt: Path,
    promoted_vtt: Path,
    draft_srt: Path,
    draft_vtt: Path,
    generated_srt: Path,
    generated_vtt: Path,
    *,
    allow_draft_subtitles: bool,
    final_timing_method: str = "track-aligned_episode_source_srt",
    draft_timing_method: str = "track-aligned_episode_source_draft_srt",
    generated_timing_method: str = "mechanical_even_distribution_from_source_lyrics_needs_human_watch",
) -> SubtitleSourceSelection:
    """Return selected subtitle lane for this render.

    Production mode (allow_draft_subtitles=False) must always use final sidecars.
    Preview mode may consume draft sidecars if present; if draft sidecars are absent,
    preview falls back to generated draft timing for this local evidence lane.
    """
    promoted_ok = promoted_srt.exists() and promoted_vtt.exists()
    draft_ok = draft_srt.exists() and draft_vtt.exists()

    if not allow_draft_subtitles:
        require_final_subtitles(promoted_srt, promoted_vtt, episode_id)
        return SubtitleSourceSelection(
            lane="final",
            source_srt=promoted_srt,
            source_vtt=promoted_vtt,
            timing_method=final_timing_method,
            requires_final=True,
            notes="Production subtitle lane: final sidecars loaded."
        )

    if promoted_ok:
        return SubtitleSourceSelection(
            lane="final",
            source_srt=promoted_srt,
            source_vtt=promoted_vtt,
            timing_method=final_timing_method,
            requires_final=True,
            notes="Production subtitle lane forced on by explicit final availability even in preview mode.",
        )

    if draft_ok:
        return SubtitleSourceSelection(
            lane="draft",
            source_srt=draft_srt,
            source_vtt=draft_vtt,
            timing_method=draft_timing_method,
            requires_final=False,
            notes="Manual preview lane: draft sidecars found and used with explicit preview flag.",
        )

    return SubtitleSourceSelection(
        lane="generated_fallback",
        source_srt=generated_srt,
        source_vtt=generated_vtt,
        timing_method=generated_timing_method,
        requires_final=False,
        notes="Manual preview lane: draft/final sidecars absent; generated timing fallback is used.",
    )


def summarize_subtitle_source(selection: SubtitleSourceSelection) -> dict[str, Any]:
    return {
        "lane": selection.lane,
        "source_srt": str(selection.source_srt),
        "source_vtt": str(selection.source_vtt),
        "timing_method": selection.timing_method,
        "requires_final": selection.requires_final,
        "notes": selection.notes,
    }


def estimate_onset_alignment(audio_path: Path, cues: list[Any], *, window_seconds: float = 0.50) -> dict[str, Any]:
    """Optional onset evidence from subtitle_alignment_pipeline.

    The result is advisory only and is intentionally low-severity by design.
    """
    if not cues:
        return {"status": "no_cues", "count": 0}

    try:
        from subtitle_alignment_pipeline import estimate_onset_deltas
    except Exception as exc:  # pragma: no cover - optional dependency path
        return {"status": "unavailable", "reason": str(exc)}

    evidence = estimate_onset_deltas(audio_path, cues, window_seconds=window_seconds)
    if evidence and isinstance(evidence, list) and evidence[0].get("status") == "unavailable":
        return {"status": "unavailable", "reason": evidence[0].get("reason", "librosa unavailable")}

    deltas_ms: list[int] = [
        int(item["delta_ms"]) for item in evidence if isinstance(item, dict) and isinstance(item.get("delta_ms"), (int, float))
    ]
    if not deltas_ms:
        return {
            "status": "available_no_matches",
            "count": len(evidence),
            "window_seconds": window_seconds,
            "max_abs_delta_ms": None,
            "outlier_count": 0,
            "outlier_threshold_ms": 300,
            "samples": [],
        }
    abs_deltas = [abs(value) for value in deltas_ms]
    threshold = 300
    outliers = [value for value in deltas_ms if abs(value) > threshold]
    return {
        "status": "ok",
        "count": len(evidence),
        "count_with_onset": len(deltas_ms),
        "coverage_ratio": round(len(deltas_ms) / len(evidence), 3),
        "window_seconds": window_seconds,
        "max_abs_delta_ms": max(abs_deltas),
        "outlier_count": len(outliers),
        "outlier_threshold_ms": threshold,
        "samples": evidence[:20],
    }
