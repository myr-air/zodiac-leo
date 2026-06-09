# S01E02-CLASSROOM-WINDOW-LONGPLAY Release Decision Plan — Classroom Window Longplay

Status: release decision planning gate open / private API video uploaded / selected thumbnail set completed / public release blocked
Episode: `s01e02-classroom-window-longplay`
Prepared: 2026-05-29

## 0. Boundary

This gate is a release decision planning surface. It has a linked narrow OAuth/API execution gate for one private `videos.insert` upload after channel verification. That bounded private video execution is now recorded; this still does not approve public publishing, scheduling, analytics, provider/browser/account actions beyond the recorded YouTube Data API execution, credentials or tokens stored in repo, Content ID action, public release readiness, or positive rights/platform claims.

Do not describe the episode, render, audio, visual, sidecars, or channel as `copyright-free`, `royalty-free`, `Content ID-safe`, `monetization-safe`, `platform-safe`, `exclusive`, `upload-ready`, or `publish-ready` except as blocked/caution language.

## 1. Current Evidence Snapshot

| Area | Current evidence | Status |
|---|---|---|
| Episode state | `manifest.json` and `reviews/current-state.md` now record this private video upload. | upload complete |
| Local QA render | `candidates/s01e02-classroom-window-longplay/render/local-render-02/video/s01e02-classroom-window-longplay.local-render-02-draft-subtitled-1080p24-qa.mp4` | user-approved local render |
| Render format | Render-02 QA records `2385.917s` container / `39:45.96` WAV timeline, `1920x1080`, `24fps`, H.264/AAC, clean decode, 13 segments, and 6 sampled snapshots. | mechanical QA passed |
| Subtitle sidecars | Authoritative source sidecars live in `subtitles/`; timing repaired with stable-ts Dynamic Vocal Alignment. | mechanical QA passed |
| Audio/content QA | Selected audio passed user human listening and timeline gaps. | source/local QA accepted |
| Visual QA | Watercolor night classroom layout is user-passed and approved. | local QA accepted |
| Metadata/disclosure | Request body for `videos.insert` validates `privacyStatus: private` and no captions/thumbnail fields. | private API video completed / public release blocked |
| Private-video ID | Private YouTube video ID: `KZNjs0Z7-Pw` | uploaded |
| Thumbnail upload | Selected thumbnail JPEG v4 uploaded via thumbnails.set | upload complete |

## 2. Required Release Decision Checks

These checks must be resolved before any future public release decision can pass.

| Check | Required evidence / owner | Current state |
|---|---|---|
| Final local asset selection | User confirms the exact render-02 MP4, source sidecars, title, description, and chapter text are the intended public inputs. | pass |
| Final metadata/disclosure review | Source draft must be re-read against the final selected assets and current platform wording expectations. | pass |
| Current public policy review | Current YouTube/public platform rules for AI-assisted or synthetic content disclosure, music/content policy, metadata, and child/minor-safe presentation must be reviewed from official public sources before any release pass. | pending / no web or account check performed in this gate |
| Account-specific constraints | User must check channel/account-specific status, upload limits, eligibility, warnings, strikes, monetization state, disclosure UI, and feature availability manually. No credentials, account IDs, screenshots, cookies, exports, or private account state should be stored here. | pending / user-owned manual check only |
| Provenance/risk acceptance | User decides whether the recorded non-secret provenance and local QA are enough for a manual release path, while accepting that this project makes no rights/platform-safety guarantees. | pass |
| Manual rollback owner | If a future manual upload is approved, the user remains owner for privacy changes, takedown/delete/unlist, metadata edits, and comment/analytics review. | pass |
| No-store hygiene | Repo must not gain credentials, OAuth tokens, browser profiles, account state, analytics exports, raw provider outputs, or tracked candidate media. | pass so far |
| API video & thumbnail execution gates | `videos.insert` resource, channel-id verification rule, helper execution guards, external env-file workflow, and `thumbnails.set` execution were used for the bounded private execution. Credentials/tokens remain outside repo. | completed for private video ID KZNjs0Z7-Pw and custom thumbnail / no public release |

## 3. Decision Options For The Next Review

| Option | Meaning | What it would allow later |
|---|---|---|
| Hold release | Keep video as private only and do not prepare public publish steps. | Current status. |
| Prepare thumbnail execution | Create a repo-source `thumbnails.set` metadata package once a thumbnail is selected or generated. | Bounded thumbnail upload execution. |

## 4. Stop Conditions

Stop and ask before continuing if any of these appear:

- any request to upload outside the approved private video API gate, publish, schedule, delete, edit YouTube Studio, use browser automation, fetch analytics, mutate an account, or call API methods beyond `channels.list(mine=true)` and `videos.insert(private)`;
- any request to create credentials, cookies, browser profiles, API keys, account IDs, or private account-state files;
- any claim that the episode is rights-safe, platform-safe, monetization-safe, Content ID-safe, upload-ready, publish-ready, exclusive, royalty-free, or copyright-free;
- any user concern from final human watch/listen review that changes asset selection or disclosure.

## 5. Current Verdict

```text
Verdict: oauth_api_private_video_uploaded_selected_thumbnail_set_public_release_blocked
Scope: release planning plus recorded private YouTube Data API videos.insert and thumbnails.set executions after render-02 local QA approval
Current local QA output: render-02 user-approved
Readiness score: remains 98/100
Release decision: public release not passed
API video ID: KZNjs0Z7-Pw
Still blocked: public publish/schedule, provider/browser actions, analytics, Content ID action, credentials/account-state storage in repo, caption upload, playlist/comments/account edits, additional media/render/package outputs or thumbnail variants, and positive rights/platform claims
```
