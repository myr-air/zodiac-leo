import importlib.util
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = PROJECT_ROOT / "scripts"
SCRIPT_PATH = SCRIPT_DIR / "render_s01e01_local.py"
sys.path.insert(0, str(SCRIPT_DIR))
spec = importlib.util.spec_from_file_location("render_s01e01_local", SCRIPT_PATH)
assert spec is not None and spec.loader is not None
render = importlib.util.module_from_spec(spec)
sys.modules["render_s01e01_local"] = render
spec.loader.exec_module(render)


class RenderS01E01LocalTest(unittest.TestCase):
    def test_timeline_tracks_match_planned_target_and_gaps(self):
        self.assertEqual(len(render.TRACKS), 13)
        self.assertEqual(render.TRACKS[0].start, 0.0)
        self.assertAlmostEqual(render.TRACKS[-1].end, render.TARGET_DURATION)

        gaps = [next_track.start - track.end for track, next_track in zip(render.TRACKS, render.TRACKS[1:])]

        self.assertEqual(len(gaps), 12)
        for gap in gaps:
            self.assertAlmostEqual(gap, render.GAP_SECONDS, places=6)

    def test_render_outputs_are_guarded_to_candidates_tree(self):
        render.assert_under_candidates(render.PROJECT_ROOT / "candidates" / "ok" / "file.mp4")

        with self.assertRaises(ValueError):
            render.assert_under_candidates(render.PROJECT_ROOT / "channel" / "unsafe.mp4")

    def test_only_canonical_output_root_is_allowed(self):
        render.assert_default_output_root(render.PROJECT_ROOT / render.DEFAULT_OUTPUT_ROOT)

        with self.assertRaises(ValueError):
            render.assert_default_output_root(render.PROJECT_ROOT / "candidates" / "s01e01-campus-cafe-longplay" / "render" / "smoke-test")

    def test_temp_root_is_constrained_to_private_temp_subtree(self):
        render.assert_safe_temp_root(render.DEFAULT_TEMP_ROOT / "frames")

        with self.assertRaises(ValueError):
            render.assert_safe_temp_root(render.PROJECT_ROOT)

    def test_parse_srt_time_supports_millisecond_precision(self):
        self.assertEqual(render.parse_srt_time("00:39:26,080"), 2366.08)


if __name__ == "__main__":
    unittest.main()
