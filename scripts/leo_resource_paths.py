"""Shared path helpers for resource/candidate roots."""

from __future__ import annotations

from pathlib import Path
import os


def resolve_candidates_root(workspace_root: Path | str | None = None) -> Path:
    """Resolve the candidate media root.

    Priority:
    1) `LEO_RESOURCE_ROOT` environment variable, interpreted as the Drive root.
       - If set to ".../candidates", that directory is used directly.
       - Otherwise `<value>/candidates` is used.
    2) `<workspace_root>/candidates` fallback.
    """
    base_root = Path(workspace_root) if workspace_root is not None else Path(__file__).resolve().parents[1]
    env_root = os.environ.get("LEO_RESOURCE_ROOT")

    if not env_root:
        return Path(base_root).resolve() / "candidates"

    candidate_root = Path(env_root).expanduser()
    if not candidate_root.is_absolute():
        candidate_root = (Path(base_root) / candidate_root).resolve()
    else:
        candidate_root = candidate_root.resolve()

    if candidate_root.name != "candidates":
        candidate_root = candidate_root / "candidates"

    return candidate_root

