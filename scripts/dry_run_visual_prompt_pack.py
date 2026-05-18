#!/usr/bin/env python3
"""Dry-run a source-only visual prompt pack.

This helper extracts copy-paste prompts from an episode visual prompt pack and
prints them to stdout. It never calls provider APIs, opens browsers, uploads
reference images, writes generated media, or creates credentials.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALID_PROVIDERS = ("gemini", "chatgpt")

START_RE = re.compile(r"^<!-- prompt:start ([a-z0-9_-]+) -->\s*$")
END_RE = re.compile(r"^<!-- prompt:end ([a-z0-9_-]+) -->\s*$")


def parse_prompt_blocks(text: str) -> dict[str, str]:
    prompts: dict[str, str] = {}
    current: str | None = None
    buffer: list[str] = []

    for line_number, line in enumerate(text.splitlines(), start=1):
        start = START_RE.match(line)
        end = END_RE.match(line)

        if start:
            if current is not None:
                raise ValueError(f"nested prompt block at line {line_number}: {line}")
            current = start.group(1)
            buffer = []
            continue

        if end:
            provider = end.group(1)
            if current is None:
                raise ValueError(f"orphan prompt end at line {line_number}: {line}")
            if provider != current:
                raise ValueError(
                    f"prompt end mismatch at line {line_number}: expected {current}, got {provider}"
                )
            body = "\n".join(buffer).strip()
            if not body:
                raise ValueError(f"empty prompt block for provider {provider!r}")
            prompts[provider] = body
            current = None
            buffer = []
            continue

        if current is not None:
            buffer.append(line)

    if current is not None:
        raise ValueError(f"unterminated prompt block for provider {current!r}")

    return prompts


def validate_prompt(provider: str, prompt: str) -> list[str]:
    lower = prompt.lower()
    errors: list[str] = []

    required_phrases = [
        "16:9",
        "original",
        "reference-free" if provider == "gemini" else "no reference-image input",
        "adult-coded",
        "gold/orange crescent-vinyl charm",
        "negative space",
        "no logos",
        "no watermark",
        "no attached reference images" if provider == "chatgpt" else "attached reference image usage",
    ]
    for phrase in required_phrases:
        if phrase.lower() not in lower:
            errors.append(f"{provider}: missing required phrase {phrase!r}")

    forbidden_positive_claims = [
        "copyright-free",
        "royalty-free",
        "content id-safe",
        "monetization-safe",
        "platform-safe",
        "upload-ready",
        "publish-ready",
    ]
    for claim in forbidden_positive_claims:
        if claim in lower:
            errors.append(f"{provider}: blocked positive rights/platform claim {claim!r}")

    automation_markers = ["api key", "oauth", "curl ", "http://", "https://"]
    for marker in automation_markers:
        if marker in lower:
            errors.append(f"{provider}: automation/network marker should not appear in prompt: {marker!r}")

    return errors


def selected_providers(requested: str, prompts: dict[str, str]) -> list[str]:
    if requested == "all":
        return [provider for provider in VALID_PROVIDERS if provider in prompts]
    return [requested]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Dry-run source-only visual prompt handoff.")
    parser.add_argument(
        "--source",
        type=Path,
        required=True,
        help="Markdown prompt pack containing prompt:start/end markers.",
    )
    parser.add_argument(
        "--provider",
        choices=("all", *VALID_PROVIDERS),
        default="all",
        help="Prompt provider block to print.",
    )
    parser.add_argument("--list", action="store_true", help="List available provider blocks.")
    args = parser.parse_args(argv)

    source = args.source if args.source.is_absolute() else ROOT / args.source
    if not source.is_file():
        print(f"ERROR: prompt source not found: {source}", file=sys.stderr)
        return 1

    try:
        prompts = parse_prompt_blocks(source.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - user-facing CLI error
        print(f"ERROR: failed to parse prompt pack: {exc}", file=sys.stderr)
        return 1

    if args.list:
        for provider in sorted(prompts):
            print(provider)
        return 0

    providers = selected_providers(args.provider, prompts)
    missing = [provider for provider in providers if provider not in prompts]
    if missing:
        print(f"ERROR: missing provider block(s): {', '.join(missing)}", file=sys.stderr)
        return 1

    validation_errors: list[str] = []
    for provider in providers:
        validation_errors.extend(validate_prompt(provider, prompts[provider]))
    if validation_errors:
        for error in validation_errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("DRY RUN ONLY: source prompt handoff")
    print(f"source: {source.relative_to(ROOT)}")
    print("boundary: no API calls, no browser automation, no reference-image upload, no generated media")
    print("validation: passed")
    for provider in providers:
        print()
        print(f"--- COPY PROMPT: {provider} ---")
        print(prompts[provider])
        print(f"--- END PROMPT: {provider} ---")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
