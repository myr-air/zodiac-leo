# Mellow Longplay Knowledge Contract

Status: core active
Updated: 2026-06-09

## Purpose

This repository is the single core source-first system for one cozy chill vocal longplay channel: `Mellow Longplay`.

There is no separate older active system. EP1-EP4 are episode packets inside the same core; future episodes use the same `channel/episodes/<episode-id>/` structure and the four-HIL fastlane in `docs/workflow-map.md`.

## Current Episode State

- `s01e01-campus-cafe-longplay` — Season 1 Week 1 `After-School First Love Longplay`.
  - Evidence state: source packet, final local render-05 QA, final burned-in subtitle sidecars, private YouTube Data API video upload, selected thumbnail set, and manual public release are recorded. Post-release Thai pronoun and spoken style subtitle fix applied on 2026-06-12.
  - Current status: manual public release completed for video ID `4pOLXPMQO5g`; do not claim platform safety, Content ID safety, monetization safety, or rights safety.
  - Truth paths: `channel/episodes/s01e01-campus-cafe-longplay/manifest.json`, `reviews/current-state.md`, `reviews/youtube-api-execution-gate.md`, `reviews/release-decision-plan.md`, `source/youtube-api-video-upload-package.md`, `source/youtube-api-thumbnail-upload-package.md`, `source/youtube-video-resource.json`, and `tracking/*.csv`.
- `s01e02-classroom-window-longplay` — Season 1 Week 2 `Classroom Window Longplay`.
  - Evidence state: source packet, selected c01 audio, `vis-c01` visual, authoritative stable-ts subtitles, render-02 local QA, final-video approval, private YouTube Data API video upload, selected thumbnail set, and manual public release are recorded. Post-release Thai pronoun and spoken style subtitle fix applied on 2026-06-12.
  - Current status: manual public release completed for video ID `KZNjs0Z7-Pw`; transcript certification, Content ID, monetization/platform-safety, and rights claims remain blocked.
  - Truth paths: `channel/episodes/s01e02-classroom-window-longplay/manifest.json`, `reviews/current-state.md`, `reviews/final-video-approval.md`, `reviews/render-export-qa.md`, `reviews/agy-render-review.md`, and `tracking/*.csv`.
- `s01e03-rooftop-golden-hour-longplay` — Season 1 Week 3 `Rooftop Golden Hour Longplay`.
  - Evidence state: source packet is synced; selected c01 audio, `vis-c01` visual, authoritative subtitles timed using stable-ts, render-02 local QA, final-video user approval for upload, YouTube Data API video upload, custom thumbnail set, and top-level comment are completed and recorded. The requested top-level comment initially failed with a 403 response, then succeeded after retry when the video was observed as public/processed; comment pinning remains pending/manual. Post-release Thai pronoun and spoken style subtitle fix applied on 2026-06-12.
  - Current status: EP3 is marked closed as manual public release complete with pin pending (video ID: `2P6fPs7NB0E`, comment ID: `Ugw3CXuFnYeKOp4TNi54AaABAg`); remaining release/account actions remain blocked pending explicit gates.
  - Truth paths: `channel/episodes/s01e03-rooftop-golden-hour-longplay/manifest.json`, `reviews/current-state.md`, `reviews/render-export-qa.md`, `reviews/youtube-api-execution-gate.md`, `reviews/release-decision-plan.md`, `source/youtube-api-video-upload-package.md`, `source/youtube-video-resource.json`, and `tracking/*.csv`.
- `s01e04-bookstore-afternoon-longplay` — Season 1 Week 4 `Bookstore Afternoon Longplay`.
  - Evidence state: source packet is synced; selected c01 audio, `vis-c01` visual, promoted track-aligned subtitles, local render-01 after track 3 replacement, private YouTube Data API upload, selected thumbnail set, public visibility observation, and top-level comment are recorded. Post-release Thai pronoun and spoken style subtitle fix applied on 2026-06-12.
  - Current status: manual public release completed for video ID `OMjvEEAIFSU`; comment pinning, captions, playlists, analytics, Content ID, account edits, platform-safety, monetization-safety, and rights claims remain blocked pending explicit gates.
  - Truth paths: `channel/episodes/s01e04-bookstore-afternoon-longplay/manifest.json`, `reviews/current-state.md`, `reviews/release-decision-plan.md`, `source/youtube-api-video-upload-package.md`, `source/youtube-video-resource.json`, and `tracking/*.csv`.
