# Mellow Longplay Episode Zero-To-YouTube Runbook Template

Status: template / source-first four-HIL gated workflow
Episode: `<episode-id>`
Prepared by: `<name-or-agent>`
Prepared date: `<YYYY-MM-DD>`

## 0. Boundary

This runbook coordinates an episode from an empty source packet to a guarded
YouTube handoff using the four planned HIL checkpoints. It does not approve provider use, generated media,
render/export, upload, public publishing, scheduling, API/browser/account
automation, credential storage, Content ID action, private analytics capture, or
positive rights/platform-safety claims.

## 0.1 Four Planned HIL Checkpoints

| HIL | User action | System may proceed to | Stop before |
|---|---|---|---|
| HIL-1 | User says to make a new episode. | Scaffold, source shaping, lyrics, Suno fields, song prompts, visual prompts, metadata draft, manual handoff notes. | Provider/browser/account generation, candidate IDs, render/export. |
| HIL-2 | User says generated/supplied media is ready and to continue. | Candidate intake, selected/pool mapping, assembly, subtitles, local preview and risk review. | Full render/upload actions. |
| HIL-3 | User approves preview-risk loop and asks for final local candidate. | Full render + thumbnail + top-level comment draft. | Upload/API/browser/account/public publish/schedule. |
| HIL-4 | User approves exact final candidate for release action. | Release/upload package, API/manual execution if selected, schedule action. | Unapproved account actions, unsupported pinning path, broader account mutation. |

Unplanned HIL is only for blockers: contradictory direction, missing/mismatched
files, failed verification, scope expansion, or provider/platform/security risk.

For S01E04, start from the roadmap seed only:

```text
Episode ID: s01e04-bookstore-afternoon-longplay
Working longplay: Bookstore Afternoon Longplay
Hook: quiet bookstore corner, paper texture
Lyric lane: teenage love, private thoughts, shy hope, calm reflection
```

## 1. Bootstrap Command

Dry-run first:

```bash
bash scripts/dev-python.sh scripts/bootstrap_episode_packet.py --s01e04 --dry-run
```

Create the source-only packet after checking the dry-run list:

```bash
bash scripts/dev-python.sh scripts/bootstrap_episode_packet.py --s01e04
bash scripts/verify-standalone.sh
```

The bootstrap creates source/review/tracking placeholders only. It must not
create `candidates/<episode-id>/`, candidate IDs, provenance facts, generated
media, render outputs, YouTube video IDs, or release facts.

## 2. Gate Flow

| Gate | Goal | Exit evidence | Planned HIL | Still blocked |
|---:|---|---|---|---|
| 0 | Scaffold source packet | manifest, current-state, source placeholders, tracking CSVs | HIL-1 opens | all media/external actions |
| 1 | Source prompt packet | episode spine, track deltas, lyrics, Suno fields, song/visual prompts, reviews | no extra planned HIL | provider use, candidates, render, YouTube |
| 2 | Candidate intake | real local audio/visual files exist first; selected/pool map, provenance rows | HIL-2 opens | release/platform actions |
| 3 | Assembly package | sequence, metadata/disclosure, upload-description chapter timestamps, English post-upload comment draft, subtitle sidecars/plan | none unless blocker | platform/API/public release/comment action |
| 4 | Preview and issue-led patch loop | preview points reviewed, issue notes logged, patch plan + status updated | HIL-2 open and completes before render | platform/API/public release |
| 5 | Full render + thumbnail + comment prep | full render candidate, thumbnail candidate, top-level comment draft in source/comment.txt | HIL-3 open after preview pass | upload/API/public release/comment pin |
| 6 | Release/upload + schedule | package/API/manual execution, thumbnail/comment follow-up, schedule note/action | HIL-4 decision | unapproved visibility mutation, analytics, Content ID |

Do not advance gates by implication. The planned prompts are HIL-1, HIL-2, HIL-3, and
HIL-4; internal gates should not interrupt unless a blocker appears. Each
external platform/API action still needs a separate narrow gate with current
evidence.

## 3. Gate 1 Fastlane Checklist

- Reuse `channel/channel.md` and `channel/roadmap.md` by citation.
- Define the Episode Style & Theme Spine before track drafting.
- For EP03 onward, apply the channel/roadmap creative delta: no planned sax
  special color, piano still allowed, exactly one non-sax special instrument in
  exactly one song, and several feeling/mood-led tracks in the 13-track slate.
- For every track, record Story + Reference Brief, Track Delta, structure
  fingerprint, micro-pattern matrix, lexical count ledger, and Suno 5.5 fields.
- Suno lyrics must include a pre-song context/control block before the first sung
  section, such as `[Song Context]`, `[Vocal Direction]`, `[Arrangement Map]`,
  and `[Duration Target]`, so Custom Mode is not forced to infer the whole
  performance from section headers alone.
- Suno `Styles` must carry concrete controls: BPM, vocal lane, instrumentation,
  arrangement arc, mix/timbre language, and a 3-minute/full-length target.
  `Exclude Styles` must block lyric drift, random vocal drift, under-3-minute
  sketches, abrupt endings, and the usual imitation/unsafe genre lanes.
- Keep references out of final lyrics, titles, Suno fields, metadata, and visual
  prompts unless they are generic abstract traits.
- Block named-artist/song/voice/channel/brand imitation and unsupported rights or
  platform claims.

## 4. YouTube Handoff Checklist

Open only after HIL-4 approves the exact final-video candidate or requests the
exact release path.

| Check | Evidence | Owner |
|---|---|---|
| Final video approval | exact MP4/render path, sidecar paths, thumbnail path if any | user + source review |
| Metadata/disclosure | title, description, chapters, tags, AI-assisted disclosure, English post-upload comment draft | source review |
| Current policy check | official current YouTube/public policy sources observed at review time | source review + user |
| Account-specific check | upload limits, channel warnings/strikes, disclosure UI, feature availability | user only; do not store private account state |
| Provenance/risk acceptance | non-secret provenance and known limitations recorded | user |
| Route choice | manual Studio handoff or guarded private API path; support automatic post-upload comment posting via `--comment-file` or env `MELLOW_YOUTUBE_COMMENT_FILE` | user |
| Rollback owner | delete/unlist/privacy/edit/comment/pin responsibilities | user |

Allowed source-only output before execution: a manual copy package or a private
API dry-run package. Actual API/browser/account mutation remains blocked until an
episode-specific execution gate is opened by HIL-4 or later explicit instruction.
The guarded upload helper supports posting one top-level comment automatically with
`commentThreads.insert` by passing the `--comment-file` argument (pointing to
`channel/episodes/<episode-id>/source/comment.txt`) or specifying
`MELLOW_YOUTUBE_COMMENT_FILE` in the external env file. For comment-only follow-up,
the guarded comment helper scans existing top-level channel comments first and
blocks exact duplicate text unless `--force-repost` is explicitly supplied.
Comment pinning remains a manual account action on YouTube Studio unless a future
official API endpoint and exact gate are recorded.

## 5. Final Handoff Card

```text
Verdict: source_prompt_handoff | final_video_candidate_pending | final_video_approved_hold_release | private_upload_gate_requested | public_publish_gate_requested | point_revision_requested | block
Scope: <source-only / local QA / YouTube handoff planning>
Evidence: <paths>
Allowed next action: <one narrow action>
Still blocked: provider/account automation, media generation without gate, render/export without gate, upload/publish/API without gate, credentials in repo, Content ID, rights/platform-safety claims
```
