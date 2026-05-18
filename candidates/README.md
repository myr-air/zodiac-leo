# Candidate Media Boundary

`candidates/` is ignored local evidence storage for user-supplied media only. Durable facts belong in episode tracking CSVs and review docs.

Current drop zones:

- None. Create `candidates/<episode-id>/audio/` and `candidates/<episode-id>/visuals/` only after the matching episode packet exists.

Do not store credentials, screenshots with private account state, browser profiles, auth files, or raw private analytics here.
