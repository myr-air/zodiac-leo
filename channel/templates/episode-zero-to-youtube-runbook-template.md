# Mellow Longplay Episode Zero-To-YouTube Runbook Template

Status: template / source-first three-HIL gated workflow  
Episode: `<episode-id>`  
Prepared by: `<name-or-agent>`  
Prepared date: `<YYYY-MM-DD>`

## 0. Boundary

This runbook coordinates an episode from an empty source packet to a guarded
YouTube handoff using the three planned HIL checkpoints. It does not approve provider use, generated media,
render/export, upload, public publishing, scheduling, API/browser/account
automation, credential storage, Content ID action, private analytics capture, or
positive rights/platform-safety claims.

## 0.1 Three Planned HIL Checkpoints

| HIL | User action | System may proceed to | Stop before |
|---|---|---|---|
| HIL-1 | User says to make a new episode. | Scaffold, source shaping, lyrics, Suno fields, song prompts, visual prompts, metadata draft, manual handoff notes. | Provider/browser/account generation, candidate IDs, render/export. |
| HIL-2 | User says generated/supplied media is ready and to continue. | Candidate intake, selected/pool mapping, assembly, subtitles, local render/export, intensive local QA. | Upload/API/browser/account/public publish. |
| HIL-3 | User approves final video for upload prep/exact action or sends point revisions. | Release/upload package or exact approved platform action; or issue-led local revision. | Rights/platform-safety claims, Content ID, transcript certification, or broader account actions. |

Unplanned HIL is only for blockers: contradictory direction, missing/mismatched
files, failed verification, scope expansion, or provider/platform/security risk.

For S01E02, start from the roadmap seed only:

```text
Episode ID: s01e02-classroom-window-longplay
Working longplay: Classroom Window Longplay
Hook: college classroom light, afternoon window
Lyric lane: curiosity, almost-said feelings, study-day warmth
```

## 1. Bootstrap Command

Dry-run first:

```bash
bash scripts/dev-python.sh scripts/bootstrap_episode_packet.py --s01e02 --dry-run
```

Create the source-only packet after checking the dry-run list:

```bash
bash scripts/dev-python.sh scripts/bootstrap_episode_packet.py --s01e02
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
| 3 | Assembly package | sequence, metadata/disclosure, chapter plan, subtitle sidecars/plan | none unless blocker | platform/API/public release |
| 4 | Local render/export + intensive QA | local render, mechanical QA, subtitle checks, visual/layout review, issue-led rerender if allowed | none unless blocker | platform/API/public release |
| 5 | Final video approval | exact candidate MP4, QA/review summaries, known limits | HIL-3 decision | upload/API/public release until exact action gate |
| 6 | Release/upload package or exact execution, if selected | episode-specific API/manual gate; channel verification; external env; privacy/visibility as approved | HIL-3 exact action approval | unapproved visibility mutation, captions, analytics, Content ID |
| 7 | Public publish decision, if separate | explicit user final visibility approval and user-owned action record | HIL-3 or later explicit action | positive rights/platform guarantees |

Do not advance gates by implication. The planned prompts are HIL-1, HIL-2, and
HIL-3 only; internal gates should not interrupt unless a blocker appears. Each
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
- Keep references out of final lyrics, titles, Suno fields, metadata, and visual
  prompts unless they are generic abstract traits.
- Block named-artist/song/voice/channel/brand imitation and unsupported rights or
  platform claims.

## 4. YouTube Handoff Checklist

Open only after HIL-3 approves the exact final-video candidate or requests the
exact upload/prep path.

| Check | Evidence | Owner |
|---|---|---|
| Final video approval | exact MP4/render path, sidecar paths, thumbnail path if any | user + source review |
| Metadata/disclosure | title, description, chapters, tags, AI-assisted disclosure | source review |
| Current policy check | official current YouTube/public policy sources observed at review time | source review + user |
| Account-specific check | upload limits, channel warnings/strikes, disclosure UI, feature availability | user only; do not store private account state |
| Provenance/risk acceptance | non-secret provenance and known limitations recorded | user |
| Route choice | manual Studio handoff or guarded private API path | user |
| Rollback owner | delete/unlist/privacy/edit responsibilities | user |

Allowed source-only output before execution: a manual copy package or a private
API dry-run package. Actual API/browser/account mutation remains blocked until an
episode-specific execution gate is opened by HIL-3 or later explicit instruction.

## 5. Final Handoff Card

```text
Verdict: source_prompt_handoff | final_video_candidate_pending | final_video_approved_hold_release | private_upload_gate_requested | public_publish_gate_requested | point_revision_requested | block
Scope: <source-only / local QA / YouTube handoff planning>
Evidence: <paths>
Allowed next action: <one narrow action>
Still blocked: provider/account automation, media generation without gate, render/export without gate, upload/publish/API without gate, credentials in repo, Content ID, rights/platform-safety claims
```