- `s01e05-apartment-window-longplay` — Season 2 Week 5 `Apartment Window Longplay`.
  - Evidence state: Gate 1 source-only prompts, lyrics, Suno manual fields, visual prompts, metadata draft, and comment are completed, synced, and locked. All 13 c01 audio selected, vis-c01 visual selected. Subtitles generated. Local render-01 re-rendered to burn in the corrected subtitles. YouTube private upload and thumbnail completed on 2026-06-12. English captions uploaded. Thai captions upload hit quota limit (manual upload pending).
  - Current status: private upload completed for video ID `QR9h3p4C3Vg`; waiting for public release, top-level comment posting (comments disabled on private), and manual Thai caption upload.
  - Truth paths: `channel/episodes/s01e05-apartment-window-longplay/manifest.json`, `reviews/current-state.md`, `tracking/*.csv`.


## Operating Model

- Default core production flow is the four-HIL fastlane in `docs/workflow-map.md`:
  1. HIL-1: user says to make a new episode; system creates source packet, song prompts, visual prompts, metadata draft, and handoff notes.
  2. HIL-2: user says generated/supplied media exists and to continue; system intakes real files, assembles, subtitles, renders locally, and self-reviews intensely.
  3. HIL-3: user approves the exact final-video candidate for upload prep or sends point revisions.
  4. HIL-4: user approves exact final route for release execution/schedule, or requests route revisions.
- Internal gates still exist for evidence/tracking; do not ask for routine micro-approval unless there is a blocker, contradiction, or risk boundary.
- Candidate IDs/provenance require real local files or an exact provider gate. Never invent media facts.
- Final video approval is not release approval and not a rights/platform-safety claim.

## Durable Source Truth

- Channel strategy: `channel/channel.md`, `channel/roadmap.md`, `channel/signature-visual-system.md`.
- Workflow/boundary: `docs/workflow-map.md`, `docs/operating-boundary.md`, `docs/provider-platform-boundary.md`, `docs/episode-lessons.md`.
- Templates: `channel/templates/`.
- Episode truth: `channel/episodes/<episode-id>/manifest.json`, `reviews/current-state.md`, `source/`, `subtitles/`, and `tracking/*.csv`.
- Candidate media and render outputs under `candidates/` are ignored local evidence, not durable source truth.

## Carry-Forward Rules

- Use the mandatory channel image style for all future channel images: soft watercolor semi-realistic anime playlist-cover illustration / lo-fi watercolor anime poster style, soft lifelike recurring listener woman archetype with varied poses, and gold crescent-vinyl totem.
- EP03+ arrangement rule: no planned sax special color; piano is allowed; choose exactly one non-sax special instrument for exactly one song.
- Future episode slates should include several feeling/mood-led tracks, not only cafe/classroom/campus object-proof songs.
- Lyrics/source workflow must keep Episode Style & Theme Spine, Track Delta, Story + Reference Brief, structure fingerprint, strict micro-pattern gate, lexical count ledger, title/lyric relationship gate, and BPM in every `Styles` field.
- Visual/render revisions must be issue-led: name the exact audio, subtitle, visual, overlay, crop, or render problem before regenerating/rerendering.
- Subtitle quality: parenthetical non-lyric lines (`(Humming low)`, `(Vocalise)` etc.) are auto-excluded from `build_track_text` via `is_parenthetical_stage_direction()`. Gate 3 subtitle pass now requires zero duration outliers > 15 s and zero low-confidence cues (< 0.3) adjacent to Outro or instrumental-break sections. See `docs/episode-lessons.md` for full rules.

## Safety

- Block provider/browser/API/account/platform actions unless a narrow explicit gate opens the exact action.
- Keep credentials, OAuth tokens, cookies, profiles, private account state, and private analytics out of repo.
- Use forbidden terms such as `copyright-free`, `royalty-free`, `Content ID-safe`, `monetization-safe`, `platform-safe`, `upload-ready`, and `publish-ready` only as blocked/caution language.
- Do not claim transcript certification, final release readiness, public publish, Content ID status, monetization status, or rights/platform safety without exact evidence and a release gate.

## Verification

Run after structural/source/tracking/script changes:

```bash
bash scripts/dev-python.sh -m json.tool <changed-manifest-or-json>
bash scripts/dev-python.sh -m py_compile <changed-script.py>
bash scripts/verify-standalone.sh
bash scripts/run-tests.sh
```

Use `bash scripts/dev-python.sh --print` to see the selected interpreter. Do not use `rtk pytest`, bare `pytest`, or bare `python3 -m pytest` in this repo.
