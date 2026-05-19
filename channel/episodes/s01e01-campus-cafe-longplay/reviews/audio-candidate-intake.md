# S01E01 Audio Candidate Intake — After-School First Love Longplay

Status: selected_draft_human_listen_passed_needs_lyric_alignment_duration_source_only
Updated: 2026-05-19

## Boundary

This review records local user-supplied audio candidate intake only. It does not approve render/export, upload/publish, Content ID action, rights/platform safety, or release readiness. Candidate audio files remain ignored local evidence under `candidates/`.

## Gate And Tools

- User explicitly opened the S01E01 local audio candidate intake and technical audio QA gate.
- Local tools used: `ffprobe` and `ffmpeg` for format, duration, loudness, and peak checks.
- External supplemental review allowed by user: Gemini CLI with `gemini-3-flash-preview` for A/B listening where it returned usable output.
- Gemini output is advisory only; Mayr selection remains a source-only draft pending human listening.
- The reusable version of this method is now recorded at `channel/templates/audio-candidate-intake-workflow-template.md`.

## Inventory Summary

- Found 26 `.wav` files: 13 tracks x 2 variants.
- Organized into 13 selected draft candidates and 13 pool candidates.
- All files observed as WAV PCM s16le, 48 kHz, stereo, 16-bit.
- Local peak check found no severe clipping; max peaks sat roughly between -4.2 dB and -2.6 dB.
- Selected draft total duration: about `41:31`.
- Pool total duration: about `42:30`.
- Duration note: the selected draft is longer than the earlier 30-35 minute target and needs sequence/listening review before any render/export planning.

## Selected Draft And Pool Map

| Track | Title | Selected candidate | Duration | Selection basis | Pool candidate | Pool duration | Notes |
|---:|---|---|---:|---|---|---:|---|
| 1 | Margin Notes at Table Three | `aud-t01_c02` | 279.92s | local technical fallback | `aud-t01_c01` | 318.12s | Selected shorter variant; pool is over 5 minutes. |
| 2 | Two Lids, One Tray | `aud-t02_c01` | 225.00s | local technical fallback | `aud-t02_c02` | 277.44s | Selected tighter shorter variant. |
| 3 | Borrowed Eraser, Written Name | `aud-t03_c01` | 204.12s | local technical fallback | `aud-t03_c02` | 217.16s | Variants technically comparable; human listen recommended. |
| 4 | Checkout Slip at Chapter Nine | `aud-t04_c01` | 209.56s | Gemini selected A with high confidence | `aud-t04_c02` | 175.00s | Gemini preferred A for library-hush mellow fit. |
| 5 | Steam on the Glass Door | `aud-t05_c01` | 218.40s | local technical fallback | `aud-t05_c02` | 220.24s | Variants technically comparable; human listen recommended. |
| 6 | Peach Can at B4 | `aud-t06_c02` | 159.92s | Gemini plus local technical pick | `aud-t06_c01` | 134.60s | Gemini preferred B; A was short and less fitting. |
| 7 | Green Dot on Your Schedule | `aud-t07_c01` | 194.92s | Gemini selected A with high confidence | `aud-t07_c02` | 169.92s | Gemini flagged B timing/phrasing weakness. |
| 8 | Cushion Seat, Charging Cord | `aud-t08_c01` | 131.88s | Gemini selected A | `aud-t08_c02` | 146.68s | Both variants are short; needs human listen. |
| 9 | Crosswalk Stripes Before Six | `aud-t09_c01` | 165.92s | Gemini selected A with high confidence | `aud-t09_c02` | 178.80s | Gemini preferred A for warmer sax-accent fit. |
| 10 | Yellow Tag on the Umbrella Rack | `aud-t10_c01` | 192.44s | local technical fallback | `aud-t10_c02` | 199.52s | Variants technically comparable; human listen recommended. |
| 11 | Quiz Key in Blue Ink | `aud-t11_c01` | 159.88s | Gemini selected A with high confidence | `aud-t11_c02` | 158.40s | Gemini preferred A for rounded study-table groove. |
| 12 | Tray Return at 5:59 | `aud-t12_c01` | 199.32s | local technical fallback | `aud-t12_c02` | 200.00s | Variants technically comparable; human listen recommended. |
| 13 | Latch Click at the Courtyard Gate | `aud-t13_c01` | 150.00s | Gemini selected A with high confidence | `aud-t13_c02` | 155.00s | Gemini preferred A for closing reprise warmth. |

## Candidate Paths

- Selected draft root: `candidates/s01e01-campus-cafe-longplay/audio/selected/`
- Pool root: `candidates/s01e01-campus-cafe-longplay/audio/pool/`
- Candidate IDs map to original variants: `c01` = first file without `(1)`, `c02` = second file with `(1)` before organization.

## Still Required

- Continue with selected audio QA handoff in `reviews/audio-qa-listening.md`.
- Human listening pass is recorded for all selected draft candidates from the user verdict on 2026-05-19.
- Lyric alignment spot-check remains required for all selected candidates.
- Duration and sequence pacing review because selected draft is about 41:31.
- Optional regeneration or swap from pool before any render/export planning.

## Still Blocked

Render/export, video assembly, subtitles timing, upload/publish, scheduling, analytics, Content ID action, rights/platform-safety claims, and release readiness remain blocked until separate explicit gates.
