#!/usr/bin/env python3
"""Generic guarded YouTube Data API video upload helper.

Default mode is dry-run. The helper is intentionally narrow: verify the
authenticated channel with channels.list(mine=true), then upload a video as
private with videos.insert. It does not upload captions or thumbnails.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

from leo_resource_paths import resolve_candidates_root


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LEO_CANDIDATES_ROOT = resolve_candidates_root(PROJECT_ROOT)
DEFAULT_EPISODE_ID = "s01e01-campus-cafe-longplay"
DEFAULT_VIDEO_PATH = Path(
    LEO_CANDIDATES_ROOT
    / "s01e01-campus-cafe-longplay/render/future-local-render-05/video/"
    "s01e01-campus-cafe-longplay.v6-subtitled-1080p24-qa.mp4"
)
DEFAULT_RESOURCE_JSON = Path(f"channel/episodes/{DEFAULT_EPISODE_ID}/source/youtube-video-resource.json")
DEFAULT_METADATA_SOURCE = Path(f"channel/episodes/{DEFAULT_EPISODE_ID}/source/youtube-api-video-upload-package.md")

ENV_KEY_EXPECTED_CHANNEL_ID = "MELLOW_YOUTUBE_EXPECTED_CHANNEL_ID"
ENV_KEY_CLIENT_SECRETS = "MELLOW_YOUTUBE_CLIENT_SECRETS"
ENV_KEY_TOKEN_CACHE = "MELLOW_YOUTUBE_TOKEN_CACHE"

SCOPES = (
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/youtube.force-ssl",
)
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"


def expand_path(path: Path | str) -> Path:
    return Path(os.path.expandvars(str(path))).expanduser()


def project_path(path: Path | str) -> Path:
    path = expand_path(path)
    return path if path.is_absolute() else PROJECT_ROOT / path


def path_is_inside_repo(path: Path) -> bool:
    resolved = expand_path(path).resolve()
    root = PROJECT_ROOT.resolve()
    return root in [resolved, *resolved.parents]


def parse_env_line(line: str) -> tuple[str, str] | None:
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return None
    if stripped.startswith("export "):
        stripped = stripped[len("export ") :].lstrip()
    if "=" not in stripped:
        raise ValueError(f"invalid env line without '=': {line!r}")
    key, value = stripped.split("=", 1)
    key = key.strip()
    value = value.strip()
    if not key:
        raise ValueError(f"invalid env line with empty key: {line!r}")
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]
    return key, value


def load_video_resource(resource_json: Path | str = DEFAULT_RESOURCE_JSON) -> dict[str, Any]:
    path = project_path(resource_json)
    data = json.loads(path.read_text(encoding="utf-8"))
    status = data.get("status", {})
    if status.get("privacyStatus") != "private":
        raise ValueError("video resource must keep status.privacyStatus as private")
    if "captions" in data:
        raise ValueError("video resource must not include captions")
    if "thumbnail" in data:
        raise ValueError("video resource must not include thumbnail")
    return data


def load_env_file(env_file: Path) -> dict[str, str | Path]:
    env_file = expand_path(env_file)
    if path_is_inside_repo(env_file):
        raise ValueError("refusing env file inside this repository; use an external path")
    if not env_file.is_file():
        raise FileNotFoundError(f"env file not found: {env_file}")

    raw: dict[str, str] = {}
    for line in env_file.read_text(encoding="utf-8").splitlines():
        parsed = parse_env_line(line)
        if parsed is None:
            continue
        key, value = parsed
        raw[key] = value

    values: dict[str, str | Path] = {}
    if raw.get(ENV_KEY_EXPECTED_CHANNEL_ID):
        values["expected_channel_id"] = raw[ENV_KEY_EXPECTED_CHANNEL_ID]
    if raw.get(ENV_KEY_CLIENT_SECRETS):
        values["client_secrets"] = expand_path(raw[ENV_KEY_CLIENT_SECRETS])
    if raw.get(ENV_KEY_TOKEN_CACHE):
        values["token_cache"] = expand_path(raw[ENV_KEY_TOKEN_CACHE])
    return values


def resolve_execution_inputs(args: argparse.Namespace) -> argparse.Namespace:
    values: dict[str, str | Path] = {}
    if args.env_file:
        values = load_env_file(args.env_file)
    if not args.expected_channel_id and values.get("expected_channel_id"):
        args.expected_channel_id = str(values["expected_channel_id"])
    if args.client_secrets is None and values.get("client_secrets"):
        args.client_secrets = values["client_secrets"]
    if args.token_cache is None and values.get("token_cache"):
        args.token_cache = values["token_cache"]
    return args


def build_upload_plan(
    expected_channel_id: str = "",
    *,
    episode_id: str = DEFAULT_EPISODE_ID,
    video_path: Path = DEFAULT_VIDEO_PATH,
    resource_json: Path = DEFAULT_RESOURCE_JSON,
    metadata_source: Path = DEFAULT_METADATA_SOURCE,
    resource: dict[str, Any] | None = None,
    comment_file: Path | None = None,
) -> dict[str, Any]:
    allowed_ops = ["channels.list(mine=true)", "videos.insert(private)"]
    blocked_ops = [
        "captions.insert",
        "thumbnails.set",
        "videos.update(public)",
        "playlistItems.insert",
        "commentThreads.insert",
        "youtubeAnalytics.*",
        "Content ID action",
    ]
    if comment_file is not None:
        allowed_ops.append("commentThreads.insert(top-level)")
        if "commentThreads.insert" in blocked_ops:
            blocked_ops.remove("commentThreads.insert")

    return {
        "episode_id": episode_id,
        "mode": "dry_run_default_execution_gate_open_private_video_only",
        "operations": ["channels.list(mine=true)", "videos.insert"],
        "expected_channel_id": expected_channel_id,
        "video_path": str(video_path),
        "resource_json": str(resource_json),
        "metadata_source": str(metadata_source),
        "part": "snippet,status",
        "mime_type": "video/mp4",
        "resumable": True,
        "notify_subscribers": False,
        "caption_upload_blocked": True,
        "thumbnail_upload_blocked": True,
        "release_decision": "private_api_video_upload_gate_open_public_publish_not_passed",
        "account_action_default": "blocked_except_private_videos_insert_after_channel_verification",
        "execution_gate": {
            "status": "open_private_video_upload_only",
            "allowed_operations": allowed_ops,
            "blocked_operations": blocked_ops,
            "allows_caption_upload": False,
            "allows_public_publish": False,
            "requires_expected_channel_id": True,
            "requires_oauth_paths_outside_repo": True,
        },
        "resource": resource if resource is not None else load_video_resource(resource_json),
    }


def validate_execute_preconditions(
    *,
    execute: bool,
    expected_channel_id: str,
    client_secrets: Path | None = None,
    token_cache: Path | None = None,
    video_path: Path | None = None,
) -> None:
    if not execute:
        return
    if not expected_channel_id.strip():
        raise ValueError("--expected-channel-id is required before any API upload execution")
    if client_secrets is None:
        raise ValueError("--client-secrets is required for execute mode")
    if token_cache is None:
        raise ValueError("--token-cache is required for execute mode")
    if path_is_inside_repo(client_secrets):
        raise ValueError("refusing OAuth client secrets path inside this repository")
    if path_is_inside_repo(token_cache):
        raise ValueError("refusing OAuth token cache path inside this repository")
    if not client_secrets.expanduser().is_file():
        raise FileNotFoundError(f"OAuth client secrets file not found: {client_secrets}")
    if video_path is not None and not video_path.is_file():
        raise FileNotFoundError(f"video file not found: {video_path}")


def assert_expected_channel(*, actual_channel_id: str, expected_channel_id: str) -> None:
    if actual_channel_id != expected_channel_id:
        raise ValueError(
            "authenticated channel mismatch; refusing upload: "
            f"actual={actual_channel_id!r} expected={expected_channel_id!r}"
        )


def load_google_api_modules() -> dict[str, Any]:
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
    except ImportError as exc:
        raise RuntimeError(
            "execute mode requires google-api-python-client google-auth "
            "google-auth-oauthlib installed outside this script"
        ) from exc
    return {
        "Request": Request,
        "Credentials": Credentials,
        "InstalledAppFlow": InstalledAppFlow,
        "build": build,
        "MediaFileUpload": MediaFileUpload,
    }


def credentials_have_required_scopes(credentials: Any, scopes: tuple[str, ...] = SCOPES) -> bool:
    if hasattr(credentials, "has_scopes"):
        return bool(credentials.has_scopes(scopes))
    granted = set(getattr(credentials, "granted_scopes", None) or getattr(credentials, "scopes", None) or [])
    return set(scopes).issubset(granted)


def load_cached_credentials(credentials_cls: Any, token_cache: Path, scopes: tuple[str, ...] = SCOPES) -> Any | None:
    if not token_cache.is_file():
        return None
    try:
        credentials = credentials_cls.from_authorized_user_file(str(token_cache))
    except ValueError:
        return None
    if not credentials_have_required_scopes(credentials, scopes):
        return None
    return credentials


def get_authenticated_service(client_secrets: Path, token_cache: Path, scopes: tuple[str, ...] = SCOPES):
    modules = load_google_api_modules()
    token_cache = token_cache.expanduser()
    credentials = load_cached_credentials(modules["Credentials"], token_cache, scopes)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(modules["Request"]())
        else:
            flow = modules["InstalledAppFlow"].from_client_secrets_file(str(client_secrets.expanduser()), scopes)
            credentials = flow.run_local_server(port=0)
        token_cache.parent.mkdir(parents=True, exist_ok=True)
        token_cache.write_text(credentials.to_json(), encoding="utf-8")
    return modules["build"](API_SERVICE_NAME, API_VERSION, credentials=credentials), modules


def authenticated_channel_id(youtube: Any) -> str:
    response = youtube.channels().list(part="id,snippet", mine=True).execute()
    items = response.get("items", [])
    if not items:
        raise ValueError("authenticated account did not return a YouTube channel")
    if len(items) > 1:
        raise ValueError("authenticated account returned multiple channels; refusing ambiguous upload")
    channel_id = items[0].get("id")
    if not channel_id:
        raise ValueError("authenticated channel response did not include id")
    return channel_id


def execute_video_upload(
    *,
    expected_channel_id: str,
    client_secrets: Path,
    token_cache: Path,
    video_path: Path = DEFAULT_VIDEO_PATH,
    resource_json: Path = DEFAULT_RESOURCE_JSON,
    notify_subscribers: bool = False,
    comment_file: Path | None = None,
) -> dict[str, Any]:
    resolved_video = project_path(video_path)
    validate_execute_preconditions(
        execute=True,
        expected_channel_id=expected_channel_id,
        client_secrets=client_secrets,
        token_cache=token_cache,
        video_path=resolved_video,
    )
    youtube, modules = get_authenticated_service(client_secrets, token_cache)
    actual_channel_id = authenticated_channel_id(youtube)
    assert_expected_channel(actual_channel_id=actual_channel_id, expected_channel_id=expected_channel_id)
    resource = load_video_resource(resource_json)
    request = youtube.videos().insert(
        part="snippet,status",
        body=resource,
        media_body=modules["MediaFileUpload"](str(resolved_video), mimetype="video/mp4", chunksize=-1, resumable=True),
        notifySubscribers=notify_subscribers,
    )
    response = None
    while response is None:
        _, response = request.next_chunk()

    video_id = response.get("id")
    comment_posted = False
    comment_thread_id = None
    if video_id and comment_file is not None:
        resolved_comment_file = project_path(comment_file)
        if resolved_comment_file.is_file():
            comment_text = resolved_comment_file.read_text(encoding="utf-8").strip()
            if comment_text:
                try:
                    comment_response = youtube.commentThreads().insert(
                        part="snippet",
                        body={
                            "snippet": {
                                "channelId": actual_channel_id,
                                "videoId": video_id,
                                "topLevelComment": {"snippet": {"textOriginal": comment_text}},
                            }
                        },
                    ).execute()
                    comment_posted = True
                    comment_thread_id = comment_response.get("id")
                except Exception as e:
                    print(f"Warning: failed to post comment: {e}", file=sys.stderr)

    return {
        "video_id": video_id,
        "channel_id": actual_channel_id,
        "privacy_status": resource["status"]["privacyStatus"],
        "caption_upload_attempted": False,
        "thumbnail_upload_attempted": False,
        "comment_posted": comment_posted,
        "comment_thread_id": comment_thread_id,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", type=Path, help="External env file with YouTube upload inputs")
    parser.add_argument("--expected-channel-id", default="", help="YouTube channel ID that must match channels.list(mine=true)")
    parser.add_argument("--client-secrets", type=Path, help="OAuth client secrets JSON path outside this repo")
    parser.add_argument("--token-cache", type=Path, help="OAuth token cache JSON path outside this repo")
    parser.add_argument("--episode-id", default=DEFAULT_EPISODE_ID)
    parser.add_argument("--video", type=Path, default=DEFAULT_VIDEO_PATH)
    parser.add_argument("--resource-json", type=Path, default=DEFAULT_RESOURCE_JSON)
    parser.add_argument("--metadata-source", type=Path, default=DEFAULT_METADATA_SOURCE)
    parser.add_argument("--comment-file", type=Path, help="Text file containing the exact pinned comment body")
    parser.add_argument("--execute", action="store_true", help="Perform the API upload after all guards pass")
    parser.add_argument("--notify-subscribers", action="store_true", help="Request subscriber notifications if execution is approved")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = resolve_execution_inputs(parse_args(sys.argv[1:] if argv is None else argv))
    comment_file = getattr(args, "comment_file", None)
    if not comment_file and args.env_file:
        try:
            raw_env = load_env_file(args.env_file)
            if "comment_file" in raw_env:
                comment_file = Path(raw_env["comment_file"])
        except Exception:
            pass

    if not args.execute:
        print(
            json.dumps(
                build_upload_plan(
                    args.expected_channel_id,
                    episode_id=args.episode_id,
                    video_path=args.video,
                    resource_json=args.resource_json,
                    metadata_source=args.metadata_source,
                    comment_file=comment_file,
                ),
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    result = execute_video_upload(
        expected_channel_id=args.expected_channel_id,
        client_secrets=args.client_secrets,
        token_cache=args.token_cache,
        video_path=args.video,
        resource_json=args.resource_json,
        notify_subscribers=args.notify_subscribers,
        comment_file=comment_file,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
