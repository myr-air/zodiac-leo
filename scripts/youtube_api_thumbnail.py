#!/usr/bin/env python3
"""Generic guarded YouTube Data API thumbnail upload helper."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import youtube_api_video_upload as video_upload


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EPISODE_ID = "s01e01-campus-cafe-longplay"
DEFAULT_THUMBNAIL_PATH = Path(
    "candidates/s01e01-campus-cafe-longplay/thumbnail/"
    "s01e01-campus-cafe-longplay.thumbnail-v4-big-brand-depth-1280x720.jpg"
)
DEFAULT_THUMBNAIL_SOURCE = Path(f"channel/episodes/{DEFAULT_EPISODE_ID}/source/youtube-api-thumbnail-upload-package.md")

ENV_KEY_VIDEO_ID = "MELLOW_YOUTUBE_VIDEO_ID"


def project_path(path: Path | str) -> Path:
    path = video_upload.expand_path(path)
    return path if path.is_absolute() else PROJECT_ROOT / path


def load_thumbnail_env_file(env_file: Path) -> dict[str, str | Path]:
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
        values = load_thumbnail_env_file(args.env_file)
    if not args.expected_channel_id and values.get("expected_channel_id"):
        args.expected_channel_id = str(values["expected_channel_id"])
    if not args.video_id and values.get("video_id"):
        args.video_id = str(values["video_id"])
    if args.client_secrets is None and values.get("client_secrets"):
        args.client_secrets = values["client_secrets"]
    if args.token_cache is None and values.get("token_cache"):
        args.token_cache = values["token_cache"]
    return args


def build_thumbnail_upload_plan(
    expected_channel_id: str = "",
    video_id: str = "",
    *,
    episode_id: str = DEFAULT_EPISODE_ID,
    thumbnail_path: Path = DEFAULT_THUMBNAIL_PATH,
    thumbnail_source: Path = DEFAULT_THUMBNAIL_SOURCE,
) -> dict[str, Any]:
    blocked_operations = [
        "videos.insert",
        "captions.insert",
        "videos.update(public)",
        "playlistItems.insert",
        "commentThreads.insert",
        "youtubeAnalytics.*",
        "Content ID action",
        "account edit",
    ]
    return {
        "episode_id": episode_id,
        "mode": "dry_run_default_execution_gate_open_thumbnail_only_followup",
        "operations": ["channels.list(mine=true)", "thumbnails.set"],
        "expected_channel_id": expected_channel_id,
        "video_id": video_id,
        "thumbnail_path": str(thumbnail_path),
        "thumbnail_source": str(thumbnail_source),
        "mime_type": "image/jpeg",
        "thumbnail_upload_allowed": True,
        "requires_existing_video_id": True,
        "requires_expected_channel_id": True,
        "requires_oauth_paths_outside_repo": True,
        "blocked_operations": blocked_operations,
        "release_decision": "private_video_thumbnail_api_gate_open_public_publish_not_passed",
    }


def validate_thumbnail_execute_preconditions(
    *,
    execute: bool,
    expected_channel_id: str,
    video_id: str,
    client_secrets: Path | None = None,
    token_cache: Path | None = None,
    thumbnail_path: Path | None = None,
) -> None:
    if not execute:
        return
    if not expected_channel_id.strip():
        raise ValueError("--expected-channel-id is required before any API thumbnail execution")
    if not video_id.strip():
        raise ValueError("--video-id is required before any API thumbnail execution")
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
    if thumbnail_path is not None and not thumbnail_path.is_file():
        raise FileNotFoundError(f"thumbnail file not found: {thumbnail_path}")


def execute_thumbnail_upload(
    *,
    expected_channel_id: str,
    video_id: str,
    client_secrets: Path,
    token_cache: Path,
    thumbnail_path: Path | None = None,
) -> dict[str, Any]:
    thumbnail = project_path(thumbnail_path or DEFAULT_THUMBNAIL_PATH)
    validate_thumbnail_execute_preconditions(
        execute=True,
        expected_channel_id=expected_channel_id,
        video_id=video_id,
        client_secrets=client_secrets,
        token_cache=token_cache,
        thumbnail_path=thumbnail,
    )
    youtube, modules = video_upload.get_authenticated_service(client_secrets, token_cache)
    actual_channel_id = video_upload.authenticated_channel_id(youtube)
    video_upload.assert_expected_channel(actual_channel_id=actual_channel_id, expected_channel_id=expected_channel_id)

    response = youtube.thumbnails().set(
        videoId=video_id,
        media_body=modules["MediaFileUpload"](str(thumbnail), mimetype="image/jpeg", chunksize=-1, resumable=True),
    ).execute()
    return {
        "video_id": video_id,
        "channel_id": actual_channel_id,
        "thumbnail_path": str(thumbnail.relative_to(PROJECT_ROOT) if PROJECT_ROOT in [thumbnail, *thumbnail.parents] else thumbnail),
        "thumbnail_upload_attempted": True,
        "response": response,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", type=Path, help="External env file with YouTube thumbnail inputs")
    parser.add_argument("--expected-channel-id", default="", help="YouTube channel ID that must match channels.list(mine=true)")
    parser.add_argument("--video-id", default="", help="Existing YouTube video ID for thumbnails.set")
    parser.add_argument("--client-secrets", type=Path, help="OAuth client secrets JSON path outside this repo")
    parser.add_argument("--token-cache", type=Path, help="OAuth token cache JSON path outside this repo")
    parser.add_argument("--episode-id", default=DEFAULT_EPISODE_ID)
    parser.add_argument("--thumbnail", type=Path, default=DEFAULT_THUMBNAIL_PATH)
    parser.add_argument("--thumbnail-source", type=Path, default=DEFAULT_THUMBNAIL_SOURCE)
    parser.add_argument("--execute", action="store_true", help="Perform the API thumbnail upload after all guards pass")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = resolve_execution_inputs(parse_args(sys.argv[1:] if argv is None else argv))
    if not args.execute:
        print(
            json.dumps(
                build_thumbnail_upload_plan(
                    expected_channel_id=args.expected_channel_id,
                    video_id=args.video_id,
                    episode_id=args.episode_id,
                    thumbnail_path=args.thumbnail,
                    thumbnail_source=args.thumbnail_source,
                ),
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    result = execute_thumbnail_upload(
        expected_channel_id=args.expected_channel_id,
        video_id=args.video_id,
        client_secrets=args.client_secrets,
        token_cache=args.token_cache,
        thumbnail_path=args.thumbnail,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
