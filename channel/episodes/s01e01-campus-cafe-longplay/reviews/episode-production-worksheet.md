# S01E01 Production Worksheet — After-School First Love Longplay

Status: source-only internal gate  
Episode: `s01e01-campus-cafe-longplay`  
Prepared date: 2026-05-18

## 0. Source-Only Boundary

This worksheet evaluates internal source readiness only. It does not approve provider use, media generation, render/export, upload, publishing, Suno/YouTube/API/browser automation, account mutation, credential storage, Content ID registration, or positive rights/platform claims.

## 1. Required Inputs Checklist

| Input | Path / source | Present? | Notes |
|---|---|---:|---|
| Channel strategy | `channel/channel.md` | yes | Cozy chill vocal longplay promise. |
| Roadmap | `channel/roadmap.md` | yes | Week 1 retuned to After-School First Love Longplay. |
| Episode manifest | `channel/episodes/s01e01-campus-cafe-longplay/manifest.json` | yes | Source packet open. |
| Operating boundary | `docs/operating-boundary.md` | yes | Source packet allowed; media/account actions blocked. |
| Provider/platform boundary | `docs/provider-platform-boundary.md` | yes | Provider and upload actions blocked. |
| Song source | `source/songs.md` | yes | Tracks 1-13 source lyrics theme-retuned after user direction change. |
| Theme retune review | `reviews/theme-retune.md` | yes | Direction changed to wholesome PG same-age teen/high-school first love. |
| Suno manual fields | `source/suno-manual-fields.md`, `source/suno-tracks/*.md`, `reviews/suno-manual-fields.md` | yes | Suno 5.5 source-only handoff is split into 13 copy-ready track files with index/defaults; no provider approval. |
| Prompt/control pack | `source/prompt-pack.md`, `reviews/prompt-pack.md` | yes | Theme-retuned source-only manual field pack reviewed; no provider approval. |
| Candidate intake checklist | `reviews/candidate-intake-checklist.md` | yes | Future-gate checklist only; no real candidates exist. |
| External lyric review | `reviews/gemini-lyrics-review.md` | historical | Gemini CLI review completed for the earlier adult/college-coded draft; superseded by theme retune. |
| Visual source | `source/visual.md`, `source/visual-prompt-pack.md`, `reviews/visual-prompt-pack.md` | yes | Theme-retuned source-only visual prompts and safe zones prepared. |
| Metadata source | `source/metadata.md` | yes | Draft copy and disclosure only. |
| Tracking CSVs | `tracking/*.csv` | yes | Initial source-state rows only. |

Verdict: `revise_source_only`  
Reason: required source packet files and source lyrics exist, but real media evidence, subtitles, readiness scoring, and release gates are not present.

## 2. Strategy Lock

| Decision | Locked value | Reviewer notes |
|---|---|---|
| Listener job | study, reading, journaling, desk work, coffee break | Matches channel promise. |
| Episode promise | an after-school first-love longplay with soft vocals and small shy details | Source-only lock. |
| World / location / time | after-school cafe, library, hallway, bus stop, school courtyard | PG same-age peer framing only. |
| Emotional arc | final bell -> noticing -> shared routine -> almost-plan -> gentle courtyard walk-away close | Good for 13-song sequence. |
| Duration decision | 30-35 minutes / 13 songs | Baseline format. |
| Arrangement variation | one piano-forward song and one soft sax accent song | Matches roadmap guardrail. |
| Public claims avoided | yes | No release or platform safety claim. |

Verdict: `pass_internal_source`

## 3. Lyric Audit Status

Tracks 1-13 have theme-retuned source-only lyric drafts and a source-level checkpoint in `reviews/lyrics.md`.

Gemini CLI external review found no blockers for the earlier adult/college-coded draft. Recommended revisions were applied then, but this external review is now superseded by the user-approved theme retune.

| Criterion | Weight | Score | Evidence / notes |
|---|---:|---:|---|
| Concrete scene details, not generic abstract language | 25 | 22 | All 13 title anchors are concrete and scene-based with added after-school cues. |
| Believable teenage first-love emotional logic | 20 | 17 | The arc remains low-stakes and PG: noticing, routine, small help, trust, almost-plan, and walk-away close. |
| Non-repetitive hooks and images across reviewed tracks | 20 | 17 | Anchors differ; cafe/afternoon/school motifs need fresh read-through after retune. |
| Singable phrasing and subtitle-friendly line lengths | 15 | 14 | Most lines are short; real sung phrasing still needs later review. |
| No blocked/capped words from the overuse guardrail | 10 | 10 | No blocked generic terms found. |
| Title/chorus/bridge each adds new meaning | 10 | 9 | Bridges add restrained movement. |
| **Total** | **100** | **88** | `pass_source_theme_retune_checkpoint` for source lyrics only. |

## 4. Song Structure Diversity Status

The source outline includes adjacent-difference planning across all 13 tracks. This still needs re-review after full lyrics and any later audio candidate evidence exist.

## 5. Visual Safe-Zone Status

Visual safe zones are planned in `source/visual.md` and reviewed in `reviews/visual.md`. Real image candidate checks remain blocked until a separate future visual candidate gate exists.

## 6. Named Revision Gates

| # | Gate | Status | Re-review trigger |
|---:|---|---|---|
| 1 | Strategy lock | pass | listener job, world, duration, or episode promise changes |
| 2 | Song-source packet | revise_after_theme_retune | titles, briefs, structure matrix, style, or exclude field changes |
| 3 | Lyric anti-slop audit | pass_source_theme_retune_checkpoint | fresh human/external review recommended before provider handoff |
| 4 | Prompt/control package review | pass_source_theme_retuned | provider/model/control fields or manual handoff notes change |
| 5 | Candidate intake/provenance check | source_checklist_prepared | real user-supplied files exist |
| 6 | Objective audio QA | n/a | real audio files exist |
| 7 | Human listening and similarity pass | n/a | real audio files exist |
| 8 | Sequence/chapter plan | revise | order, gap, chapter, duration, or story arc changes |
| 9 | Visual world and safe-zone plan | pass_source_theme_retuned_prompt_pack | subject, layout, overlay, crop, prompt, or source image use changes |
| 10 | Subtitle/source timing plan | pending | lyrics, sung words, timing policy, or timeline exists |
| 11 | Metadata/disclosure pack | revise | title, description, tags, chapters, disclosure, or claim wording changes |
| 12 | Internal readiness scorecard | pending | source packet becomes complete enough to score |
| 13 | Future render/export gate | blocked | render/export intent or final asset path changes |
| 14 | Future upload/public-publish planning gate | blocked | upload intent, account boundary, policy, disclosure, or asset status changes |
| 15 | Post-release analytics loop | n/a | future release exists and manual metrics are provided |

## 7. Final Source Verdict

```text
Verdict: revise_source_only
Scope: internal source-only readiness
Anti-slop lyric score: 88/100 for theme-retuned source lyrics
Internal readiness score: pending
Critical blockers: no audio evidence, no visual candidate, no subtitles, no readiness gate, no release gate
Required revisions: fresh lyric review before provider handoff; add real evidence only after separate gates
Next allowed action: human/external review of theme-retuned source lyrics
Still blocked: provider/account automation, media generation, render/export, upload/publish, API calls, credential handling, Content ID registration, rights/platform-safety claims
```
