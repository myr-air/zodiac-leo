import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image


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

    def test_only_current_gate_output_root_is_allowed(self):
        render.assert_allowed_output_root(render.PROJECT_ROOT / render.DEFAULT_OUTPUT_ROOT)
        self.assertEqual(render.DEFAULT_OUTPUT_ROOT.name, "future-local-render-05")

        with self.assertRaises(ValueError):
            render.assert_allowed_output_root(render.PROJECT_ROOT / "candidates" / "s01e01-campus-cafe-longplay" / "render" / "future-local-render-01")

        with self.assertRaises(ValueError):
            render.assert_allowed_output_root(render.PROJECT_ROOT / "candidates" / "s01e01-campus-cafe-longplay" / "render" / "future-local-render-02")

        with self.assertRaises(ValueError):
            render.assert_allowed_output_root(render.PROJECT_ROOT / "candidates" / "s01e01-campus-cafe-longplay" / "render" / "future-local-render-03")

        with self.assertRaises(ValueError):
            render.assert_allowed_output_root(render.PROJECT_ROOT / "candidates" / "s01e01-campus-cafe-longplay" / "render" / "future-local-render-04")

        with self.assertRaises(ValueError):
            render.assert_allowed_output_root(render.PROJECT_ROOT / "candidates" / "s01e01-campus-cafe-longplay" / "render" / "smoke-test")

    def test_render_segments_cover_whole_timeline_with_song_gaps(self):
        segments = render.render_segments()
        self.assertEqual(len(segments), 13)
        self.assertEqual(segments[0].start, 0.0)
        self.assertAlmostEqual(segments[-1].end, render.TARGET_DURATION)
        for segment, track in zip(segments, render.TRACKS):
            self.assertEqual(segment.track, track)
            self.assertAlmostEqual(segment.start, track.start)

    def test_now_playing_uses_header_font_family_for_render_05(self):
        self.assertEqual(render.NOW_PLAYING_FONT_PATHS, render.HEADER_FONT_PATHS)
        fonts = render.render_fonts()
        self.assertEqual(fonts["header"].getname()[0], fonts["now"].getname()[0])

    def test_temp_root_is_constrained_to_private_temp_subtree(self):
        render.assert_safe_temp_root(render.DEFAULT_TEMP_ROOT / "frames")

        with self.assertRaises(ValueError):
            render.assert_safe_temp_root(render.PROJECT_ROOT)

        with self.assertRaises(ValueError):
            render.assert_safe_temp_root(render.DEFAULT_TEMP_ROOT / "bad\nroot")

    def test_concat_paths_reject_control_char_injection(self):
        with self.assertRaises(ValueError):
            render.quote_concat_path(render.DEFAULT_TEMP_ROOT / "bad\nfile.png")

    def test_parse_srt_time_supports_millisecond_precision(self):
        self.assertEqual(render.parse_srt_time("00:39:26,080"), 2366.08)

    def test_equalizer_frame_has_soft_visible_alpha(self):
        frame = render.make_equalizer_frame(0.75, 12.0)

        alpha = frame.getchannel("A")
        self.assertGreater(alpha.getbbox()[2], 300)
        self.assertGreater(max(alpha.getdata()), 100)

    def test_subtitle_motion_uses_slow_fade_and_subtle_upward_slide(self):
        cue = render.SubtitleCue(12.0, 14.5, "First line\nSecond line")
        alpha_start, dx_start, dy_start = render.subtitle_motion_state(cue, cue.start)
        alpha_mid, dx_mid, dy_mid = render.subtitle_motion_state(cue, cue.start + 1.35)
        alpha_end, _, _ = render.subtitle_motion_state(cue, cue.end)

        self.assertAlmostEqual(render.subtitle_fade_seconds(cue), 0.7)
        self.assertEqual((dx_start, dy_start), (-2.0, 8.0))
        self.assertEqual((round(dx_mid, 3), round(dy_mid, 3)), (0.0, 0.0))
        self.assertEqual(alpha_start, 0.0)
        self.assertGreater(alpha_mid, 0.99)
        self.assertEqual(alpha_end, 0.0)

    def test_refined_headphone_icon_is_balanced_and_visible(self):
        icon = render.refined_headphone_icon()
        self.assertEqual(icon.size, (94, 92))
        self.assertEqual(render.HEADPHONE_ICON_POS, (48, 88))

        alpha = icon.getchannel("A")
        bbox = alpha.getbbox()
        self.assertIsNotNone(bbox)
        assert bbox is not None
        center_x = (bbox[0] + bbox[2]) / 2
        self.assertLess(abs(center_x - 47), 3)
        self.assertGreater(max(alpha.getdata()), 120)

    def test_music_note_frame_is_subtle_and_in_icon_zone(self):
        frame = render.render_music_note_frame(1.4)
        self.assertEqual(frame.size, (render.MUSIC_NOTE_CANVAS_WIDTH, render.MUSIC_NOTE_CANVAS_HEIGHT))

        alpha = frame.getchannel("A")
        bbox = alpha.getbbox()
        self.assertIsNotNone(bbox)
        assert bbox is not None
        self.assertLessEqual(max(alpha.getdata()), 90)
        self.assertGreater(bbox[0], 35)
        self.assertLess(bbox[2], render.MUSIC_NOTE_CANVAS_WIDTH)

    def test_render_05_light_reflection_shadow_textures_have_visible_alpha(self):
        makers = (
            render.make_sunlight_texture,
            render.make_reflection_texture,
            render.make_shadow_texture,
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            for maker in makers:
                path = Path(tmpdir) / f"{maker.__name__}.png"
                maker(path)
                alpha = Image.open(path).getchannel("A")
                self.assertIsNotNone(alpha.getbbox())
                self.assertGreater(max(alpha.getdata()), 0)


if __name__ == "__main__":
    unittest.main()
