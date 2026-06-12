Status: thumbnail upload completed / video ID ShWN-wK-ZNY / public release blocked
Episode: `s01e05-apartment-window-longplay`
Prepared: 2026-06-11

## 0. Boundary

This file records the narrow thumbnail upload package for S01E05 after the local thumbnail derivative was created from the accepted `vis-c01` visual background. It scopes only one YouTube Data API `thumbnails.set` call for existing S01E05 video ID `ShWN-wK-ZNY`, after authenticated channel verification succeeds and after OAuth client secrets/token-cache paths are supplied outside this repo.

This does not approve a new video upload by this helper, scheduling, visibility mutation, captions, analytics, account edits, playlist edits, comments, Content ID action, credentials or tokens stored in repo, private account-state storage, extra thumbnail variants, browser automation, or positive rights/platform claims.

The allowed API action for this package is only:

```text
channels.list(mine=true) -> verify authenticated channel ID
thumbnails.set -> upload the selected local PNG for S01E05 video ID ShWN-wK-ZNY
```

The video upload is handled by `source/youtube-api-video-upload-package.md` and `scripts/youtube_api_video_upload.py`. The thumbnail helper must not call `videos.insert`.

Do not store OAuth client secrets, OAuth tokens, cookies, browser profiles, private analytics exports, account IDs, screenshots of private account state, or generated account-state files in this repo.

Do not describe this episode, render, audio, visual, sidecars, thumbnail, or channel as `copyright-free`, `royalty-free`, `Content ID-safe`, `monetization-safe`, `platform-safe`, `exclusive`, `upload-ready`, or `publish-ready` except as blocked/caution language.

## 1. Source Inputs

| Item | Source path / value | Notes |
|---|---|---|
| Thumbnail candidate | `candidates/s01e05-apartment-window-longplay/thumbnail/s01e05-apartment-window-longplay.thumbnail-layered-premium-1280x720.png` | Local PNG derivative from the accepted `vis-c01` background; `1280x720` dimensions. |
| Thumbnail API helper | `scripts/youtube_api_thumbnail.py` | Channel-level dry-run default helper; refuses execution without channel ID, video ID, and OAuth path guards. |
| Video ID | `ShWN-wK-ZNY` | S01E05 YouTube video ID from the guarded video upload. Do not store private account state here. |
| API env template | `channel/templates/youtube-api-upload-env.example` | Channel-level placeholder only; real env file must stay outside repo. |

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
uv run --project /Users/xiivth/workspaces/zodiac/leo --with google-api-python-client --with google-auth --with google-auth-oauthlib python scripts/youtube_api_thumbnail.py \
  --env-file /Users/xiivth/.config/mellow-longplay/.secret/channel.env \
  --episode-id s01e05-apartment-window-longplay \
  --video-id ShWN-wK-ZNY \
  --thumbnail candidates/s01e05-apartment-window-longplay/thumbnail/s01e05-apartment-window-longplay.thumbnail-layered-premium-1280x720.png \
  --thumbnail-source channel/episodes/s01e05-apartment-window-longplay/source/youtube-api-thumbnail-upload-package.md
```

Execution mode:

```bash
uv run --project /Users/xiivth/workspaces/zodiac/leo --with google-api-python-client --with google-auth --with google-auth-oauthlib python scripts/youtube_api_thumbnail.py \
  --execute \
  --env-file /Users/xiivth/.config/mellow-longplay/.secret/channel.env \
  --episode-id s01e05-apartment-window-longplay \
  --video-id ShWN-wK-ZNY \
  --thumbnail candidates/s01e05-apartment-window-longplay/thumbnail/s01e05-apartment-window-longplay.thumbnail-layered-premium-1280x720.png \
  --thumbnail-source channel/episodes/s01e05-apartment-window-longplay/source/youtube-api-thumbnail-upload-package.md
```

Execution guards:

- Refuse `--execute` without `--expected-channel-id` or external env value.
- Refuse `--execute` without `--video-id`.
- Refuse `--env-file` paths inside this repository.
- Refuse OAuth client secrets or token-cache paths inside this repository.
- Verify the authenticated channel ID before `thumbnails.set`.
- Use the selected local PNG thumbnail only unless a new explicit gate changes the asset.
- Do not call `videos.insert`, `captions.insert`, playlist, comments, analytics, Content ID, publish, schedule, unlist, delete, or metadata-update operations from this helper.

## 4. Execution Gate Packet

```text
Scope: one S01E05 thumbnails.set upload for the selected local PNG after an existing YouTube video ID exists
Mode: OAuth/API execution planned for thumbnail-only follow-up
Allowed operations: channels.list(mine=true), thumbnails.set
Required user inputs at execution time: expected channel ID, video ID, OAuth client secrets path outside repo, token-cache path outside repo; may be supplied via an external env file
Credential storage: outside repo only; do not commit, copy, summarize, screenshot, or store tokens/account state here
Blocked operations: videos.insert from this helper, schedule, visibility update, captions.insert, playlist action, comments, analytics, Content ID, browser automation, account edits, metadata update after upload, extra thumbnail variants
Stop triggers: channel ID mismatch, missing expected channel ID, missing video ID, OAuth paths inside repo, missing local thumbnail file, API project/account restriction, YouTube checks/policy/copyright notice, user concern changing asset or metadata selection
```

## 5. Current Verdict

```text
Verdict: oauth_api_thumbnail_followup_completed
Scope: thumbnail-only YouTube Data API thumbnails.set execution after channel verification and after S01E05 video ID exists
Current local thumbnail: selected PNG derivative from vis-c01 under candidates/s01e05-apartment-window-longplay/thumbnail/
Execution result: thumbnails.set completed for video ID ShWN-wK-ZNY on verified channel UC4qQwe3oiykEGhL_WyVFtMg and returned youtube#thumbnailSetResponse
Still blocked: schedule Studio browser analytics Content ID credentials or tokens in repo account-state storage caption upload playlist comments metadata update after upload extra thumbnail variants and positive rights/platform claims
```
