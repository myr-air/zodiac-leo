# S01E04 Subtitle Audit + Core Workflow (All Tracks)

Updated: 2026-06-08
Episode: `s01e04-bookstore-afternoon-longplay`

Goal
- Verify all 13 tracks for lead-in timing, gap continuity, overlap, and cue count before final publish-step handoff.

Workflow (canonical)
1. Build draft alignments per track from song-source with no full render:
   - `python3 scripts/subtitle_alignment_pipeline.py align-song-source-track --track-number N --out-dir candidates/s01e04-bookstore-afternoon-longplay/subtitles/track-0N --prefix s01e04 --fast-mode --onset-evidence --no-render`
2. Validate timing continuity in a single pass:
   - Check `display_cues` first cue, max inter-cue gap, and overlap.
3. Promote reviewed draft lanes only when approved:
   - `python3 scripts/subtitle_alignment_pipeline.py promote-final-sidecars --episode-id s01e04-bookstore-afternoon-longplay --proof-root candidates/s01e04-bookstore-afternoon-longplay/subtitles --out-dir channel/episodes/s01e04-bookstore-afternoon-longplay/subtitles --proof-prefix s01e04 --prefix s01e04-bookstore-afternoon-longplay --tracks 1 2 3 4 5 6 7 8 9 10 11 12 13 --gap-seconds 1.0 --max-line-chars 37`

Execution result (approved now)
- Input draft files: all `track-XX/s01e04-track-XX-subtitle-alignment-draft-01.json` under `candidates/s01e04-bookstore-afternoon-longplay/subtitles`.
- Output final sidecars:
  - [s01e04-bookstore-afternoon-longplay.en.srt](../subtitles/s01e04-bookstore-afternoon-longplay.en.srt)
  - [s01e04-bookstore-afternoon-longplay.en.vtt](../subtitles/s01e04-bookstore-afternoon-longplay.en.vtt)
- `status` for promoted draft JSON remains `draft_alignment_requires_human_watch_pass` (human review pass is still required by policy), but all draft lane timing files were accepted for local source sidecar promotion.

Track timing summary (draft-01 artifacts)
- Track 1: first cue 0.88s, max inter-cue gap 1.22s, overlap count 0
- Track 2: first cue 2.84s, max inter-cue gap 3.66s, overlap count 0
- Track 3: first cue 10.74s, max inter-cue gap 2.70s, overlap count 0
- Track 4: first cue 0.12s, max inter-cue gap 7.92s, overlap count 0
- Track 5: first cue 0.36s, max inter-cue gap 1.16s, overlap count 0
- Track 6: first cue 3.06s, max inter-cue gap 2.28s, overlap count 0
- Track 7: first cue 3.20s, max inter-cue gap 6.56s, overlap count 0
- Track 8: first cue 13.08s, max inter-cue gap 11.12s, overlap count 0
- Track 9: first cue 0.32s, max inter-cue gap 2.26s, overlap count 0
- Track 10: first cue 3.50s, max inter-cue gap 5.04s, overlap count 0
- Track 11: first cue 0.42s, max inter-cue gap 1.28s, overlap count 0
- Track 12: first cue 12.12s, max inter-cue gap 1.38s, overlap count 0
- Track 13: first cue 0.52s, max inter-cue gap 2.06s, overlap count 0

Decision
- No overlap found in any track lane.
- Track-3 lead-in is long for artistic intro handling and remains non-overlap.
- Approved for source subtitle finality at track-lane level pending final Gate-4 metadata + policy passes.
