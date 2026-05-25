# S01E01 Release Decision Plan — After-School First Love Longplay

Status: release decision planning gate open / private API video uploaded and selected thumbnail set / public release blocked  
Episode: `s01e01-campus-cafe-longplay`  
Opened: 2026-05-25

## 0. Boundary

This gate is a release decision planning surface. It had a linked narrow OAuth/API execution gate for one private `videos.insert` upload after channel verification plus one thumbnail-only `thumbnails.set` follow-up after a private video ID existed. That bounded private video plus selected-thumbnail execution is now recorded; this still does not approve public publishing, scheduling, analytics, provider/browser/account actions beyond the recorded YouTube Data API execution, credentials or tokens stored in repo, Content ID action, public release readiness, or positive rights/platform claims.

Do not describe the episode, render, audio, visual, sidecars, or channel as `copyright-free`, `royalty-free`, `Content ID-safe`, `monetization-safe`, `platform-safe`, `exclusive`, `upload-ready`, or `publish-ready` except as blocked/caution language.

## 1. Current Evidence Snapshot

| Area | Current evidence | Status |
|---|---|---|
| Episode state | `manifest.json` and `reviews/current-state.md` now record this source-only release decision planning gate. | planning open |
| Local QA render | `candidates/s01e01-campus-cafe-longplay/render/future-local-render-05/video/s01e01-campus-cafe-longplay.v6-subtitled-1080p24-qa.mp4` | user-approved local QA only |
| Render format | Render-05 QA records `2503.28s` / `41:43.28`, `1920x1080`, `24fps`, H.264/AAC, clean decode, 13 resumable segments, and 7 sampled snapshots. | mechanical QA passed |
| Subtitle sidecars | Authoritative source sidecars live in `subtitles/`; render-05 copied `.srt` / `.vtt` byte-match source, include 598 cues, no overlaps, no gap cues, max line length 37, and Track 1 cue 58 corrected. | mechanical QA passed |
| Audio/content QA | Selected audio passed user human listening, supplemental lyric-anchor spot-check, and the `41:31.28` content duration decision. Track 13 opening dialogue caveat remains recorded because selected audio begins at Verse 1. | source/local QA accepted |
| Visual QA | V6 visual direction is user-passed source-only; render-05 carries forward render-04/V6 visual revisions and is user-approved as local QA output. | local QA accepted |
| Metadata/disclosure | `source/metadata.md` has a listener-facing title, description, AI-assisted disclosure wording, chapter display draft, and tag policy. `source/youtube-api-video-upload-package.md` packaged those fields for the private API `videos.insert` gate with channel-id verification and no caption upload; `source/youtube-api-thumbnail-upload-package.md` records the selected thumbnail follow-up. | private API video and thumbnail follow-up completed / public release blocked |
| Private-video title note | User reported the current private YouTube title is `『 After-School First Love Longplay 』| Soft Cozy Vocals for Study & Coffee Breaks` and had already been corrected outside this repo. | recorded note only / no metadata API mutation by this repo |
| Provenance | `reviews/local-provenance-evidence.md` records user-reported non-secret facts: selected audio candidates from Suno v5.5 in May 2026 and visual background from ChatGPT image in May 2026, with no account state stored. | source evidence only |
| Internal readiness | `reviews/episode-production-worksheet.md` remains `96/100`. | no release/platform approval |

## 2. Required Release Decision Checks

These checks must be resolved before any future release decision can pass.

