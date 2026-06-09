# Mellow Longplay Episode Lessons And Rules

Status: active carry-forward summary
Updated: 2026-06-05

## Why This Exists

Keep the working memory lean. Detailed episode evidence stays in each episode packet; this file keeps only lessons that should change the next episode.

## Current Snapshot

| Episode | Useful state | Do not over-claim |
|---|---|---|
| S01E01 `After-School First Love Longplay` | Final local render-05 QA was user-approved; private YouTube API upload and selected thumbnail set are recorded. | Public release, Content ID, monetization, platform safety, and rights safety are not proven by repo evidence. |
| S01E02 `Classroom Window Longplay` | Render-01 is the final-video candidate; audio/subtitle/visual lanes are pre-final approved; final video approval is pending. | Final video approval is not release/upload approval. |

## Lessons Learned

### Workflow / HIL

- Too many micro-approvals slow the channel. Use four planned HIL checkpoints: new episode, generated-media-ready continue, final-video decision, and release-route decision.
- Internal gates are still required for evidence, but they should not become user interruptions unless a blocker appears.
- Final video approval and upload/release approval are separate. Do not merge them by implication.

### Source And Songwriting

- Repeated object-proof formulas get stale fast. EP03+ should include more feeling/mood-led tracks where atmosphere or emotion leads while staying concrete.
- Keep the Story + Reference Brief, Track Delta, structure fingerprint, strict micro-pattern gate, title/lyric relationship gate, and lexical count ledger.
- Do not title songs by instruments unless the instrument is a real story object. Arrangement belongs in `Styles` and notes.
- Every Suno `Styles` field needs approximate BPM and clear control values.
- EP03+ rule: no planned sax special color; choose exactly one non-sax special instrument for exactly one song.

### Visual Direction

- The channel house style is now fixed: soft watercolor semi-realistic anime playlist-cover illustration / lo-fi watercolor anime poster style.
- The recurring listener woman should be recognizable by archetype and motifs, not by exact face or exact pose. Vary pose, gesture, camera angle, and object interaction.
- Keep the gold crescent-vinyl totem visible when possible.
- Do not use stored/local references as provider reference-image inputs unless a future explicit gate opens that exact action.

### Candidate Intake

- Candidate IDs and provenance start only after real local files exist.
- Technical fallback is allowed for overnight/local automation, but any weak evidence must be carried into final-video review rather than becoming a hidden claim.
- Keep pool variants until final-video approval or an issue-led replacement decision.
- Do not rely on blind mechanical fallback (e.g. choosing files without suffix) for audio selection. Run automatic silence detection (silencedetect filter) to identify Suno generation glitches (such as long silent gaps) before finalizing the selection.

### Subtitles

- Mechanical cue checks prove structure, not transcript certification.
- Keep cue checks: parseable files, no overlaps, no cues in planned gaps, readable line length, and current-source lyric basis.
- If selected audio differs from source lyrics, record uncertainty; do not silently rewrite subtitles.
- When swapping an audio candidate or changing track durations, always regenerate track-level subtitle alignments and verify that absolute cue timestamps across the entire longplay match the updated chapter timeline window. Run strict validation tests to check for cues outside track windows.

### Render And Review

- FFmpeg capabilities vary by environment. S01E02 needed Pillow-generated overlays because `ass`, `subtitles`, and `drawtext` filters were not available.
- Rerenders should be issue-led: name the exact overlay, subtitle, visual, audio, crop, motion, or timing problem.
- Agy/browser visual review can support layout/readability, but it does not prove audio quality, lyric alignment, transcript certification, or platform safety.

### Upload / Platform

- API helpers must verify the authenticated channel ID before mutation and keep env/client/token paths outside repo.
- Captions were not uploaded for S01E01 because subtitles were burned in; do not assume that for future episodes without a gate.
- Start metadata source with chapter timestamps whenever a local/final timeline exists; chapters belong in the upload description package, not as an afterthought.
- Draft one short English post-upload engagement comment during metadata work. API posting can use a separate `commentThreads.insert` gate after a video ID exists; pinning remains manual/account-side unless a future official API gate is recorded.
- Never claim `copyright-free`, `royalty-free`, `Content ID-safe`, `monetization-safe`, `platform-safe`, `upload-ready`, or `publish-ready` except as blocked/caution language.

## Next Episode Rules

1. Start with HIL-1, then create only source/prompt handoff materials.
2. Stop for user/manual generation; do not create candidate IDs before real files exist.
3. After HIL-2, run intake -> assembly -> subtitles -> render -> intensive QA as one local system slice.
4. Stop at HIL-3 with one exact final-video candidate and a short issue list, then advance to HIL-4 for the release route decision when ready.
5. If HIL-3 approves final-video candidate, move to HIL-4 (release route). HIL-4 opens the separate release/upload gate with current policy/account checks, metadata chapters, and the English post-upload comment draft.
6. If HIL-3 requests revisions, change only the named issue area.
