# S01E01 YouTube API Thumbnail Upload Package — After-School First Love Longplay

Status: OAuth/API execution gate open / thumbnail-only follow-up after private video ID / public release not passed  
Episode: `s01e01-campus-cafe-longplay`  
Prepared: 2026-05-25

## 0. Boundary

This file records the narrow thumbnail follow-up for S01E01 after the local thumbnail derivative was created from the accepted `G.png` visual background. It approves only a future YouTube Data API `thumbnails.set` call for an existing private S01E01 video ID, after authenticated channel verification succeeds and after OAuth client secrets/token-cache paths are supplied outside this repo.

This does not approve a new video upload by this helper, public publishing, scheduling, visibility mutation after upload, captions, analytics, account edits, playlist edits, comments, Content ID action, credentials or tokens stored in repo, private account-state storage, extra thumbnail variants, browser automation, or positive rights/platform claims.

The allowed API action for this package is only:

```text
channels.list(mine=true) -> verify authenticated channel ID
thumbnails.set -> upload the selected local JPEG for the provided private S01E01 video ID
```

The private video upload remains handled by `source/youtube-api-video-upload-package.md` and `scripts/youtube_api_video_upload.py`. The thumbnail helper must not call `videos.insert`.

Do not store OAuth client secrets, OAuth tokens, cookies, browser profiles, private analytics exports, account IDs, screenshots of private account state, or generated account-state files in this repo.

Do not describe this episode, render, audio, visual, sidecars, thumbnail, or channel as `copyright-free`, `royalty-free`, `Content ID-safe`, `monetization-safe`, `platform-safe`, `exclusive`, `upload-ready`, or `publish-ready` except as blocked/caution language.

## 1. Source Inputs

| Item | Source path / value | Notes |
|---|---|---|
| Thumbnail candidate | `candidates/s01e01-campus-cafe-longplay/thumbnail/s01e01-campus-cafe-longplay.thumbnail-1280x720.jpg` | Local JPEG derivative from the accepted `G.png` background; `1280x720`; `227005` bytes at creation. |
| Thumbnail generator | `scripts/create_s01e01_thumbnail.py` | Local-only PIL composition from `G.png`; no provider/browser/API/account action. |
| Thumbnail API helper | `scripts/youtube_api_thumbnail.py` | Channel-level dry-run default helper; refuses execution without channel ID, video ID, and OAuth path guards and accepts per-video thumbnail paths. |
| Video ID | external value only | Use the private video ID returned by the guarded `videos.insert` call or supplied by the user. Do not store private account state here. |
| API env template | `channel/templates/youtube-api-upload-env.example` | Channel-level placeholder only; real env file must stay outside repo and may include `MELLOW_YOUTUBE_VIDEO_ID`. |

## 2. Channel Verification Rule

The helper must verify the authenticated channel before any `thumbnails.set` call:

```text
1. Call channels.list(part="id,snippet", mine=true).
2. Require exactly one channel in the response.
3. Compare response id against a user-provided expected channel ID.
4. Abort before thumbnail upload if the expected channel ID is missing or mismatched.
```

The expected channel ID and video ID are intentionally supplied at execution time. If the user treats either value as private, keep it outside the repo and pass it only through CLI flags or an external env file.

## 3. Helper Behavior

Dry-run default:

```bash
python3 scripts/youtube_api_thumbnail.py \
  --expected-channel-id UC_REPLACE_WITH_TARGET_CHANNEL_ID \
  --video-id VIDEO_REPLACE_AFTER_PRIVATE_UPLOAD
```

External env-file execution mode under this gate:

```bash
python3 scripts/youtube_api_thumbnail.py \
  --execute \
  --env-file "$HOME/.config/mellow-longplay/youtube-upload/channel.env"
```

Direct flag execution mode under this gate:

```bash
python3 scripts/youtube_api_thumbnail.py \
  --execute \
  --expected-channel-id UC_REPLACE_WITH_TARGET_CHANNEL_ID \
  --video-id VIDEO_REPLACE_AFTER_PRIVATE_UPLOAD \
  --client-secrets /path/outside/repo/client_secret.json \
  --token-cache /path/outside/repo/youtube-token.json
```

Execution guards:

- Refuse `--execute` without `--expected-channel-id`.
- Refuse `--execute` without `--video-id`.
- Refuse `--env-file` paths inside this repository.
- Refuse OAuth client secrets or token-cache paths inside this repository.
- Verify the authenticated channel ID before `thumbnails.set`.
- Use the selected local JPEG thumbnail only unless a new explicit gate changes the asset.
- Do not call `videos.insert`, `captions.insert`, playlist, comments, analytics, Content ID, publish, schedule, unlist, delete, or metadata-update operations from this helper.

## 4. Execution Gate Packet

```text
Scope: one S01E01 thumbnails.set upload for the selected local JPEG after a private video ID exists
Mode: OAuth/API execution gate open for thumbnail-only follow-up
Allowed operations: channels.list(mine=true), thumbnails.set
Required user inputs at execution time: expected channel ID, video ID, OAuth client secrets path outside repo, token-cache path outside repo; may be supplied via an external env file
Credential storage: outside repo only; do not commit, copy, summarize, screenshot, or store tokens/account state here
Blocked operations: videos.insert from this helper, public publish, schedule, visibility update, captions.insert, playlist action, comments, analytics, Content ID, browser automation, account edits, metadata update after upload
Stop triggers: channel ID mismatch, missing expected channel ID, missing video ID, OAuth paths inside repo, missing local thumbnail file, API project/account restriction, YouTube checks/policy/copyright notice, user concern changing asset or metadata selection
```

## 5. Current Verdict

```text
Verdict: oauth_api_thumbnail_followup_gate_open_public_release_not_passed
Scope: thumbnail-only YouTube Data API thumbnails.set execution after channel verification and after a private S01E01 video ID exists
Current local thumbnail: selected JPEG derivative from G.png under candidates/s01e01-campus-cafe-longplay/thumbnail/
Channel safety: helper must verify authenticated channel id before thumbnails.set
Allowed after user supplies execution inputs: OAuth flow and one thumbnails.set call to the verified expected channel context for the provided private S01E01 video ID
Still blocked: public publish schedule Studio browser analytics Content ID credentials or tokens in repo account-state storage caption upload playlist comments metadata update after upload extra thumbnail variants and positive rights/platform claims
```
