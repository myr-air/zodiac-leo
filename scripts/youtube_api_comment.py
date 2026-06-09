#!/usr/bin/env python3
"""Generic guarded YouTube Data API top-level comment helper.

Default mode is dry-run. The helper is intentionally narrow: verify the
authenticated channel with channels.list(mine=true), check for an existing
matching top-level channel comment, then create one top-level video comment with
commentThreads.insert. It does not pin comments, update metadata, publish
videos, upload thumbnails/captions, or touch analytics.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import youtube_api_video_upload as video_upload


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EPISODE_ID = "s01e01-campus-cafe-longplay"
DEFAULT_COMMENT_SOURCE = Path(f"channel/episodes/{DEFAULT_EPISODE_ID}/source/metadata.md")

ENV_KEY_VIDEO_ID = "MELLOW_YOUTUBE_VIDEO_ID"
ENV_KEY_COMMENT_FILE = "MELLOW_YOUTUBE_COMMENT_FILE"
ENV_KEY_COMMENT_TEXT = "MELLOW_YOUTUBE_COMMENT_TEXT"

COMMENT_SCOPES = (
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube.readonly",
)


def project_path(path: Path | str) -> Path:
    path = video_upload.expand_path(path)
    return path if path.is_absolute() else PROJECT_ROOT / path


def load_comment_env_file(env_file: Path) -> dict[str, str | Path]:
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
    if raw.get(ENV_KEY_COMMENT_FILE):
        values["comment_file"] = video_upload.expand_path(raw[ENV_KEY_COMMENT_FILE])
    if raw.get(ENV_KEY_COMMENT_TEXT):
        values["comment_text"] = raw[ENV_KEY_COMMENT_TEXT]
    return values


def read_comment_text(comment_text: str = "", comment_file: Path | None = None) -> str:
    if comment_text.strip():
        return comment_text.strip()
    if comment_file is None:
        return ""
    path = project_path(comment_file)
    if not path.is_file():
        raise FileNotFoundError(f"comment file not found: {path}")
    return path.read_text(encoding="utf-8").strip()


def normalize_comment_text(value: str) -> str:
    return "\n".join(line.rstrip() for line in value.strip().splitlines()).strip()


def resolve_execution_inputs(args: argparse.Namespace) -> argparse.Namespace:
    values: dict[str, str | Path] = {}
    if args.env_file:
        values = load_comment_env_file(args.env_file)
    if not args.expected_channel_id and values.get("expected_channel_id"):
        args.expected_channel_id = str(values["expected_channel_id"])
    if not args.video_id and values.get("video_id"):
        args.video_id = str(values["video_id"])
    if args.client_secrets is None and values.get("client_secrets"):
        args.client_secrets = values["client_secrets"]
    if args.token_cache is None and values.get("token_cache"):
        args.token_cache = values["token_cache"]
    if args.comment_file is None and values.get("comment_file"):
        args.comment_file = values["comment_file"]
    if not args.comment_text and values.get("comment_text"):
        args.comment_text = str(values["comment_text"])
    return args


def build_comment_insert_plan(
    expected_channel_id: str = "",
    video_id: str = "",
    comment_text: str = "",
    *,
    episode_id: str = DEFAULT_EPISODE_ID,
    comment_source: Path = DEFAULT_COMMENT_SOURCE,
    force_repost: bool = False,
) -> dict[str, Any]:
    comment = comment_text.strip()
    return {
        "episode_id": episode_id,
        "mode": "dry_run_default_execution_gate_required_comment_only",
        "operations": [
            "channels.list(mine=true)",
            "commentThreads.list(top-level duplicate guard)",
            "commentThreads.insert(top-level)",
        ],
        "expected_channel_id": expected_channel_id,
        "video_id": video_id,
        "comment_source": str(comment_source),
        "comment_length": len(comment),
        "comment_preview": comment[:160],
        "api_comment_post_allowed_after_gate": True,
        "api_comment_pin_supported": False,
        "force_repost": force_repost,
        "duplicate_comment_guard": "Before insert, scan existing top-level comments from the authenticated channel and block exact text duplicates unless --force-repost is supplied.",
        "pinning_note": "Official YouTube Data API v3 supports top-level commentThreads.insert, not a pin-comment operation; pin manually if needed.",
        "requires_existing_video_id": True,
        "requires_expected_channel_id": True,
        "requires_oauth_paths_outside_repo": True,
        "scopes": list(COMMENT_SCOPES),
        "blocked_operations": [
            "videos.insert",
            "thumbnails.set",
            "captions.insert",
            "videos.update(public)",
            "playlistItems.insert",
            "comment pinning",
            "comments.update/delete/moderation",
            "youtubeAnalytics.*",
            "Content ID action",
            "account edit",
        ],
        "release_decision": "comment_api_gate_only_public_publish_or_pin_not_implied",
    }


def validate_comment_execute_preconditions(
    *,
    execute: bool,
    expected_channel_id: str,
    video_id: str,
    comment_text: str,
    client_secrets: Path | None = None,
    token_cache: Path | None = None,
) -> None:
    if not execute:
        return
    if not expected_channel_id.strip():
        raise ValueError("--expected-channel-id is required before any API comment execution")
    if not video_id.strip():
        raise ValueError("--video-id is required before any API comment execution")
    if not comment_text.strip():
        raise ValueError("comment text is required before any API comment execution")
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


def find_existing_channel_comment(
    youtube: Any,
    *,
    channel_id: str,
    video_id: str,
    comment_text: str,
) -> dict[str, Any] | None:
    expected_text = normalize_comment_text(comment_text)
    if not expected_text:
        return None

    page_token: str | None = None
    while True:
        request_kwargs: dict[str, Any] = {
            "part": "snippet",
            "videoId": video_id,
            "maxResults": 100,
            "textFormat": "plainText",
        }
        if page_token:
            request_kwargs["pageToken"] = page_token
        response = youtube.commentThreads().list(**request_kwargs).execute()
        for item in response.get("items", []):
            top_level = item.get("snippet", {}).get("topLevelComment", {})
            snippet = top_level.get("snippet", {})
            author_channel = snippet.get("authorChannelId", {}).get("value")
            if author_channel != channel_id:
                continue
            existing_text = normalize_comment_text(snippet.get("textOriginal") or snippet.get("textDisplay") or "")
            if existing_text == expected_text:
                return {
                    "comment_thread_id": item.get("id"),
                    "comment_id": top_level.get("id"),
                }
        page_token = response.get("nextPageToken")
        if not page_token:
            return None


def execute_comment_insert(
    *,
    expected_channel_id: str,
    video_id: str,
    comment_text: str,
    client_secrets: Path,
    token_cache: Path,
    force_repost: bool = False,
) -> dict[str, Any]:
    validate_comment_execute_preconditions(
        execute=True,
        expected_channel_id=expected_channel_id,
        video_id=video_id,
        comment_text=comment_text,
        client_secrets=client_secrets,
        token_cache=token_cache,
    )
    youtube, _ = video_upload.get_authenticated_service(client_secrets, token_cache, scopes=COMMENT_SCOPES)
    actual_channel_id = video_upload.authenticated_channel_id(youtube)
    video_upload.assert_expected_channel(actual_channel_id=actual_channel_id, expected_channel_id=expected_channel_id)

    existing_comment = find_existing_channel_comment(
        youtube,
        channel_id=actual_channel_id,
        video_id=video_id,
        comment_text=comment_text,
    )
    if existing_comment and not force_repost:
        existing_id = existing_comment.get("comment_thread_id") or existing_comment.get("comment_id")
        raise ValueError(
            "matching top-level comment already exists for this video from the authenticated channel; "
            f"use --force-repost to intentionally create another copy (existing={existing_id})"
        )

    response = youtube.commentThreads().insert(
        part="snippet",
        body={
            "snippet": {
                "channelId": actual_channel_id,
                "videoId": video_id,
                "topLevelComment": {"snippet": {"textOriginal": comment_text.strip()}},
            }
        },
    ).execute()
    top_level_comment = response.get("snippet", {}).get("topLevelComment", {})
    return {
        "video_id": video_id,
        "channel_id": actual_channel_id,
        "comment_thread_id": response.get("id"),
        "comment_id": top_level_comment.get("id"),
        "comment_insert_attempted": True,
        "comment_pin_attempted": False,
        "duplicate_comment_found_before_insert": bool(existing_comment),
        "response": response,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", type=Path, help="External env file with YouTube comment inputs")
    parser.add_argument("--expected-channel-id", default="", help="YouTube channel ID that must match channels.list(mine=true)")
    parser.add_argument("--video-id", default="", help="Existing YouTube video ID for commentThreads.insert")
    parser.add_argument("--client-secrets", type=Path, help="OAuth client secrets JSON path outside this repo")
    parser.add_argument("--token-cache", type=Path, help="OAuth token cache JSON path outside this repo")
    parser.add_argument("--episode-id", default=DEFAULT_EPISODE_ID)
    parser.add_argument("--comment-text", default="", help="Comment body. Prefer --comment-file for multiline copy.")
    parser.add_argument("--comment-file", type=Path, help="Text file containing the exact comment body")
    parser.add_argument("--comment-source", type=Path, default=DEFAULT_COMMENT_SOURCE)
    parser.add_argument("--force-repost", action="store_true", help="Allow posting even when an identical channel comment already exists")
    parser.add_argument("--execute", action="store_true", help="Post the top-level comment after all guards pass")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = resolve_execution_inputs(parse_args(sys.argv[1:] if argv is None else argv))
    comment_text = read_comment_text(args.comment_text, args.comment_file)
    if not args.execute:
        print(
            json.dumps(
                build_comment_insert_plan(
                    expected_channel_id=args.expected_channel_id,
                    video_id=args.video_id,
                    comment_text=comment_text,
                    episode_id=args.episode_id,
                    comment_source=args.comment_source,
                    force_repost=args.force_repost,
                ),
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    result = execute_comment_insert(
        expected_channel_id=args.expected_channel_id,
        video_id=args.video_id,
        comment_text=comment_text,
        client_secrets=args.client_secrets,
        token_cache=args.token_cache,
        force_repost=args.force_repost,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
