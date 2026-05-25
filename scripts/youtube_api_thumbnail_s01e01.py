#!/usr/bin/env python3
"""Backward-compatible S01E01 entry point for the generic thumbnail helper.

Prefer `scripts/youtube_api_thumbnail.py` for new Mellow Longplay videos.
"""

from __future__ import annotations

from youtube_api_thumbnail import main


if __name__ == "__main__":
    raise SystemExit(main())
