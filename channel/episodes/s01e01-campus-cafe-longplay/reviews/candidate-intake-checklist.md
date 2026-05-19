# S01E01 Candidate Intake Checklist — After-School First Love Longplay

Status: intake_recorded_human_listen_lyric_anchor_duration_accepted_source_only
Episode: `s01e01-campus-cafe-longplay`  
Prepared date: 2026-05-18

## 0. Boundary

This checklist prepares a future manual candidate-intake gate only. It does not approve Suno/provider use, browser automation, API calls, generated media, downloads, candidate files, render/export, upload, publishing, account mutation, Content ID action, or positive rights/platform claims.

Do not create candidate IDs, file paths, generation dates, provider facts, QA results, or acceptance decisions until real user-supplied local files exist after a separate explicit gate.

## 1. Gate-Open Preconditions

Before any candidate is logged, confirm all items below are true:

- [x] User explicitly approves the exact manual provider/candidate-intake gate for this episode.
- [x] The current source packet still matches `manifest.json`, `source/songs.md`, and `source/prompt-pack.md`.
- [x] Any lyric, title, prompt, exclude, vocal policy, provider/model, disclosure, or upload-intent change has been re-reviewed first.
- [x] The user supplies real local files or a real local file inventory; no provider/browser/API fetching is performed here.
- [x] Candidate files remain local evidence under ignored candidate storage; durable facts go only into reviews and tracking CSVs.
- [x] No credentials, cookies, account IDs, account emails, private analytics, browser profiles, or raw account exports are stored.
- [x] Provider/model/mode/date facts are recorded only if known, non-private, and supplied by the user.
- [x] No claim is made that any candidate is exclusive, rights-cleared, platform-safe, upload-ready, or publish-ready.

## 2. Allowed Intake Inputs After Approval

| Input | Allowed? | Intake rule |
|---|---:|---|
| User-supplied local audio candidate files | yes after gate | Log only after files exist. |
| User-supplied local still-image candidate files | yes after gate | Log only after files exist. |
| User-supplied generation notes | yes after gate | Store compact non-private facts only. |
| Provider URLs, cookies, account exports, screenshots, browser state | no | Do not request or store. |
| Rendered video exports | no | Future render/export gate only. |
| Upload or publish metadata actions | no | Future release decision gate only. |

## 3. Candidate ID Pattern

Assign IDs only after a real file exists:

- Audio pattern: `aud-t##_c##` for a concrete track file, for example Track 01 candidate 01.
- Visual pattern: `vis-c##` for a concrete still-image file.
- Render pattern: not assigned in Candidate Intake; render/export remains blocked.

Never reserve or pre-fill IDs for missing files.

## 4. Audio Candidate Intake Sheet

Use one row per real audio file. Mark unknowns as `unknown`; do not guess.

| Field | Required? | Rule |
|---|---:|---|
| Candidate ID | yes | Assign only after file exists. |
| Track number and title | yes | Must match `source/songs.md`. |
| Local path | yes | Actual local path only. |
| File format | yes | Record observed extension/container. |
| Duration | yes | Record observed duration if available. |
| Source lyric version | yes | Should point to revised `source/songs.md`. |
| Prompt pack version | yes | Should point to `source/prompt-pack.md`. |
| Provider/model/mode/date | if known | Non-private user-supplied facts only. |
| Account boundary | if relevant | Use non-private wording such as `user private account not recorded`. |
| Immediate blocker flags | yes | Record obvious blocker or `none_observed_at_intake`. |
| Next status | yes | Use `needs_audio_qa`, `needs_human_listen`, `quarantine_rejected`, or `needs_regeneration`. |

### Audio Immediate Blockers

Quarantine or reject at intake if any are obvious:

- Named-artist, known-song, real-person voice, celebrity likeness, or competitor-channel imitation.
- Wrong title, wrong track order, wrong or missing lyrics, unsupported ad-libs, or non-English-first output.
- Sexualized teen framing, adult/minor romance, teacher/student romance, childlike vocal delivery, or inappropriate adult framing.
- Harsh genre shift: trap, aggressive rap, EDM drop, distorted rock, bombastic choir, or busy jazz soloing.
- Track 4 is not the only piano-forward color song.
- Track 9 is not the only soft-sax accent song, or sax dominates the vocal.
- Brand names, logos, film/game/TV references, claims about rights/platform safety, or release-readiness wording.
- Severe artifacts: clipping, garbled vocal, unusable timing, broken file, or obvious silence.

## 5. Visual Candidate Intake Sheet

Use one row per real still-image file. Mark unknowns as `unknown`; do not guess.

| Field | Required? | Rule |
|---|---:|---|
| Candidate ID | yes | Assign only after file exists. |
| Local path | yes | Actual local path only. |
| File format and dimensions | yes | Record observed facts only. |
| Source visual version | yes | Should point to `source/visual.md`. |
| Generation notes/provider facts | if known | Non-private user-supplied facts only. |
| Safe-zone first look | yes | Intake flag only; real crop/overlay review later. |
| Immediate blocker flags | yes | Record obvious blocker or `none_observed_at_intake`. |
| Next status | yes | Use `needs_visual_review`, `quarantine_rejected`, or `needs_regeneration`. |

