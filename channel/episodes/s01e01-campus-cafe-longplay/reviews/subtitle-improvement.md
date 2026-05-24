# S01E01 Subtitle Improvement Review

Status: final_sidecars_promoted_track_1_cue_58_text_corrected_source_only_render_export_blocked  
Updated: 2026-05-24

## Boundary

This review records source-only subtitle improvement for vocal alignment and shorter lyric cue segmentation, plus the later source-only final sidecar promotion. It does not approve full video assembly, render/export, upload/publish, provider/API/browser/account action, release readiness, transcript certification, or rights/platform-safety claims.

## User Direction

User passed the V6 cute-smooth visual direction source-only and closed the visual proof review gate. Residual subtitle issue was that proof subtitles were not aligned closely enough to the sung vocal and some cue chunks were too long. User then passed the current Track 1 subtitle proof after the sung-lyric watch pass source-only. Gate 10 work generated no-render draft alignment sidecars for Tracks 2-13; Track 13 is aligned against sung source sections only because the selected audio begins at Verse 1 and omits the source `Dialogue First` section. User later reported all remaining Tracks 2-13 PASS after human watch source-only, then approved final sidecar promotion using `reviews/assembly-package.md`. On 2026-05-24, after render-04 review, the user identified a Track 1 late-song lyric text mismatch; cue 58 at `00:04:10.280 --> 00:04:16.540` was corrected from `Save my seat and I'll walk you home` to `Same seat tomorrow after school` with timing unchanged.

## Inputs

- Visual proof accepted source-only: `candidates/s01e01-campus-cafe-longplay/visual/proofs/animated-v6/s01e01-vis-c01-v6-cute-smooth-motion-proof-30s-01.mp4`.
- Selected audio source for Track 1 proof: `candidates/s01e01-campus-cafe-longplay/audio/selected/aud-t01_c02--margin-notes-at-table-three.wav`.
- Full selected audio sequence is recorded in `reviews/audio-qa-listening.md` and `tracking/assets.csv`.
- Source lyrics: `source/songs.md`.
- Subtitle workspace: `subtitles/README.md`.

## Generated Track 1 Proof

- Draft JSON: `candidates/s01e01-campus-cafe-longplay/subtitles/proofs/track-01/s01e01-track-01-subtitle-alignment-draft-01.json`.
- Draft proof video: `candidates/s01e01-campus-cafe-longplay/subtitles/proofs/track-01/s01e01-track-01-subtitle-alignment-draft-01.proof.mp4`.
- Draft proof sidecars: `...draft.srt`, `...draft.vtt`, and `...proof.ass` in the same local proof directory.
- Tracks 2-12 no-render draft sidecars: `candidates/s01e01-campus-cafe-longplay/subtitles/proofs/track-02/` through `track-12/`.
- Track 13 sung-section draft sidecars: `track-13/`, generated with `--exclude-sections "Dialogue First"`, returned 32 expected lines and 32 display cues. Historical incomplete fast-check evidence remains in `track-13-fast-check/` for provenance.
- Method: `stable-ts` alignment from approved source lyrics and selected Track 1 WAV, with accurate mode as the default and `--fast-mode` opt-in only.
- Motion polish: subtitle proof rendering now keeps cue start/end timing unchanged while using proof-only slower entry motion (`1.5s` fade/slide in with 18px upward slide) and fade-only exit (`1.0s` fade out, no slide out).
- Boundary: proof files remain ignored local evidence. Promoted final sidecars live under `subtitles/` and are source-only; they are not full assembly, render/export, upload, release, transcript certification, or rights/platform-safety approval.

## Mechanical Check

- Track 1 line count matches: 59 expected lines and 59 display cues.
- Minimum display gap: `0.08s`.
- Maximum line length: 37 characters.
- Cue 41 bridge timing is corrected from the stale long-span proof to a 3.24s display cue.
- Review flags retained for provenance: cues 58-59 are low-confidence outro repeat alignments; cue 58 is the longest display cue at 6.26s.
- Human sung-lyric watch pass: user passed the current Track 1 proof source-only on 2026-05-22, then reported Tracks 2-13 PASS source-only on 2026-05-22.
- Tracks 2-12: draft line-count coverage matches source lyrics, no-overlap checks pass, and user human-watch pass is recorded source-only.
- Track 13: sung-section draft line-count coverage matches selected-audio sections, no-overlap checks pass, and user human-watch pass is recorded source-only; the absent `Dialogue First` source section is excluded from subtitle timing and remains a source/audio caveat.
- Final sidecar promotion: `scripts/subtitle_alignment_pipeline.py promote-final-sidecars --print-json` produced 598 cues across 13 tracks, max line length 37 chars, no overlaps, no cues in the 1-second inter-track gaps, Track 13 `Dialogue First` exclusion preserved, and final timeline duration `41:43.28`.
- Track 1 cue 58 source correction: source `.srt` and `.vtt` plus Track 1 lyric mirrors now use `Same seat tomorrow after school` at the existing outro-hook timing. Cue count, timing, gap policy, and line-length ceiling are unchanged.

## Improvement Rules

- Align cue starts and ends to sung vocal phrasing, not to approximate proof placeholders.
- Prefer phrase-level cues over long stanza blocks.
- Keep 1-2 lines per cue, with natural line breaks at breath, clause, or musical phrase boundaries.
- Avoid cue text that stays onscreen after the sung phrase has clearly moved on.
- Do not invent lyric words if the sung audio differs from source text; mark uncertainty for review.
- Do not revise or regenerate final sidecars without a later sidecar revision/promotion gate.

## Current Verdict

`final_sidecars_promoted_track_1_cue_58_text_corrected_source_only_render_export_blocked`

Next allowed source-only action is separately approved render/export planning if the user wants to move beyond subtitle source files. Full assembly, render/export, upload/publish, and release remain blocked until a separate explicit gate.