| Check | Required evidence / owner | Current state |
|---|---|---|
| Final local asset selection | User confirms the exact render-05 MP4, source sidecars, title, description, and chapter text are the intended public inputs. | pending decision |
| Final metadata/disclosure review | Source draft must be re-read against the final selected assets and current platform wording expectations. | pending decision |
| Current public policy review | Current YouTube/public platform rules for AI-assisted or synthetic content disclosure, music/content policy, metadata, and child/minor-safe presentation must be reviewed from official public sources before any release pass. | pending / no web or account check performed in this gate |
| Account-specific constraints | User must check channel/account-specific status, upload limits, eligibility, warnings, strikes, monetization state, disclosure UI, and feature availability manually. No credentials, account IDs, screenshots, cookies, exports, or private account state should be stored here. | pending / user-owned manual check only |
| Provenance/risk acceptance | User decides whether the recorded non-secret provenance and local QA are enough for a manual release path, while accepting that this project makes no rights/platform-safety guarantees. | pending decision |
| Manual rollback owner | If a future manual upload is approved, the user remains owner for privacy changes, takedown/delete/unlist, metadata edits, and comment/analytics review. | pending decision |
| No-store hygiene | Repo must not gain credentials, OAuth tokens, browser profiles, account state, analytics exports, raw provider outputs, or tracked candidate media. | pass so far |
| API video and thumbnail execution gate | `videos.insert` resource, `thumbnails.set` thumbnail follow-up, channel-id verification rule, helper execution guards, external env-file workflow, and no-caption API boundary were used for the bounded private video and selected thumbnail execution. Credentials/tokens remain outside repo. | completed for private video ID 4pOLXPMQO5g / no public release |

## 3. Decision Options For The Next Review

| Option | Meaning | What it would allow later |
|---|---|---|
| Hold release | Keep render-05 as local QA only and do not prepare public package steps. | No new actions. |
| Prepare source-only API video upload package | Create a repo-source `videos.insert` metadata package and dry-run helper with channel-id verification, still with no OAuth/API/account action. | Prepared source-only after user selected API video-only route. |
| OAuth/API execution recorded | User explicitly accepted the private API route. The bounded execution recorded one private `videos.insert` upload to a verified expected channel ID and one `thumbnails.set` follow-up for the selected local JPEG. | Completed for the bounded private route; credentials and tokens stay outside the repo; public release remains blocked. |

Recommended default after the private upload and selected thumbnail follow-up: keep the video private until the remaining policy/account/checks/provenance/rollback review is resolved. Public release remains blocked.

## 4. Stop Conditions

Stop and ask before continuing if any of these appear:

- any request to upload outside the approved private video plus thumbnail API gate, publish, schedule, delete, edit YouTube Studio, use browser automation, fetch analytics, mutate an account, or call API methods beyond `channels.list(mine=true)`, `videos.insert(private)`, and `thumbnails.set` for the selected local JPEG;
- any request to create credentials, cookies, browser profiles, API keys, account IDs, or private account-state files;
- any claim that the episode is rights-safe, platform-safe, monetization-safe, Content ID-safe, upload-ready, publish-ready, exclusive, royalty-free, or copyright-free;
- any new or revised render/export, extra thumbnail variant, bumper media, sidecar text/timing change, public metadata package, or candidate media output without a separate explicit gate;
- any unresolved mismatch between render-05, source sidecars, title/description, provenance, or policy/account checks;
- any user concern from final human watch/listen review that changes asset selection or disclosure.

## 5. Current Verdict

```text
Verdict: oauth_api_private_video_uploaded_selected_thumbnail_set_public_release_blocked
Scope: release planning plus recorded one private YouTube Data API videos.insert execution after render-05 local QA approval plus one thumbnails.set follow-up for the selected local JPEG
Current local QA output: render-05 user-approved local QA only
Readiness score: remains 96/100
Release decision: public release not passed
API package: source/youtube-api-video-upload-package.md and source/youtube-api-thumbnail-upload-package.md prepared and bounded execution recorded with external env-file workflow
Pending: final asset selection decision, final metadata/disclosure review, current public platform policy review, account-specific channel and upload-limit check, provenance/risk acceptance, rollback owner
Still blocked: public publish/schedule, provider/browser actions, analytics, Content ID action, credentials/account-state storage in repo, caption upload, playlist/comments/account edits, additional media/render/package outputs or thumbnail variants, and positive rights/platform claims
```