### Visual Immediate Blockers

Quarantine or reject at intake if any are obvious:

- Real school/cafe names, logos, brand marks, readable private text, or identifiable real-person likeness.
- Childlike subject, sexualized teen framing, adult/minor implication, teacher/student romance, revealing school uniform framing, celebrity likeness, or exact face copying.
- Provider reference-image use that was not separately approved.
- Heavy text baked into the image, unsafe crop for title/subtitle overlays, or unusable aspect ratio.
- Visual style that breaks the warm PG after-school first-love source direction.
- Rights/platform/upload/publish readiness claims embedded in notes or file labels.

## 6. Track Coverage Checklist

Do not fill candidate IDs here until files exist.

| Track | Title | Audio intake status | Notes |
|---:|---|---|---|
| 1 | Margin Notes at Table Three | human_listen_lyric_anchor_duration_accepted_source_only | Selected `aud-t01_c02`; pool `aud-t01_c01`; long track accepted within 41:31 source-only duration. |
| 2 | Two Lids, One Tray | human_listen_lyric_anchor_duration_accepted_source_only | Selected `aud-t02_c01`; pool `aud-t02_c02`. |
| 3 | Borrowed Eraser, Written Name | human_listen_lyric_anchor_duration_accepted_source_only | Selected `aud-t03_c01`; pool `aud-t03_c02`. |
| 4 | Checkout Slip at Chapter Nine | human_listen_lyric_anchor_duration_accepted_source_only | Selected `aud-t04_c01`; pool `aud-t04_c02`. |
| 5 | Steam on the Glass Door | human_listen_lyric_anchor_duration_accepted_source_only | Selected `aud-t05_c01`; pool `aud-t05_c02`. |
| 6 | Peach Can at B4 | human_listen_lyric_anchor_duration_accepted_source_only | Selected `aud-t06_c02`; pool `aud-t06_c01`. |
| 7 | Green Dot on Your Schedule | human_listen_lyric_anchor_duration_accepted_source_only | Selected `aud-t07_c01`; pool `aud-t07_c02`. |
| 8 | Cushion Seat, Charging Cord | human_listen_lyric_anchor_duration_accepted_source_only | Selected `aud-t08_c01`; pool `aud-t08_c02`; short track accepted within 41:31 source-only sequence. |
| 9 | Crosswalk Stripes Before Six | human_listen_lyric_anchor_duration_accepted_source_only | Selected `aud-t09_c01`; pool `aud-t09_c02`. |
| 10 | Yellow Tag on the Umbrella Rack | human_listen_lyric_anchor_duration_accepted_source_only | Selected `aud-t10_c01`; pool `aud-t10_c02`. |
| 11 | Quiz Key in Blue Ink | human_listen_lyric_anchor_duration_accepted_source_only | Selected `aud-t11_c01`; pool `aud-t11_c02`. |
| 12 | Tray Return at 5:59 | human_listen_lyric_anchor_duration_accepted_source_only | Selected `aud-t12_c01`; pool `aud-t12_c02`. |
| 13 bonus | Latch Click at the Courtyard Gate | human_listen_lyric_anchor_duration_accepted_source_only | Selected `aud-t13_c01`; pool `aud-t13_c02`; opening-dialogue caveat. |

## 7. Tracking Sync When Real Files Exist

For each real candidate file, update the relevant subset together:

- `tracking/assets.csv`: actual candidate asset row with real path, status, and compact notes.
- `tracking/provenance.csv`: non-private source/provider facts if known; otherwise mark `unknown_user_supplied`.
- `tracking/status.csv`: candidate-intake area status and next required review.
- `reviews/current-state.md`: current evidence summary and still-blocked actions.
- `manifest.json`: source state only if the durable episode state changes.

Do not store raw provider account data, credentials, cookies, browser state, screenshots, analytics, or large raw logs.

## 8. Intake Outcomes

Allowed Candidate Intake outcomes:

- `intake_recorded_needs_audio_qa_source_only`
- `intake_recorded_human_listen_passed_needs_lyric_alignment_duration_source_only`
- `intake_recorded_human_listen_lyric_alignment_passed_needs_duration_decision_source_only`
- `intake_recorded_human_listen_lyric_anchor_duration_accepted_source_only`
- `intake_recorded_needs_visual_review`
- `quarantine_rejected`
- `needs_regeneration`
- `needs_human_review`

Not allowed at Candidate Intake:

- release approval
- upload or publish approval
- render/export approval
- final quality pass
- rights/platform-safety assurance
- Content ID or monetization claims

## 9. Exit Criteria For Candidate Intake

Candidate Intake can close only when real files exist and the review docs/tracking CSVs accurately show:

- all logged candidates have actual paths and non-invented provenance status;
- blockers are recorded without overclaiming safety;
- audio files needing review are routed to objective audio QA and human listening;
- visual files needing review are routed to visual safe-zone/crop review;
- render/export and release gates remain blocked unless separately approved later.

Current state: 26 user-supplied local WAV candidates exist. A source-only selected draft set and pool set are recorded in `reviews/audio-candidate-intake.md`; all selected candidates passed user human listening and Gemini supplemental lyric anchor spot-check, and the 41:31 duration/sequence is accepted source-only before any later gate.
