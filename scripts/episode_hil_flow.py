#!/usr/bin/env python3
"""Core HIL flow checker for reusable episode pipelines.

This script centralizes the HIL-1..HIL-4 gate contract in one place so each new
episode can use the same shared checkpoints and operations model without adding
new per-episode orchestration code.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from collections import Counter, deque
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EPISODE_ROOT = PROJECT_ROOT / "channel" / "episodes"
CANDIDATE_ROOT = PROJECT_ROOT / "candidates"


@dataclass(frozen=True)
class EvidenceSpec:
    name: str
    base: str  # "episode" or "candidate"
    patterns: tuple[str, ...]
    operator: str = "all"  # "all" or "any"
    required: bool = True
    min_count: int = 1


@dataclass(frozen=True)
class HilStage:
    key: str
    title: str
    scope: str
    can_work_without_previous: bool = False
    custom_checks: tuple[str, ...] = ()
    checks: tuple[EvidenceSpec, ...] = ()
    allowed_ops: tuple[str, ...] = ()
    blocked_ops: tuple[str, ...] = ()


STAGES = {
    "hil-1": HilStage(
        key="hil-1",
        title="Prompt packet",
        scope="Draft and lock source prompts/metadata, not touching providers/media/release.",
        custom_checks=("source-content-gate",),
        checks=(
            EvidenceSpec("manifest", "episode", ("manifest.json",), "all", True, 1),
            EvidenceSpec(
                "source prompt docs",
                "episode",
                (
                    "source/songs.md",
                    "source/suno-manual-fields.md",
                    "source/prompt-pack.md",
                    "source/visual.md",
                    "source/metadata.md",
                ),
                "all",
                True,
                1,
            ),
        ),
        allowed_ops=(
            "Edit source documents.",
            "Update episode-style source reviews.",
            "Update tracking rows for source-only evidence.",
        ),
        blocked_ops=(
            "Provider/audio or provider/browser automation.",
            "Candidate ID or provenance claims before real local files.",
            "Render/export, upload, scheduling, or account mutation.",
            "Platform/release/risk-claim language not evidenced.",
        ),
    ),
    "hil-2": HilStage(
        key="hil-2",
        title="Preview + issue-led review",
        scope="Intake real local media, identify risky segments, review + patch before any upload gate.",
        custom_checks=("media-intake-gate",),
        checks=(
            EvidenceSpec(
                "suno source tracks",
                "episode",
                ("source/suno-tracks/*.md",),
                "all",
                True,
                1,
            ),
            EvidenceSpec(
                "selected audio candidates",
                "candidate",
                ("audio/selected/*.wav",),
                "any",
                True,
                1,
            ),
            EvidenceSpec(
                "selected visual candidates",
                "candidate",
                ("visual/selected/*",),
                "any",
                True,
                1,
            ),
            EvidenceSpec(
                "candidate-intake review notes",
                "episode",
                (
                    "reviews/audio-candidate-intake.md",
                    "reviews/visual-candidate-intake.md",
                    "reviews/candidate-intake-checklist.md",
                ),
                "all",
                True,
                1,
            ),
            EvidenceSpec(
                "preview / risk evidence",
                "episode",
                ("reviews/*proof*.md", "reviews/*review*.md"),
                "any",
                True,
                1,
            ),
        ),
        allowed_ops=(
            "Open local real files into candidate layout.",
            "Create segment-wise preview notes for risky points.",
            "Patch local candidates where issues are identified.",
            "Update manifest status and current-state review when scope changes.",
        ),
        blocked_ops=(
            "Render/export without explicit local-risk review.",
            "Any API/browser action, upload, or publish.",
            "Public release claims before final-video gate.",
        ),
    ),
    "hil-3": HilStage(
        key="hil-3",
        title="Full render + thumbnail + comment prep",
        scope="Create final-video candidate, select thumbnail, draft pin-comment text.",
        custom_checks=("subtitle-alignment-gate",),
        checks=(
            EvidenceSpec(
                "authoritative English subtitles",
                "episode",
                ("subtitles/*.en.srt", "subtitles/*.en.vtt"),
                "any",
                True,
                1,
            ),
            EvidenceSpec(
                "authoritative Thai subtitles",
                "episode",
                ("subtitles/*.th.srt", "subtitles/*.th.vtt"),
                "any",
                True,
                1,
            ),
            EvidenceSpec(
                "final render candidate",
                "candidate",
                ("render/**/*.mp4",),
                "all",
                True,
                1,
            ),
            EvidenceSpec(
                "final render review notes",
                "episode",
                (
                    "reviews/render-export-qa.md",
                    "reviews/render-export-plan.md",
                    "reviews/render-export-package.md",
                ),
                "any",
                True,
                1,
            ),
            EvidenceSpec(
                "thumbnail asset and plan",
                "candidate",
                ("thumbnail/*",),
                "any",
                True,
                1,
            ),
            EvidenceSpec(
                "comment draft",
                "episode",
                ("source/comment.txt",),
                "all",
                True,
                1,
            ),
        ),
        allowed_ops=(
            "Finalize local render candidate.",
            "Prepare thumbnail artifact candidate list for later API/manual handoff.",
            "Refine top-level comment draft for post-upload pin/engagement flow.",
        ),
        blocked_ops=(
            "Any release API execute action.",
            "Publish/private visibility mutation.",
            "Caption uploads, schedule, or playlist edits.",
        ),
    ),
    "hil-4": HilStage(
        key="hil-4",
        title="Upload + schedule",
        scope="Run approved upload and post-upload operations, then schedule publish.",
        checks=(
            EvidenceSpec(
                "video upload package",
                "episode",
                ("source/youtube-api-video-upload-package.md", "source/youtube-video-resource.json"),
                "all",
                True,
                1,
            ),
            EvidenceSpec(
                "thumbnail upload package",
                "episode",
                ("source/youtube-api-thumbnail-upload-package.md",),
                "all",
                True,
                1,
            ),
            EvidenceSpec(
                "release evidence row",
                "episode",
                (
                    "reviews/youtube-api-execution-gate.md",
                    "reviews/render-export-qa.md",
                    "reviews/release-decision-plan.md",
                ),
                "any",
                False,
                1,
            ),
            EvidenceSpec(
                "tracking rows",
                "episode",
                ("tracking/status.csv", "tracking/assets.csv", "tracking/provenance.csv", "tracking/decisions.csv"),
                "all",
                True,
                1,
            ),
        ),
        allowed_ops=(
            "YouTube upload API/manual handoff execution.",
            "thumbnail upload command.",
            "top-level comment insertion command (manual pin as required).",
            "release scheduling and visibility change through approved account action.",
        ),
        blocked_ops=(
            "Any account action not explicitly approved in release gate.",
            "Comment pin through unsupported API path.",
            "Unbounded credentials or sensitive auth state inside repo.",
        ),
    ),
}


_FIELD_LABEL_RE = re.compile(r"^\s*\*{0,2}([A-Za-z][A-Za-z ]+[A-Za-z])\s*\*{0,2}\s*:\s*(.*)")
_SECTION_HEADER_RE = re.compile(r"^\s*\[([^\]]+)\]\s*$")
_TRACK_INDEX_RE = re.compile(r"(?:^|[^a-zA-Z0-9])t(\d{1,2})(?:$|[^a-zA-Z0-9])", re.IGNORECASE)
_TRACK_VARIANT_RE = re.compile(r"(?:^|[^a-zA-Z0-9])c(0[12])(?:$|[^a-zA-Z0-9])", re.IGNORECASE)
_FIELD_ALIASES = {
    "song title": "song_title",
    "lyrics mode": "lyrics_mode",
    "lyrics": "lyrics",
    "styles": "styles",
    "exclude styles": "exclude_styles",
    "vocal gender": "vocal_gender",
    "weirdness": "weirdness",
    "style influence": "style_influence",
    "reject criteria": "reject_criteria",
}
_WORD_RE = re.compile(r"[a-z']+")
_STOP_WORDS = {
    "a",
    "an",
    "and",
    "the",
    "to",
    "of",
    "in",
    "on",
    "at",
    "for",
    "with",
    "from",
    "is",
    "are",
    "was",
    "were",
    "be",
    "been",
    "am",
    "as",
    "it",
    "its",
    "i",
    "you",
    "we",
    "he",
    "she",
    "they",
    "my",
    "your",
    "me",
    "we",
    "us",
    "that",
    "this",
    "these",
    "those",
    "there",
    "here",
    "but",
    "or",
    "if",
    "so",
    "not",
    "by",
    "up",
    "out",
    "just",
    "can",
    "will",
    "more",
    "then",
    "than",
    "about",
}
_WATCHLIST_WORDS = {
    "soft",
    "quiet",
    "small",
    "little",
    "gentle",
    "warm",
    "slow",
    "line",
    "sign",
    "page",
    "name",
    "same",
    "tomorrow",
    "smile",
    "light",
    "street",
    "door",
    "glass",
    "hand",
    "walk",
    "wait",
    "close",
    "after",
    "school",
    "dream",
    "vibe",
    "cosmic",
    "destiny",
    "glow",
    "blue",
    "calm",
    "plain",
    "dark",
    "day",
    "night",
    "window",
}
_REQUIRED_TRACK_FIELDS = (
    "song_title",
    "lyrics_mode",
    "lyrics",
    "styles",
    "exclude_styles",
    "vocal_gender",
    "weirdness",
    "style_influence",
    "reject_criteria",
)
_STANDARD_SONG_SECTION_KEYWORDS = (
    "intro",
    "verse",
    "pre chorus",
    "pre-chorus",
    "chorus",
    "hook",
    "refrain",
    "bridge",
    "outro",
)
_LYRICS_CONTEXT_KEYWORDS = (
    "song context",
    "performance notes",
    "vocal direction",
    "arrangement map",
    "duration target",
    "suno direction",
    "song structure",
    "instrumentation",
    "vocal style",
)
_STYLE_CONTROL_GROUPS = {
    "tempo": (r"\b(?:approx\.?\s*)?\d{2,3}\s*bpm\b",),
    "vocal": (r"\bvocal\b", r"\bfemale\b", r"\bmale\b", r"\balto\b", r"\btenor\b", r"\bmezzo\b"),
    "instrumentation": (r"\bkeys?\b", r"\bguitar\b", r"\bbass\b", r"\bdrums?\b", r"\bpads?\b", r"\bpiano\b", r"\bsynth\b"),
    "arrangement_arc": (r"\bintro\b", r"\bverse\b", r"\bchorus\b", r"\bhook\b", r"\bbridge\b", r"\boutro\b", r"\blift\b", r"\bbuild\b"),
    "mix_or_timbre": (r"\bmix\b", r"\bclose[- ]mic", r"\bdry vocal\b", r"\breverb\b", r"\broom\b", r"\btape\b", r"\bwide\b", r"\btimbre\b"),
    "duration_target": (r"\b3[: ]?0\d\b", r"\b3[- ]?minute\b", r"\bthree[- ]minute\b", r"\bfull[- ]length\b", r"\bat least 3\b"),
}
_EXCLUDE_CONTROL_GROUPS = {
    "lyric_drift": (r"\bauto[- ]generated lyrics\b", r"\binvented lyrics\b", r"\blyric rewrite\b", r"\bchanged lyrics\b"),
    "underlength": (r"\bunder 3\b", r"\bshort sketch\b", r"\babrupt ending\b", r"\bcut[- ]off\b"),
    "vocal_drift": (r"\brandom vocalist\b", r"\bchildlike vocal\b", r"\bnovelty vocal\b", r"\bvocal imitation\b"),
}


def _normalise_text(value: str) -> str:
    return re.sub(r"[^a-z0-9 ]", " ", value.lower())


def _tokenise(value: str) -> list[str]:
    return [token for token in _WORD_RE.findall(_normalise_text(value)) if token and token not in _STOP_WORDS]


def _normalise_title(value: str) -> str:
    return _normalise_text(value).strip().replace("  ", " ")


def _parse_suno_track_file(path: Path) -> dict[str, str]:
    raw = path.read_text(encoding="utf-8")
    lines = raw.splitlines()
    fields: dict[str, str] = {}
    current_field: str | None = None
    buffer: list[str] = []

    def flush_lyrics() -> None:
        nonlocal fields, current_field, buffer
        if current_field != "lyrics":
            return
        content = "\n".join(buffer).strip()
        content = re.sub(r"(?ms)^```(?:text)?\s*$\n?|^```\s*$\n?", "", content).strip()
        fields["lyrics"] = content
        current_field = None
        buffer = []

    for line in lines:
        match = _FIELD_LABEL_RE.match(line)
        if match:
            key_raw = match.group(1).strip().lower()
            value = match.group(2).strip()
            canonical = _FIELD_ALIASES.get(key_raw)
            if not canonical:
                if current_field == "lyrics":
                    buffer.append(line)
                continue
            if current_field == "lyrics":
                flush_lyrics()
            if canonical == "lyrics":
                current_field = canonical
                buffer = []
                if value:
                    buffer.append(value)
            else:
                fields[canonical] = value
                current_field = None
            continue
        if current_field == "lyrics":
            buffer.append(line)

    if current_field == "lyrics":
        flush_lyrics()

    return fields


def _extract_sections(lyrics: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {"unknown": []}
    current = "unknown"
    header_counts: dict[str, int] = {}
    for line in lyrics.splitlines():
        section_match = _SECTION_HEADER_RE.match(line.strip())
        if section_match:
            raw_title = _normalise_title(section_match.group(1))
            header_counts[raw_title] = header_counts.get(raw_title, 0) + 1
            if header_counts[raw_title] > 1:
                current = f"{raw_title}_{header_counts[raw_title]}"
            else:
                current = raw_title
            sections.setdefault(current, [])
            continue
        sections.setdefault(current, [])
        sections[current].append(line.strip())
    return sections


def _first_named_section(sections: dict[str, list[str]]) -> str:
    for section_name in sections:
        if section_name != "unknown":
            return section_name
    return ""


def _has_any_pattern(value: str, patterns: tuple[str, ...]) -> bool:
    return any(re.search(pattern, value, re.IGNORECASE) for pattern in patterns)


def _detect_prompt_control_issues(path: Path, lyrics: str, styles: str, exclude_styles: str) -> list[str]:
    issues: list[str] = []
    sections = _extract_sections(lyrics)
    named_sections = [section for section in sections if section != "unknown"]
    first_section = _first_named_section(sections)

    context_sections = [
        section
        for section in named_sections
        if any(keyword in section for keyword in _LYRICS_CONTEXT_KEYWORDS)
    ]
    if not context_sections:
        issues.append(f"{path.name} Lyrics missing pre-song context/control section for Suno custom mode.")
    elif first_section in context_sections and len(named_sections) > 1:
        context_words = 0
        for section in context_sections:
            context_words += len(_tokenise(" ".join(sections.get(section, []))))
            # Count words in the section name itself (headers like "Song Structure: ...")
            context_words += len(_tokenise(section))
        if context_words < 18:
            issues.append(f"{path.name} Lyrics context/control section is too thin for Suno steering.")

    first_standard_index = next(
        (
            index
            for index, section in enumerate(named_sections)
            if any(section.startswith(keyword) for keyword in _STANDARD_SONG_SECTION_KEYWORDS)
        ),
        None,
    )
    if first_standard_index == 0:
        issues.append(f"{path.name} Lyrics start directly with song section; add context before the first sung section.")

    # Ensure there is at least one bracketed section/line for an instrumental break or solo
    # (e.g. [Instrumental Break], [Solo - Rhodes], [Cello solo]) to hit 3+ minutes
    has_instrumental_or_solo = False
    for line in lyrics.splitlines():
        line_stripped = line.strip()
        if line_stripped.startswith("[") and line_stripped.endswith("]"):
            content = line_stripped[1:-1].lower()
            if any(word in content for word in ("instrumental", "solo", "break")):
                has_instrumental_or_solo = True
                break
    if not has_instrumental_or_solo:
        issues.append(
            f"{path.name} Lyrics missing explicit bracketed instrumental break/solo section "
            "(e.g., [Instrumental Break] or [Solo]) to ensure song duration reaches 3+ minutes."
        )

    styles_lower = styles.lower()
    missing_style_groups = [
        group
        for group, patterns in _STYLE_CONTROL_GROUPS.items()
        if not _has_any_pattern(styles_lower, patterns)
    ]
    if missing_style_groups:
        issues.append(f"{path.name} Styles missing control groups: {', '.join(missing_style_groups)}.")

    comma_parts = [part.strip() for part in styles.split(",") if part.strip()]
    if len(comma_parts) < 9:
        issues.append(f"{path.name} Styles too short/vague; expected richer comma-separated control values.")

    exclude_lower = exclude_styles.lower()
    missing_exclude_groups = [
        group
        for group, patterns in _EXCLUDE_CONTROL_GROUPS.items()
        if not _has_any_pattern(exclude_lower, patterns)
    ]
    if missing_exclude_groups:
        issues.append(f"{path.name} Exclude Styles missing drift guards: {', '.join(missing_exclude_groups)}.")

    return issues


def _max_repeat_run(lines: list[str]) -> int:
    if not lines:
        return 0
    max_run = 1
    run = 1
    prev = ""
    for line in lines:
        norm = " ".join(_tokenise(line))
        if not norm:
            continue
        if norm == prev:
            run += 1
            max_run = max(max_run, run)
        else:
            run = 1
            prev = norm
    return max_run


def _extract_episode_number(episode_id: str) -> tuple[int, int] | None:
    match = re.match(r"^s(\d+)e(\d+)", episode_id)
    if not match:
        return None
    return int(match.group(1)), int(match.group(2))


def _collect_previous_episode_tracks(episode_id: str) -> list[str]:
    current = _extract_episode_number(episode_id)
    if not current:
        return []

    previous_titles: list[str] = []
    for child in sorted(EPISODE_ROOT.iterdir()):
        if not child.is_dir():
            continue
        numbers = _extract_episode_number(child.name)
        if not numbers or numbers >= current:
            continue
        track_dir = child / "source" / "suno-tracks"
        for path in sorted(track_dir.glob("*.md")):
            try:
                parsed = _parse_suno_track_file(path)
                title = str(parsed.get("song_title", "")).strip()
                if title:
                    previous_titles.append(_normalise_title(title))
            except OSError:
                continue
    return previous_titles


def _line_contains_phrase(line: str, phrase: str) -> bool:
    if not phrase:
        return False
    return _normalise_title(line).find(_normalise_title(phrase)) >= 0


def _section_has_title_repeat(section_lines: list[str], title: str) -> bool:
    if not title:
        return False
    title_norm = _normalise_title(title)
    if not title_norm:
        return False
    count = sum(1 for line in section_lines if _line_contains_phrase(line, title_norm))
    return count >= 2


def _detect_anti_patterns(track: dict[str, Any], track_index: int, episode_id: str) -> list[str]:
    issues: list[str] = []
    del episode_id
    title = str(track.get("song_title", "")).strip()
    sections = track.get("sections", {})
    lyrics = str(track.get("lyrics", ""))

    for section_name, section_lines in sections.items():
        if ("chorus" in section_name or "refrain" in section_name) and _section_has_title_repeat(section_lines, title):
            issues.append(f"Track {track_index} repeats title phrase in {section_name}.")

    if track_index > 1 and title:
        for section_name in sections:
            if "chorus" in section_name:
                for line in sections[section_name]:
                    if line and _line_contains_phrase(line, title):
                        issues.append(f"Track {track_index} uses title in chorus lead-in.")
                break

    for line in lyrics.splitlines():
        if re.search(r"\bNo\b.*,\s*\bno\b", line, re.IGNORECASE):
            issues.append(f"Track {track_index} uses negative-construction pair (`No..., no...`).")
            break
        if re.match(r"^\s*Maybe\b", line, re.IGNORECASE):
            issues.append(f"Track {track_index} starts lyric line with `Maybe...`.")
            break
        if re.match(r"^\s*Nothing\b", line, re.IGNORECASE):
            issues.append(f"Track {track_index} starts lyric line with `Nothing...`.")
            break
        if re.search(r"\bone\s+(soft|small|note|sign|line)\b", line, re.IGNORECASE):
            issues.append(f"Track {track_index} uses `one small/soft note/sign/line` payoff pattern.")
            break

    for section_name, section_lines in sections.items():
        if section_name.startswith("final refrain") or section_name.startswith("outro"):
            if _max_repeat_run(section_lines) >= 4:
                issues.append(f"Track {track_index} has aggressive final repeat stacking in {section_name}.")

    return sorted(set(issues))


def _build_hil1_track_analyses(episode_root: Path, episode_id: str) -> tuple[list[dict[str, Any]], list[str]]:
    track_dir = episode_root / "source" / "suno-tracks"
    track_paths = sorted(track_dir.glob("*.md"))
    if not track_paths:
        return [], ["No source/suno-tracks/*.md found."]

    analyses: list[dict[str, Any]] = []
    issues: list[str] = []
    previous_titles: list[str] = []
    previous_signatures: deque[tuple[str, ...]] = deque(maxlen=4)
    previous_word_windows: deque[Counter[str]] = deque(maxlen=3)
    prior_titles = _collect_previous_episode_tracks(episode_id)

    for track_index, path in enumerate(track_paths, start=1):
        parsed = _parse_suno_track_file(path)
        lyrics = str(parsed.get("lyrics", "")).strip()
        styles = str(parsed.get("styles", ""))
        title = str(parsed.get("song_title", "")).strip()
        missing_fields = [field for field in _REQUIRED_TRACK_FIELDS if not parsed.get(field)]
        if missing_fields:
            issues.append(f"{path.name} missing: {', '.join(sorted(missing_fields))}.")

        if not re.search(r"(?i)\b(?:approx\.?\s*)?\d{2,3}\s*bpm\b", styles):
            issues.append(f"{path.name} Styles missing approximate BPM.")

        episode_num = _extract_episode_number(episode_id)
        min_lyric_lines = 18
        if episode_num:
            season, ep = episode_num
            if season > 1 or (season == 1 and ep >= 5):
                min_lyric_lines = 24

        non_section_lines = len([line for line in lyrics.splitlines() if line.strip() and not line.strip().startswith("[")])
        if non_section_lines < min_lyric_lines:
            issues.append(
                f"{path.name} lyrics look short for a full track source "
                f"(found {non_section_lines} lines, expected at least {min_lyric_lines})."
            )

        exclude_styles = str(parsed.get("exclude_styles", ""))
        issues.extend(_detect_prompt_control_issues(path, lyrics, styles, exclude_styles))

        sections = _extract_sections(lyrics)
        section_signature = tuple(section for section in sections.keys() if section != "unknown")
        if track_index > 1 and section_signature == previous_signatures[-1]:
            issues.append(f"{path.name} has structure signature same as previous track.")
        if len(previous_signatures) >= 3:
            last_three = list(previous_signatures)[-3:]
            if all(sig == section_signature for sig in last_three):
                issues.append(f"{path.name} repeats the same section signature for 4 tracks in a row.")

        if title:
            title_norm = _normalise_title(title)
            for prior_title in prior_titles:
                if not prior_title:
                    continue
                ratio = 1.0 if prior_title == title_norm else SequenceMatcher(None, title_norm, prior_title).ratio()
                if ratio >= 0.9:
                    issues.append(f"{path.name} title is too close to earlier episode title set.")
                    break
            for prev in previous_titles:
                if not prev:
                    continue
                if SequenceMatcher(None, title_norm, prev).ratio() >= 0.85:
                    issues.append(f"{path.name} title is too close to previous track title in current episode.")
                    break
            previous_titles.append(title_norm)

        sung_lyrics = "\n".join(
            line
            for line in lyrics.splitlines()
            if not (line.strip().startswith("[") and line.strip().endswith("]"))
        )
        tokens = Counter(_tokenise(sung_lyrics))
        if tokens:
            recent_window = Counter()
            for prior in previous_word_windows:
                recent_window.update(prior)
            overlap = []
            for key, count in tokens.items():
                if key in _WATCHLIST_WORDS and count >= 2 and recent_window.get(key, 0) >= 2:
                    overlap.append(key)
            if overlap:
                issues.append(f"{path.name} reuses watchlist words across adjacent tracks: {', '.join(sorted(set(overlap)))}.")

        analyses.append(
            {
                "path": path.name,
                "song_title": title,
                "lyrics": lyrics,
                "sections": sections,
                "signature": section_signature,
            }
        )
        previous_word_windows.append(tokens)
        previous_signatures.append(section_signature)
        issues.extend(_detect_anti_patterns(analyses[-1], track_index, episode_id))

    if len(track_paths) != 13:
        issues.append(f"Suno track count is {len(track_paths)}; expected 13.")

    return analyses, sorted(set(issues))


def _make_quality_check(name: str, passed: bool, expected: tuple[str, ...], found: int, samples: list[str], required: bool = True) -> dict[str, Any]:
    return {
        "name": name,
        "required": required,
        "operator": "custom",
        "expected": expected,
        "found": found,
        "min_count": 0,
        "passed": bool(passed),
        "samples": samples[:8],
    }


def _run_hil1_core_package_checks(episode_root: Path) -> list[str]:
    issues: list[str] = []

    # 1. Check metadata.md
    metadata_path = episode_root / "source" / "metadata.md"
    if metadata_path.exists():
        metadata_text = metadata_path.read_text(encoding="utf-8")

        # Check Title format: 『 Title 』| Subtitle
        title_matches = re.findall(r"『[^』]+』\s*\|\s*[^\n]+", metadata_text)
        if not title_matches:
            issues.append("metadata.md: Missing or incorrectly formatted listener-facing title. Title must follow '『 Title 』| Subtitle' format.")

        # Check AI Disclosure
        if "disclosure" not in metadata_text.lower() or not any(word in metadata_text.lower() for word in ("ai-assisted", "ai assistance", "synthesized", "generation")):
            issues.append("metadata.md: Missing AI-assisted workflow disclosure statement in description.")

        # Check forbidden platform claims in the description block itself
        description_match = re.search(
            r"### Description draft\s*\n+```[a-z]*\n(.*?)\n```",
            metadata_text,
            re.DOTALL | re.IGNORECASE
        )
        if description_match:
            description_draft = description_match.group(1).lower()
            for claim in ("copyright-free", "royalty-free", "monetization-safe", "content id-safe", "upload-ready", "publish-ready"):
                if claim in description_draft:
                    issues.append(f"metadata.md: Forbidden platform safety claim found in description: '{claim}'.")
        else:
            for claim in ("copyright-free", "royalty-free", "monetization-safe", "content id-safe", "upload-ready", "publish-ready"):
                if f"claim {claim}" in metadata_text.lower() or f"is {claim}" in metadata_text.lower():
                    issues.append(f"metadata.md: Forbidden platform safety claim found: '{claim}'.")
    else:
        issues.append("metadata.md: File is missing.")

    # 2. Check visual.md
    visual_path = episode_root / "source" / "visual.md"
    if visual_path.exists():
        visual_text = visual_path.read_text(encoding="utf-8")

        # Check art direction keywords (watercolor, semi-realistic, anime, 16:9, lifelike)
        missing_art_keys = []
        for key in ("watercolor", "semi-realistic", "anime", "16:9", "lifelike"):
            if key not in visual_text.lower():
                missing_art_keys.append(key)
        if missing_art_keys:
            issues.append(f"visual.md: Missing signature art direction keywords: {', '.join(missing_art_keys)}.")

        # Check safe-zone mapping guidelines
        if "safe-zone" not in visual_text.lower() and "safe zone" not in visual_text.lower():
            issues.append("visual.md: Missing Safe-Zone mapping instructions for overlays.")
    else:
        issues.append("visual.md: File is missing.")

    # 3. Check comment.txt
    comment_path = episode_root / "source" / "comment.txt"
    if comment_path.exists():
        comment_text = comment_path.read_text(encoding="utf-8")
        if len(comment_text.strip()) < 20:
            issues.append("comment.txt: Pinned comment draft is too short or empty.")
        elif "?" not in comment_text:
            issues.append("comment.txt: Pinned comment must include an engaging community question (?) to foster listener interaction.")
    else:
        issues.append("comment.txt: File is missing.")

    return issues


def _run_hil1_checks(episode_root: Path, episode_id: str) -> list[dict[str, Any]]:
    analyses, issues = _build_hil1_track_analyses(episode_root, episode_id)
    field_issues = [
        item
        for item in issues
        if (
            "missing:" in item
            or "Styles missing" in item
            or "Exclude Styles missing" in item
            or "Lyrics missing pre-song context" in item
            or "Lyrics context/control" in item
            or "Lyrics start directly" in item
            or "Styles too short/vague" in item
        )
    ]
    structure_issues = [item for item in issues if "title" in item or "structure" in item or "repeats" in item or "pattern" in item]
    overlap_issues = [item for item in issues if "repeats watchlist" in item or "reuses" in item or "too close" in item]
    anti_issues = [item for item in issues if "payoff" in item or "Negative-construction" in item or "Maybe" in item or "Nothing" in item]

    package_issues = _run_hil1_core_package_checks(episode_root)

    return [
        _make_quality_check(
            "suno tracks present",
            bool(len(analyses) >= 13),
            ("source/suno-tracks/*.md",),
            len(analyses),
            [analysis["path"] for analysis in analyses[:8]],
            required=True,
        ),
        _make_quality_check(
            "song fields + source controls",
            not field_issues,
            (
                "Song Title",
                "Lyrics Mode",
                "Lyrics",
                "Styles",
                "Exclude Styles",
                "Vocal Gender",
                "Weirdness",
                "Style Influence",
                "Reject Criteria",
                "approx BPM",
                "lyrics context/control block",
                "style control groups",
                "exclude drift guards",
            ),
            len(field_issues),
            field_issues,
            required=True,
        ),
        _make_quality_check(
            "lyrics structure & anti-pattern gate",
            not structure_issues and not anti_issues,
            (
                "title_first_check",
                "No/no pattern",
                "Maybe/Nothing start",
                "one small/soft note/sign/line pattern",
                "final hook stacking",
            ),
            len(structure_issues) + len(anti_issues),
            structure_issues + anti_issues,
            required=True,
        ),
        _make_quality_check(
            "lexical overlap gate",
            not overlap_issues,
            ("watchlist overlap",),
            len(overlap_issues),
            overlap_issues,
            required=True,
        ),
        _make_quality_check(
            "episode overlap gate",
            not [item for item in issues if "earlier episode" in item or "too close to previous" in item],
            ("no title-level overlap",),
            len([item for item in issues if "earlier episode" in item or "too close to previous" in item]),
            [item for item in issues if "earlier episode" in item or "too close to previous" in item],
            required=True,
        ),
        _make_quality_check(
            "cozy channel package gate",
            not package_issues,
            (
                "title format validation",
                "ai workflow disclosure",
                "no platform safety claims",
                "signature art direction keys",
                "safe zone overlays",
                "community pinned comment with engagement question",
            ),
            len(package_issues),
            package_issues,
            required=True,
        ),
    ]


def _extract_track_index(value: str) -> int | None:
    stem = Path(value).stem
    match = _TRACK_INDEX_RE.search(stem)
    if not match:
        return None
    index = int(match.group(1))
    return index if 1 <= index <= 13 else None


def _extract_track_variant(value: str) -> str | None:
    stem = Path(value).stem
    match = _TRACK_VARIANT_RE.search(stem)
    return match.group(1).lower() if match else None


def _candidate_files_with_indices(audio_root: Path, subset_name: str) -> tuple[list[Path], list[str], dict[int, int]]:
    files = sorted((audio_root / subset_name).glob("*.wav")) if audio_root.is_dir() else []
    unknown: list[str] = []
    index_counts: dict[int, int] = {}
    for path in files:
        index = _extract_track_index(path.name)
        if index is None:
            unknown.append(path.name)
        else:
            index_counts[index] = index_counts.get(index, 0) + 1
    return files, unknown, index_counts


def _run_hil2_checks(episode_root: Path, episode_id: str) -> list[dict[str, Any]]:
    del episode_id
    candidate_root = CANDIDATE_ROOT / episode_root.name
    audio_root = candidate_root / "audio"
    visual_root = candidate_root / "visual"

    selected_files, selected_unknown, selected_counts = _candidate_files_with_indices(audio_root, "selected")
    pool_files, pool_unknown, pool_counts = _candidate_files_with_indices(audio_root, "pool")
    selected_variant_unknown: list[str] = []
    pool_variant_unknown: list[str] = []
    selected_wrong_variant: list[str] = []
    pool_wrong_variant: list[str] = []

    for path in selected_files:
        variant = _extract_track_variant(path.name)
        if variant is None:
            selected_variant_unknown.append(path.name)
        elif variant != "01":
            selected_wrong_variant.append(path.name)

    for path in pool_files:
        variant = _extract_track_variant(path.name)
        if variant is None:
            pool_variant_unknown.append(path.name)
        elif variant != "02":
            pool_wrong_variant.append(path.name)

    selected_c01_count = len(selected_files) - len(selected_variant_unknown) - len(selected_wrong_variant)
    pool_c02_count = len(pool_files) - len(pool_variant_unknown) - len(pool_wrong_variant)
    selected_index_duplicate: list[str] = []
    pool_index_duplicate: list[str] = []
    for track_index, count in selected_counts.items():
        if count > 1:
            selected_index_duplicate.append(f"track {track_index:02d} x{count}")
    for track_index, count in pool_counts.items():
        if count > 1:
            pool_index_duplicate.append(f"track {track_index:02d} x{count}")

    selected_ok = len(selected_files) == 13
    pool_ok = len(pool_files) == 13
    selected_index_missing: list[str] = []
    pool_index_missing: list[str] = []

    for track_index in range(1, 14):
        if selected_counts.get(track_index, 0) == 0:
            selected_index_missing.append(f"track {track_index:02d}")
        if pool_counts.get(track_index, 0) == 0:
            pool_index_missing.append(f"track {track_index:02d}")

    visual_files = [
        item
        for item in sorted(visual_root.glob("**/*"))
        if item.is_file() and item.name != ".DS_Store"
    ]
    selected_visual_files = sorted(
        item
        for item in (visual_root / "selected").glob("*")
        if item.is_file() and item.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp"}
    )
    visual_still = [item for item in visual_files if item.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp"}]
    visual_video = [item for item in visual_files if item.suffix.lower() in {".mp4", ".mov", ".webm"}]

    selected_ratio = f"selected c01:{sum(1 for path in selected_files if '_c01' in path.name.lower())}/13"
    pool_ratio = f"pool c02:{sum(1 for path in pool_files if '_c02' in path.name.lower())}/13"
    variant_ratio = f"selected c01:{selected_c01_count}/13 pool c02:{pool_c02_count}/13"

    checks = [
        _make_quality_check(
            "audio set completeness",
            selected_ok and pool_ok,
            ("audio/selected/*.wav", "audio/pool/*.wav"),
            len(selected_files) + len(pool_files),
            [str(path.relative_to(PROJECT_ROOT)) for path in selected_files[:8]] + [str(path.relative_to(PROJECT_ROOT)) for path in pool_files[:8]],
            required=True,
        ),
        _make_quality_check(
            "audio track continuity",
            (
                not selected_index_missing
                and not pool_index_missing
                and not selected_index_duplicate
                and not pool_index_duplicate
            ),
            ("track 01..13 selected", "track 01..13 pool"),
            len(selected_index_missing) + len(pool_index_missing) + len(selected_index_duplicate) + len(pool_index_duplicate),
            [
                "selected missing: " + ", ".join(selected_index_missing),
                "pool missing: " + ", ".join(pool_index_missing),
                "selected duplicate: " + ", ".join(selected_index_duplicate),
                "pool duplicate: " + ", ".join(pool_index_duplicate),
            ],
            required=True,
        ),
        _make_quality_check(
            "candidate variant lock",
            (
                not selected_variant_unknown
                and not pool_variant_unknown
                and not selected_wrong_variant
                and not pool_wrong_variant
                and selected_c01_count == 13
                and pool_c02_count == 13
            ),
            ("aud-t01..13_c01", "aud-t01..13_c02"),
            len(selected_variant_unknown)
            + len(pool_variant_unknown)
            + len(selected_wrong_variant)
            + len(pool_wrong_variant),
            [
                "selected variant unknown: " + ", ".join(selected_variant_unknown),
                "pool variant unknown: " + ", ".join(pool_variant_unknown),
                "selected wrong variant: " + ", ".join(selected_wrong_variant),
                "pool wrong variant: " + ", ".join(pool_wrong_variant),
                variant_ratio,
            ],
            required=True,
        ),
        _make_quality_check(
            "selected visual evidence",
            bool(selected_visual_files),
            ("visual/*.png", "visual/*.jpg", "visual/*.jpeg", "visual/*.webp", "visual/selected/*", "visual/proofs/*"),
            len(selected_visual_files),
            [str(path.relative_to(PROJECT_ROOT)) for path in selected_visual_files[:8]],
            required=True,
        ),
        _make_quality_check(
            "filename health",
            not selected_unknown and not pool_unknown,
            ("parsable_track_number_in_filename",),
            len(selected_unknown) + len(pool_unknown),
            selected_unknown + pool_unknown,
            required=True,
        ),
    ]

    try:
        import sys
        if str(PROJECT_ROOT / "scripts") not in sys.path:
            sys.path.append(str(PROJECT_ROOT / "scripts"))
        from gate_validation_helpers import run_audio_silence_check
        silence_errors = run_audio_silence_check(episode_root.name, workspace_root=PROJECT_ROOT)
    except Exception as exc:
        silence_errors = [f"Failed to execute audio silence detection check: {exc}"]

    checks.append(
        _make_quality_check(
            "audio silence verification",
            not silence_errors,
            ("no silent gaps >= 5s in selected/pool audio",),
            len(silence_errors),
            silence_errors,
            required=True,
        )
    )

    return checks


def _run_hil3_checks(episode_root: Path, episode_id: str) -> list[dict[str, Any]]:
    del episode_id
    try:
        import sys
        if str(PROJECT_ROOT / "scripts") not in sys.path:
            sys.path.append(str(PROJECT_ROOT / "scripts"))
        from gate_validation_helpers import run_subtitle_alignment_check
        alignment_errors = run_subtitle_alignment_check(episode_root.name, workspace_root=PROJECT_ROOT)
    except Exception as exc:
        alignment_errors = [f"Failed to execute subtitle alignment timing check: {exc}"]

    return [
        _make_quality_check(
            "subtitle timing alignment",
            not alignment_errors,
            ("promoted SRT timing matches selected audio timeline and local JSONs",),
            len(alignment_errors),
            alignment_errors,
            required=True,
        )
    ]


def _split_patterns(value: Any) -> tuple[str, ...]:
    if isinstance(value, str):
        return (value.strip(),) if value.strip() else ()
    if not isinstance(value, list):
        return ()
    return tuple(item.strip() for item in (str(item).strip() for item in value) if item.strip())


def _to_text_tuple(value: Any, fallback: tuple[str, ...] = ()) -> tuple[str, ...]:
    if value is None:
        return fallback
    if isinstance(value, (str, int, float, bool)):
        return (str(value).strip(),) if str(value).strip() else fallback
    if not isinstance(value, list):
        return fallback
    values = tuple(str(item).strip() for item in value)
    normalized = tuple(item for item in values if item)
    return normalized if normalized else fallback


def _parse_custom_checks(raw_checks: Any, fallback: tuple[EvidenceSpec, ...]) -> tuple[EvidenceSpec, ...]:
    if not isinstance(raw_checks, list):
        return fallback
    parsed_checks: list[EvidenceSpec] = []
    for check in raw_checks:
        if not isinstance(check, dict):
            continue
        pattern_values = _split_patterns(check.get("patterns"))
        if not pattern_values:
            continue
        try:
            min_count = int(check.get("min_count", 1))
        except (TypeError, ValueError):
            min_count = 1
        parsed_checks.append(
            EvidenceSpec(
                name=str(check.get("name", "custom check")),
                base=str(check.get("base", "episode")).strip() or "episode",
                patterns=pattern_values,
                operator=str(check.get("operator", "all")),
                required=bool(check.get("required", True)),
                min_count=min_count,
            )
        )
    return tuple(parsed_checks) if parsed_checks else fallback


def _to_custom_check_list(value: Any, fallback: tuple[str, ...]) -> tuple[str, ...]:
    if isinstance(value, list):
        normalized = tuple(item.strip() for item in (str(item).strip() for item in value) if item.strip())
        return normalized if normalized else fallback
    if isinstance(value, tuple):
        normalized = tuple(item.strip() for item in (str(item).strip() for item in value) if item.strip())
        return normalized if normalized else fallback
    return fallback


def load_stage_plan(manifest: dict[str, Any]) -> dict[str, HilStage]:
    plan = manifest.get("pipeline")
    if not isinstance(plan, dict):
        return STAGES.copy()

    stage_entries = plan.get("stages")
    if not isinstance(stage_entries, list):
        return STAGES.copy()

    loaded: dict[str, HilStage] = {}
    used_keys: set[str] = set()
    for entry in stage_entries:
        if not isinstance(entry, dict):
            continue
        key = str(entry.get("key", "")).strip().lower()
        if key not in STAGES:
            continue
        fallback = STAGES[key]
        loaded[key] = HilStage(
            key=key,
            title=str(entry.get("title", fallback.title)),
            scope=str(entry.get("scope", fallback.scope)),
            can_work_without_previous=bool(entry.get("can_work_without_previous", fallback.can_work_without_previous)),
            custom_checks=_to_custom_check_list(entry.get("custom_checks"), fallback.custom_checks),
            checks=_parse_custom_checks(entry.get("checks", fallback.checks), fallback.checks),
            allowed_ops=_to_text_tuple(entry.get("allowed_ops"), fallback.allowed_ops),
            blocked_ops=_to_text_tuple(entry.get("blocked_ops"), fallback.blocked_ops),
        )
        used_keys.add(key)

    for key, fallback in STAGES.items():
        if key not in used_keys:
            loaded[key] = fallback

    return loaded


def resolve_episode_root(episode_id: str) -> Path:
    root = EPISODE_ROOT / episode_id
    if not root.exists():
        raise ValueError(f"episode root not found: {root}")
    return root


def load_manifest(episode_root: Path) -> dict[str, Any]:
    manifest_path = episode_root / "manifest.json"
    if not manifest_path.is_file():
        raise FileNotFoundError(f"manifest.json not found: {manifest_path}")
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("manifest.json is not a JSON object")
    return data


def base_root(episode_root: Path, base: str, episode_id: str) -> Path:
    if base == "episode":
        return episode_root
    if base == "candidate":
        return CANDIDATE_ROOT / episode_id
    raise ValueError(f"invalid base kind: {base!r}")


def collect_matches(target_root: Path, pattern: str) -> list[Path]:
    has_wildcard = any(ch in pattern for ch in "*?[")
    if not has_wildcard:
        p = target_root / pattern
        return [p] if p.exists() else []
    return sorted([path for path in target_root.glob(pattern) if path.is_file()])


def check_evidence(episode_root: Path, episode_id: str, spec: EvidenceSpec) -> dict[str, Any]:
    root = base_root(episode_root, spec.base, episode_id)
    all_matches: list[Path] = []
    per_pattern: dict[str, list[Path]] = {}

    for pattern in spec.patterns:
        matches = collect_matches(root, pattern)
        per_pattern[pattern] = matches
        all_matches.extend(matches)

    all_unique = sorted({*all_matches})
    if spec.operator == "all":
        missing_patterns = [p for p, matches in per_pattern.items() if not matches]
        passed = len(missing_patterns) == 0
    elif spec.operator == "any":
        passed = len(all_unique) >= spec.min_count
    else:
        raise ValueError(f"invalid operator {spec.operator!r}")

    samples = [str(item.relative_to(PROJECT_ROOT)) for item in all_unique[:8]]
    return {
        "name": spec.name,
        "required": spec.required,
        "operator": spec.operator,
        "expected": spec.patterns,
        "found": len(all_unique),
        "min_count": spec.min_count,
        "passed": bool(passed),
        "samples": samples,
    }


def manifest_episode_state(manifest: dict[str, Any]) -> dict[str, str]:
    return {
        "status": str(manifest.get("status", "")),
        "gate": str(manifest.get("gate", "")),
        "episode_id": str(manifest.get("episode_id", "")),
    }


def hil_report(episode_id: str, stage_key: str, manifest: dict[str, Any], episode_root: Path) -> dict[str, Any]:
    stage_defs = load_stage_plan(manifest)
    if stage_key not in stage_defs:
        raise ValueError(f"unknown stage: {stage_key}")
    stage = stage_defs[stage_key]
    checks = [check_evidence(episode_root, episode_id, spec) for spec in stage.checks]
    if stage.custom_checks:
        for custom in stage.custom_checks:
            if custom == "source-content-gate" and stage_key == "hil-1":
                checks.extend(_run_hil1_checks(episode_root, episode_id))
            if custom == "media-intake-gate" and stage_key == "hil-2":
                checks.extend(_run_hil2_checks(episode_root, episode_id))
            if custom == "subtitle-alignment-gate" and stage_key == "hil-3":
                checks.extend(_run_hil3_checks(episode_root, episode_id))

    required_missing = [item["name"] for item in checks if item["required"] and not item["passed"]]
    optional_missing = [item["name"] for item in checks if not item["required"] and not item["passed"]]

    order = tuple(stage_defs.keys())
    stage_index = order.index(stage_key)
    dependency_keys = order[:stage_index]
    dependency_ok = True
    dependency_notes: list[str] = []
    if dependency_keys:
        for previous in dependency_keys:
            previous_checks = hil_report(episode_id, previous, manifest, episode_root)["required_checks"]
            previous_missing = [item for item in previous_checks if item["required"] and not item["passed"]]
            if previous_missing:
                dependency_ok = False
                dependency_notes.append(f"{previous} not complete: {', '.join(item['name'] for item in previous_missing)}")

    allowed = bool(not required_missing and (dependency_ok or stage.can_work_without_previous))

    render_cmd = discover_render_script(episode_id)
    hil3_commands = []
    if stage_key == "hil-3":
        hil3_commands.extend(
            [
                f"Run render: {render_cmd}" if render_cmd else "Prepare render script for this episode in scripts/.",
                "Run local render smoke proof after risk review edits.",
                "Generate final thumbnail candidate and save under candidates/<episode>/thumbnail/.",
                "Keep final comment draft in source/comment.txt.",
            ]
        )
    hil4_commands = []
    if stage_key == "hil-4":
        hil4_commands.extend(
            [
                "Run youtube_api_video_upload.py (dry-run first), then execute only if user approved HIL-4.",
                "Run youtube_api_thumbnail.py with final thumbnail.",
                "Run youtube_api_comment.py with source/comment.txt (pin remains manual).",
                "Open schedule path: manual Studio flow or approved external scheduling flow, then write final schedule note.",
            ]
        )

    return {
        "stage": stage_key,
        "title": stage.title,
        "scope": stage.scope,
        "can_enter": allowed,
        "dependency_gate": "passed" if dependency_ok else "blocked",
        "dependency_notes": dependency_notes,
        "required_checks": checks,
        "required_missing": required_missing,
        "optional_missing": optional_missing,
        "allowed_operations": list(stage.allowed_ops),
        "blocked_operations": list(stage.blocked_ops),
        "next_step_actions": hil3_commands if stage_key == "hil-3" else hil4_commands if stage_key == "hil-4" else [],
        "manifest_state": manifest_episode_state(manifest),
    }


def discover_render_script(episode_id: str) -> str | None:
    match = re.match(r"^(s\d+e\d+)", episode_id)
    if not match:
        return None
    episode_render_script = PROJECT_ROOT / "scripts" / f"render_{match.group(1)}_local.py"
    if episode_render_script.is_file():
        return f"python {episode_render_script.as_posix()}"
    return None


def parse_hil(value: str) -> str:
    value = value.strip().lower()
    hil_map = {
        "1": "hil-1",
        "2": "hil-2",
        "3": "hil-3",
        "4": "hil-4",
        "hil1": "hil-1",
        "hil2": "hil-2",
        "hil3": "hil-3",
        "hil4": "hil-4",
        "hil-1": "hil-1",
        "hil-2": "hil-2",
        "hil-3": "hil-3",
        "hil-4": "hil-4",
    }
    if value in hil_map:
        return hil_map[value]
    if value in STAGES:
        return value
    raise ValueError(f"unsupported HIL value: {value}")


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--episode-id", required=True, help="Episode ID like s01e04-bookstore-afternoon-longplay")
    parser.add_argument(
        "--hil",
        choices=tuple(STAGES.keys()) + ("1", "2", "3", "4"),
        help="Target HIL to inspect; default checks all.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output machine-readable JSON",
    )
    return parser.parse_args(list(argv) if argv is not None else None)


def print_text_result(result: dict[str, Any]) -> None:
    if not result.get("can_enter", False):
        print(f"[BLOCKED] {result['stage']} can't open: dependency gate blocked.")
    else:
        print(f"[READY] {result['stage']} open.")

    print(f"Scope: {result['title']} — {result['scope']}")
    if result["dependency_gate"] != "passed":
        for note in result["dependency_notes"]:
            print(f"- {note}")

    manifest = result["manifest_state"]
    print(f"Manifest status: {manifest['status']}")
    print(f"Manifest gate  : {manifest['gate']}")

    for item in result["required_checks"]:
        status = "PASS" if item["passed"] else "FAIL"
        req = "REQ" if item["required"] else "OPT"
        if not item["found"]:
            sample_text = "no files"
        else:
            sample_text = ", ".join(item["samples"])
        print(f"{status} [{req}] {item['name']} found={item['found']} min={item['min_count']} samples={sample_text}")

    if result["required_missing"]:
        print("Missing required evidence:")
        for item in result["required_missing"]:
            print(f"- {item}")
    else:
        print("Required evidence: complete.")

    if result["optional_missing"]:
        print("Optional evidence not found:")
        for item in result["optional_missing"]:
            print(f"- {item}")

    print("Allowed ops:")
    for item in result["allowed_operations"]:
        print(f"- {item}")
    print("Blocked ops:")
    for item in result["blocked_operations"]:
        print(f"- {item}")

    if result["next_step_actions"]:
        print("Next step actions:")
        for item in result["next_step_actions"]:
            print(f"- {item}")


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)
    episode_root = resolve_episode_root(args.episode_id)
    manifest = load_manifest(episode_root)
    stage_defs = load_stage_plan(manifest)
    stage_key = parse_hil(args.hil) if args.hil else ""
    selected = (stage_key,) if stage_key else tuple(stage_defs.keys())
    reports = [hil_report(args.episode_id, stage, manifest, episode_root) for stage in selected]
    if args.json:
        print(json.dumps(reports, indent=2, sort_keys=True))
        return 0

    for item in reports:
        print_text_result(item)
        if item is not reports[-1]:
            print("-" * 80)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
