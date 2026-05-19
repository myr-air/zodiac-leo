# S01E01 Suno Prompt Retune Research Trail

Status: source-only research note  
Episode: `s01e01-campus-cafe-longplay`  
Observed: 2026-05-19

## Boundary

This note is source-only. It does not approve provider/Suno/browser/API/account action, generation, candidate creation, render/export, upload/publish, Content ID action, or rights/platform/release claims.

## Sources

| URL | Observed date | Evidence summary | Applicability / caveat | Decision impact |
|---|---|---|---|---|
| https://musicsmith.ai/blog/ai-music-generation-prompts-best-practices | 2026-05-19 | Clear prompts outperform fancy/long prompts; front-load genre+mood because style text may truncate; use descriptive brief with genre/mood/vocal/tempo/structure; use short exclusions; avoid artist names; preserve model flexibility. | High applicability to Suno style/exclude wording quality and consistency. Third-party blog, not official Suno docs. | Retune base and per-track `Styles` to compact descriptive specs; shorten excludes; place genre/mood/vocal/tempo early. |
| https://jackrighteous.com/blogs/guides-using-suno-ai-music-creation/advanced-suno-prompt-engineering-guide | 2026-05-19 | Treat prompts as specs; separate identity/palette/vocals/section goals/constraints; avoid contradictions; iterate one variable at a time; Weirdness increases surprise; Style Influence increases adherence; keep hook conservative. | High applicability to source planning format and control tuning. Third-party guide, not official Suno docs. | Add planning scaffold (`IDENTITY / PALETTE / VOCALS / SECTION GOALS / CONSTRAINTS`) while keeping final style fields compact; set low/moderate Weirdness and high consistent Style Influence. |
| https://viblo.asia/p/how-to-prompt-suno-a-comprehensive-guide-2oKLn1kWJQO | 2026-05-19 | Generic prompt writing reminders: clarity, context, concise-but-detailed wording. | Medium/low applicability due generic framing. | Reinforces concise, explicit wording and avoiding prompt bloat. |
| Medium URL (provided by user) | 2026-05-19 | Returned HTTP 403 and was inaccessible during review window. | Inaccessible; no evidence extracted. | Not used as evidence for retune decisions. |

## Retune Direction Applied

- Keep Suno `Styles` concise and front-loaded: genre, mood, vocal, tempo first.
- Keep `Exclude Styles` short and targeted with safety blockers retained.
- Preserve strict teen PG same-age guardrails (non-sexualized, no adult/minor, no teacher/student, no childlike voice, no real school/brand identity).
- Iterate one variable at a time in future source-only retunes.
- Keep cohesive longplay controls: low/moderate Weirdness, high consistent Style Influence.
