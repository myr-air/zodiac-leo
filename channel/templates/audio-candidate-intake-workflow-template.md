# Mellow Longplay Local Audio Candidate Intake Workflow Template

Status: reusable workflow / source-only / three-HIL fastlane compatible
Updated: 2026-05-27

## 0. Boundary

Use this only after HIL-2 (`generated/supplied media exists; continue to video`) or after the user explicitly opens a local audio candidate intake gate and supplies real local files. This workflow does not approve provider/browser/API/account action, upload/publish, Content ID action, rights/platform-safety claims, or release readiness.

Candidate media stays ignored local evidence under `candidates/`. Durable facts go in review docs and tracking CSVs only.

## 1. Gate Preconditions

- HIL-2 is recorded for the episode, or the user explicitly opens the exact episode audio candidate intake gate.
- Current source packet still matches `manifest.json`, `source/songs.md`, `source/prompt-pack.md`, and current review docs.
- No lyric/title/prompt/vocal policy/provider/upload intent has changed without re-review.
- Files are local user-supplied media; do not fetch provider URLs, screenshots, cookies, browser state, account exports, or credentials.
- Provider/model/date/account facts are recorded only if known, non-private, and user-supplied. Otherwise use `unknown_user_supplied`.

## 2. Expected File Intake Pattern

For a two-variant pass per 13-track episode, raw files may arrive as title-named pairs:

```text
candidates/<episode-id>/audio/<Title>.wav
candidates/<episode-id>/audio/<Title> (1).wav
```

Map them consistently:

- first file without `(1)` -> `c01` / variant `A`
- file with `(1)` -> `c02` / variant `B`

After selection, organize without changing audio content:

```text
candidates/<episode-id>/audio/selected/aud-t##_c##--<slug>.wav
candidates/<episode-id>/audio/pool/aud-t##_c##--<slug>.wav
```

Never reserve IDs before real files exist.

## 3. Local Technical QA

Use local tools first, before any external supplemental review:

- `ffprobe`: duration, container/codec, sample rate, channel count, bitrate/bit depth.
- `ffmpeg` `volumedetect`: mean volume, max volume, rough clipping/headroom check.
- Inventory completeness: expected track count x variants, missing/extra titles, duplicate names, unexpected formats.

Record only compact results, not raw logs. Treat technical picks as fallback only; under the three-HIL fastlane they must be carried into the system's intensive render review and HIL-3 final-video decision rather than causing a separate planned HIL prompt.

## 4. Optional Gemini Supplemental A/B Listening

Use only when the user explicitly allows Gemini/external supplemental audio review. Keep it advisory and source-only.

Known working model path from S01E01:

- `gemini-3-flash-preview` can listen to short/compressed local audio previews through Gemini CLI.

Observed caveats:

- `gemini-3-flash-preview`, `gemini-3.1-pro-preview`, and `gemini-3.1-flash-lite-preview` are available model IDs in this environment, but output may be blank for some longer A/B prompts.
- `gemini-2.5-flash` reported it could not directly listen in the same workflow.
- Files ignored by `.gitignore` may be blocked from direct Gemini file reading. If needed, create temporary compressed preview copies inside the workspace, use them for review, then delete them before final state.

Suggested safe Gemini prompt shape:

```text
Compare audio A and B for Mellow Longplay Track ## - <title>.
A: @"<temp>/t##_A.mp3"
B: @"<temp>/t##_B.mp3"
Pick A or B for SELECTED; other goes POOL. Judge cozy chill vocal longplay fit, lyric clarity, mix quality, artifacts, no harsh genre break. No rights/upload claims.
Return one compact line or strict JSON: selected, confidence, reason, pool_reason, blockers.
```

Gemini output must be recorded as advisory only. Do not store raw private transcripts or credentials.

## 5. Selection Rules

Select one draft candidate per track, then pool the alternate. Prefer:

- cozy chill longplay fit;
- comfortable vocal and English-first lyric clarity;
- fewer obvious artifacts, timing issues, harshness, clipping, silence, or genre breaks;
- episode spine compliance, including reserved variation slots;
- duration/sequence fit.

If Gemini is unavailable or blank, use local technical fallback plus mark `needs_final_video_review_source_only`; do not stop for a separate planned listening HIL unless audio evidence is contradictory or risky.

## 6. Required Durable Sync

After organizing selected/pool candidates, update:

- `reviews/audio-candidate-intake.md`: selected/pool map, inventory, technical QA summary, Gemini caveat, still-blocked actions.
- `reviews/candidate-intake-checklist.md`: track coverage statuses and candidate IDs.
- `reviews/current-state.md`: selected draft status and HIL-3/final-video-review carry-forward.
- `manifest.json`: audio candidate state only.
- `tracking/assets.csv`: candidate asset rows with actual local paths.
- `tracking/provenance.csv`: `unknown_user_supplied` or non-private known facts only.
- `tracking/status.csv`: candidate intake status and next action.
- `tracking/decisions.csv`: selection/pool decision.
- `KNOWLEDGE.md`: compact current-state summary if project-level state changes.

Run `bash scripts/dev-python.sh -m json.tool <manifest>` and `bash scripts/verify-standalone.sh` after sync.

## 7. Exit State

Allowed exit statuses:

- `selected_draft_needs_final_video_review_source_only`
- `selected_draft_system_review_passed_final_video_approval_pending_source_only`
- `selected_draft_human_listen_passed_needs_lyric_alignment_duration_source_only`
- `selected_draft_human_listen_lyric_alignment_passed_needs_duration_decision_source_only`
- `selected_draft_human_listen_lyric_anchor_duration_accepted_source_only`
- `needs_lyric_alignment_spot_check_source_only`
- `needs_regeneration_or_pool_swap_source_only`
- `quarantine_rejected`

Still blocked unless the relevant HIL/gate approves: render/export before HIL-2, upload/publish, scheduling, analytics, Content ID action, rights/platform-safety claims, and release readiness. Final video approval happens at HIL-3, not inside audio intake.
