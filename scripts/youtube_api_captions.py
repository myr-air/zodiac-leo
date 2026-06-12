#!/usr/bin/env python3
"""Generic guarded YouTube Data API caption upload helper."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import youtube_api_video_upload as video_upload

PROJECT_ROOT = Path(__file__).resolve().parents[1]

ENV_KEY_VIDEO_ID = "MELLOW_YOUTUBE_VIDEO_ID"


def project_path(path: Path | str) -> Path:
    path = video_upload.expand_path(path)
    return path if path.is_absolute() else PROJECT_ROOT / path


def load_caption_env_file(env_file: Path) -> dict[str, str | Path]:
    env_file = video_upload.expand_path(env_file)
    if video_upload.path_is_inside_repo(env_file):
        raise ValueError("refusing env file inside this repository; use an external path")
    if not env_file.is_file():
        raise FileNotFoundError(f"env file not found: {env_file}")

    raw: dict[str, str] = {}
    for line in env_file.read_text(encoding="utf-8").splitlines():
        parsed = video_upload.parse_env_line(line)
        if parsed is None:
            continue
        key, value = parsed
        raw[key] = value

    values: dict[str, str | Path] = {}
    if raw.get(video_upload.ENV_KEY_EXPECTED_CHANNEL_ID):
        values["expected_channel_id"] = raw[video_upload.ENV_KEY_EXPECTED_CHANNEL_ID]
    if raw.get(ENV_KEY_VIDEO_ID):
        values["video_id"] = raw[ENV_KEY_VIDEO_ID]
    if raw.get(video_upload.ENV_KEY_CLIENT_SECRETS):
        values["client_secrets"] = video_upload.expand_path(raw[video_upload.ENV_KEY_CLIENT_SECRETS])
    if raw.get(video_upload.ENV_KEY_TOKEN_CACHE):
        values["token_cache"] = video_upload.expand_path(raw[video_upload.ENV_KEY_TOKEN_CACHE])
    return values


def resolve_execution_inputs(args: argparse.Namespace) -> argparse.Namespace:
    values: dict[str, str | Path] = {}
    if args.env_file:
        values = load_caption_env_file(args.env_file)
    if not args.expected_channel_id and values.get("expected_channel_id"):
        args.expected_channel_id = str(values["expected_channel_id"])
    if not args.video_id and values.get("video_id"):
        args.video_id = str(values["video_id"])
    if args.client_secrets is None and values.get("client_secrets"):
        args.client_secrets = values["client_secrets"]
    if args.token_cache is None and values.get("token_cache"):
        args.token_cache = values["token_cache"]
    return args


def build_caption_upload_plan(
    expected_channel_id: str = "",
    video_id: str = "",
    *,
    caption_path: Path,
    language: str = "th",
    name: str = "Thai (Cozy Translation)",
) -> dict[str, Any]:
    blocked_operations = [
        "videos.insert",
        "videos.update(public)",
        "playlistItems.insert",
        "commentThreads.insert",
        "youtubeAnalytics.*",
        "Content ID action",
        "account edit",
    ]
    return {
        "mode": "dry_run_default_execution_gate_open_caption_only_followup",
        "operations": ["channels.list(mine=true)", "captions.insert"],
        "expected_channel_id": expected_channel_id,
        "video_id": video_id,
        "caption_path": str(caption_path),
        "language": language,
        "name": name,
        "caption_upload_allowed": True,
        "requires_existing_video_id": True,
        "requires_expected_channel_id": True,
        "requires_oauth_paths_outside_repo": True,
        "blocked_operations": blocked_operations,
        "release_decision": "private_video_caption_api_gate_open_public_publish_not_passed",
    }


def validate_caption_execute_preconditions(
    *,
    execute: bool,
    expected_channel_id: str,
    video_id: str,
    client_secrets: Path | None = None,
    token_cache: Path | None = None,
    caption_path: Path | None = None,
) -> None:
    if not execute:
        return
    if not expected_channel_id.strip():
        raise ValueError("--expected-channel-id is required before any API caption execution")
    if not video_id.strip():
        raise ValueError("--video-id is required before any API caption execution")
    if client_secrets is None:
        raise ValueError("--client-secrets is required for execute mode")
    if token_cache is None:
        raise ValueError("--token-cache is required for execute mode")
    if video_upload.path_is_inside_repo(client_secrets):
        raise ValueError("refusing OAuth client secrets path inside this repository")
    if video_upload.path_is_inside_repo(token_cache):
        raise ValueError("refusing OAuth token cache path inside this repository")
    if not client_secrets.expanduser().is_file():
        raise FileNotFoundError(f"OAuth client secrets file not found: {client_secrets}")
    if caption_path is not None and not caption_path.is_file():
        raise FileNotFoundError(f"caption file not found: {caption_path}")


def execute_caption_upload(
    *,
    expected_channel_id: str,
    video_id: str,
    client_secrets: Path,
    token_cache: Path,
    caption_path: Path,
    language: str = "th",
    name: str = "Thai (Cozy Translation)",
) -> dict[str, Any]:
    caption = project_path(caption_path)
    validate_caption_execute_preconditions(
        execute=True,
        expected_channel_id=expected_channel_id,
        video_id=video_id,
        client_secrets=client_secrets,
        token_cache=token_cache,
        caption_path=caption,
    )
    youtube, modules = video_upload.get_authenticated_service(client_secrets, token_cache)
    actual_channel_id = video_upload.authenticated_channel_id(youtube)
    video_upload.assert_expected_channel(actual_channel_id=actual_channel_id, expected_channel_id=expected_channel_id)

    media = modules["MediaFileUpload"](
        str(caption),
        mimetype="*/*",
        chunksize=-1,
        resumable=True
    )
    
    response = youtube.captions().insert(
        part="snippet",
        body={
            "snippet": {
                "videoId": video_id,
                "language": language,
                "name": name,
                "isDraft": False
            }
        },
        media_body=media
    ).execute()

    return {
        "video_id": video_id,
        "channel_id": actual_channel_id,
        "caption_path": str(caption.relative_to(PROJECT_ROOT) if PROJECT_ROOT in [caption, *caption.parents] else caption),
        "caption_upload_attempted": True,
        "response": response,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", type=Path, help="External env file with YouTube caption inputs")
    parser.add_argument("--expected-channel-id", default="", help="YouTube channel ID that must match channels.list(mine=true)")
    parser.add_argument("--video-id", default="", help="Existing YouTube video ID for captions.insert")
    parser.add_argument("--client-secrets", type=Path, help="OAuth client secrets JSON path outside this repo")
    parser.add_argument("--token-cache", type=Path, help="OAuth token cache JSON path outside this repo")
    parser.add_argument("--caption-path", type=Path, required=True, help="Path to SRT/VTT file to upload")
    parser.add_argument("--language", default="th", help="Subtitle language code (e.g. th, en)")
    parser.add_argument("--name", default="Thai (Cozy Translation)", help="Display name of subtitle track")
    parser.add_argument("--execute", action="store_true", help="Perform the API caption upload after all guards pass")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = resolve_execution_inputs(parse_args(sys.argv[1:] if argv is None else argv))
    if not args.execute:
        print(
            json.dumps(
                build_caption_upload_plan(
                    expected_channel_id=args.expected_channel_id,
                    video_id=args.video_id,
                    caption_path=args.caption_path,
                    language=args.language,
                    name=args.name,
                ),
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    result = execute_caption_upload(
        expected_channel_id=args.expected_channel_id,
        video_id=args.video_id,
        client_secrets=args.client_secrets,
        token_cache=args.token_cache,
        caption_path=args.caption_path,
        language=args.language,
        name=args.name,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
