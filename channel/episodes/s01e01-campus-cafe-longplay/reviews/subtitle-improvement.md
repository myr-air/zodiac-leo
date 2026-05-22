# S01E01 Subtitle Improvement Review

Status: track_1_human_watch_passed_source_only_final_sidecars_blocked  
Updated: 2026-05-22

## Boundary

This review opens source-only subtitle improvement for vocal alignment and shorter lyric cue segmentation. It does not approve final `.srt`/`.vtt` sidecars, full video assembly, render/export, upload/publish, provider/API/browser/account action, release readiness, or rights/platform-safety claims.

## User Direction

User passed the V6 cute-smooth visual direction source-only and closed the visual proof review gate. Residual subtitle issue was that proof subtitles were not aligned closely enough to the sung vocal and some cue chunks were too long. User then passed the current Track 1 subtitle proof after the sung-lyric watch pass source-only.

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
- Method: `stable-ts` alignment from approved source lyrics and selected Track 1 WAV, with accurate mode as the default and `--fast-mode` opt-in only.
- Motion polish: subtitle proof rendering now keeps cue start/end timing unchanged while using proof-only slower entry motion (`1.5s` fade/slide in with 18px upward slide) and fade-only exit (`1.0s` fade out, no slide out).
- Boundary: these files are ignored local evidence for subtitle review only. They are not final sidecars, full assembly, render/export, upload, release, or rights/platform-safety approval.

## Mechanical Check

- Track 1 line count matches: 59 expected lines and 59 display cues.
- Minimum display gap: `0.08s`.
- Maximum line length: 37 characters.
- Cue 41 bridge timing is corrected from the stale long-span proof to a 3.24s display cue.
- Review flags retained for provenance: cues 58-59 are low-confidence outro repeat alignments; cue 58 is the longest display cue at 6.26s.
- Human sung-lyric watch pass: user passed the current Track 1 proof source-only on 2026-05-22.

## Improvement Rules

- Align cue starts and ends to sung vocal phrasing, not to approximate proof placeholders.
- Prefer phrase-level cues over long stanza blocks.
- Keep 1-2 lines per cue, with natural line breaks at breath, clause, or musical phrase boundaries.
- Avoid cue text that stays onscreen after the sung phrase has clearly moved on.
- Do not invent lyric words if the sung audio differs from source text; mark uncertainty for review.
- Do not create final sidecars until a later final timeline/assembly gate approves the exact output target.

## Current Verdict

`track_1_alignment_proof_human_watch_passed_source_only_final_sidecars_blocked`

Next allowed source-only action is to carry the reviewed Track 1 proof timing forward as reference for a later assembly timeline. Final `.srt`/`.vtt` sidecars, full assembly, render/export, upload/publish, and release remain blocked until a separate explicit gate.
