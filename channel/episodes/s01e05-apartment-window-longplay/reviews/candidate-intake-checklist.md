# S01E05 Candidate Intake Checklist — Apartment Window Longplay

Status: gate_2_checks_complete / source-only / public publish blocked
Updated: 2026-06-09

## Boundary

This checklist records local media sanity checks for S01E05. Candidate files remain ignored local evidence under `candidates/`. This does not approve provider/browser/API/account action, upload/publish, Content ID action, transcript certification, release readiness, or rights/platform-safety claims.

## Check Items

- [x] All 13 selected audio tracks (`c01`) present in `audio/selected/` and correctly named.
- [x] All 13 pool audio tracks (`c02`) present in `audio/pool/` and correctly named.
- [x] Visual candidate (`vis-c01`) present in `visual/selected/` and correctly named.
- [x] File naming validation checks pass (all files conform to standard schema `aud-tXX_cYY--slug.wav`).
- [x] Audio silence verification (no silent gaps >= 5s inside the wav tracks) passes.

## Verdict

```text
Verdict: candidate_intake_checklist_passed_source_only
Scope: local media validation and formatting checklist
```
