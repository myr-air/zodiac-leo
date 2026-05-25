# S01E01 YouTube API Execution Gate — After-School First Love Longplay

Status: open / private video API upload plus thumbnail follow-up / public release not passed  
Episode: `s01e01-campus-cafe-longplay`  
Opened: 2026-05-25

## 0. Boundary

The user opened the OAuth/API execution gate for the API route and initially kept scope to the video upload only. This gate now allows one future YouTube Data API `videos.insert` upload of the render-05 MP4 as `private`, plus one thumbnail-only `thumbnails.set` follow-up using the selected local JPEG after a private video ID exists. Both helpers must verify that the authenticated channel ID matches the user-provided expected channel ID before any API mutation.

This gate does not approve public publishing, scheduling, visibility changes after upload, captions, playlists, comments, analytics, Content ID action, browser automation, YouTube Studio edits, account edits, credential storage in repo, private account-state storage, extra thumbnail variants, or positive rights/platform claims.

## 1. Security Packet

```text
Scope: one private S01E01 render-05 video upload using YouTube Data API videos.insert plus one thumbnail-only thumbnails.set follow-up for the selected local JPEG
Mode: narrow execution gate; not public release
Assets: render-05 MP4, selected local thumbnail JPEG, metadata payload from source/metadata.md, source/youtube-api-video-upload-package.md, and source/youtube-api-thumbnail-upload-package.md
Actors: user-owned Google/YouTube account, OpenCode helper script, YouTube Data API
Trust boundaries: local repo -> external OAuth flow -> YouTube account/channel -> YouTube Data API
Lanes selected: Secrets/Crypto, External Boundary, Agent/Automation, Data Exposure, Abuse/Business Logic
Lanes skipped: Authn/Authz application roles are not implemented here; Config/Deployment and Migration/Destructive Ops are not touched
Allowed actions: channels.list(mine=true), videos.insert(private), thumbnails.set for the selected local JPEG after video ID exists
Blocked actions: public publish, schedule, visibility update, captions.insert, playlist/comment/analytics/Content ID/account operations, browser automation, token or client-secret storage in repo, extra thumbnail variants
Required inputs: expected channel ID, OAuth client secrets path outside repo, token cache path outside repo; thumbnail follow-up also requires the private video ID; may be supplied through an external env file
Stop triggers: missing or mismatched channel ID, missing video ID for thumbnail step, OAuth paths inside repo, missing local video or thumbnail, API/client dependency failure, account upload limit/verification issue, YouTube checks/policy/copyright notice, any user concern requiring metadata or asset change
```

## 2. Env File Workflow

Use one channel-level env file only outside the repository. The repo contains a placeholder template at `channel/templates/youtube-api-upload-env.example`.

Example setup:

```bash
mkdir -p "$HOME/.config/mellow-longplay/youtube-upload"
cp channel/templates/youtube-api-upload-env.example "$HOME/.config/mellow-longplay/youtube-upload/channel.env"
```

Edit the external file manually so it contains real local paths:

```text
MELLOW_YOUTUBE_EXPECTED_CHANNEL_ID=UC_REPLACE_WITH_TARGET_CHANNEL_ID
MELLOW_YOUTUBE_VIDEO_ID=VIDEO_REPLACE_AFTER_PRIVATE_UPLOAD
MELLOW_YOUTUBE_CLIENT_SECRETS=/absolute/path/outside/repo/client_secret.json
MELLOW_YOUTUBE_TOKEN_CACHE=/absolute/path/outside/repo/youtube-token.json
```

The helpers refuse env files inside this repo. The env file stores reusable channel-level local paths, target channel ID, and optionally the private video ID for the current thumbnail follow-up; the OAuth client secret JSON and generated token cache must also stay outside this repo.

## 3. Execution Command Shape

Dry-run inspection remains the default:

```bash
python3 scripts/youtube_api_video_upload.py --expected-channel-id UC_REPLACE_WITH_TARGET_CHANNEL_ID
```

Dry-run through the external env file:

```bash
python3 scripts/youtube_api_video_upload.py \
  --env-file "$HOME/.config/mellow-longplay/youtube-upload/channel.env"
```

Execution under this open gate requires all three user-provided inputs:

```bash
python3 scripts/youtube_api_video_upload.py \
  --execute \
  --env-file "$HOME/.config/mellow-longplay/youtube-upload/channel.env"
```

For future Mellow Longplay videos, reuse the same env file and pass episode-specific paths explicitly:

```bash
python3 scripts/youtube_api_video_upload.py \
  --env-file "$HOME/.config/mellow-longplay/youtube-upload/channel.env" \
  --episode-id s01e02-example \
  --video candidates/s01e02-example/render/final.mp4 \
  --resource-json channel/episodes/s01e02-example/source/youtube-video-resource.json \
  --metadata-source channel/episodes/s01e02-example/source/youtube-api-video-upload-package.md
```

Create or refresh the local thumbnail JPEG from the selected `G.png` background:

```bash
python3 scripts/create_s01e01_thumbnail.py
```

Thumbnail dry-run after a private video ID exists:

```bash
python3 scripts/youtube_api_thumbnail.py \
  --expected-channel-id UC_REPLACE_WITH_TARGET_CHANNEL_ID \
  --video-id VIDEO_REPLACE_AFTER_PRIVATE_UPLOAD
```

Thumbnail execution under this gate requires expected channel ID, video ID, OAuth client secrets path, and token-cache path outside repo:

```bash
python3 scripts/youtube_api_thumbnail.py \
  --execute \
  --env-file "$HOME/.config/mellow-longplay/youtube-upload/channel.env"
```

Do not paste secrets into chat. Do not place the OAuth client secrets file or token cache anywhere under this repository.

## 4. Current Verdict

```text
Verdict: oauth_api_execution_gate_open_private_video_upload_plus_thumbnail_followup
Allowed API calls: channels.list(mine=true), videos.insert(private), thumbnails.set after private video ID exists
Upload target: render-05 MP4 only
Caption upload: blocked because subtitles are burned in
Thumbnail upload: selected local JPEG derivative from G.png only
Public release: not passed
Credential/account storage in repo: blocked
```
