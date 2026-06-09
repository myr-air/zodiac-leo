import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = PROJECT_ROOT / "scripts"
SCRIPT_PATH = SCRIPT_DIR / "render_s01e02_local.py"
sys.path.insert(0, str(SCRIPT_DIR))
spec = importlib.util.spec_from_file_location("render_s01e02_local", SCRIPT_PATH)
assert spec is not None and spec.loader is not None
render = importlib.util.module_from_spec(spec)
sys.modules["render_s01e02_local"] = render
spec.loader.exec_module(render)


class RenderS01E02LocalTest(unittest.TestCase):
    def test_only_render_02_revision_output_root_is_allowed(self):
        self.assertEqual(render.DEFAULT_OUTPUT_ROOT.name, "local-render-02")
        render.assert_allowed_output_root(render.PROJECT_ROOT / render.DEFAULT_OUTPUT_ROOT)

        with self.assertRaises(ValueError):
            render.assert_allowed_output_root(
                render.PROJECT_ROOT
                / "candidates"
                / "s01e02-classroom-window-longplay"
                / "render"
                / "local-render-01"
            )

    def test_refined_headphone_icon_matches_ep1_render05_standard(self):
        icon = render.refined_headphone_icon()
        self.assertEqual(icon.size, (94, 92))
        self.assertEqual(render.HEADPHONE_ICON_POS, (48, 34))

        alpha = icon.getchannel("A")
        bbox = alpha.getbbox()
        self.assertIsNotNone(bbox)
        assert bbox is not None
        center_x = (bbox[0] + bbox[2]) / 2
        self.assertLess(abs(center_x - 47), 3)
        self.assertGreater(max(alpha.getdata()), 120)

    def test_music_note_frame_stays_subtle_in_header_zone(self):
        frame = render.render_music_note_frame(1.4)
        self.assertEqual(frame.size, (render.MUSIC_NOTE_CANVAS_WIDTH, render.MUSIC_NOTE_CANVAS_HEIGHT))

        alpha = frame.getchannel("A")
        bbox = alpha.getbbox()
        self.assertIsNotNone(bbox)
        assert bbox is not None
        self.assertLessEqual(max(alpha.getdata()), 90)
        self.assertGreater(bbox[0], 35)
        self.assertLess(bbox[2], render.MUSIC_NOTE_CANVAS_WIDTH)

    def test_custom_ribbon_equalizer_replaces_showwaves_style(self):
        frame = render.make_equalizer_frame(0.75, 12.0)

        alpha = frame.getchannel("A")
        self.assertGreater(alpha.getbbox()[2], 300)
        self.assertGreater(max(alpha.getdata()), 90)

    def test_ass_burnin_keeps_header_out_of_subtitle_filter(self):
        timeline = [render.TimelineTrack(render.TRACKS[0], 0.0, 12.0, 288)]
        cues = [render.Cue("T01", 1.0, 3.0, "First line")]
        ass = render.serialize_ass(cues, timeline, 12.0)

        self.assertIn("Style: Lyric", ass)
        self.assertIn("First line", ass)
        self.assertNotIn("Header,,", ass)
        self.assertNotIn("TrackTitle,,", ass)

    def test_night_classroom_effect_textures_have_visible_alpha(self):
        makers = (
            render.make_particle_texture,
            render.make_star_texture,
            render.make_lamp_glow_texture,
            render.make_light_sweep,
            render.make_night_glow_texture,
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

    def test_particle_motion_is_slow_random_drift_not_upward_scroll_only(self):
        x_expr, y_expr = render.particle_motion_expr(render.global_time_expr(184.72))

        self.assertIn("sin", x_expr)
        self.assertIn("cos", x_expr)
        self.assertIn("sin", y_expr)
        self.assertIn("cos", y_expr)
        self.assertNotIn("mod(-", y_expr)

    def test_render_segments_cover_timeline_with_following_gaps(self):
        timeline = [
            render.TimelineTrack(render.TRACKS[0], 0.0, 10.0, 240),
            render.TimelineTrack(render.TRACKS[1], 11.0, 20.0, 216),
        ]
        segments = render.render_segments(timeline, 20.0)

        self.assertEqual(len(segments), 2)
        self.assertEqual(segments[0].start, 0.0)
        self.assertEqual(segments[0].end, 11.0)
        self.assertEqual(segments[1].start, 11.0)
        self.assertEqual(segments[1].end, 20.0)

    def test_segment_cues_shift_to_segment_local_time(self):
        segment = render.RenderSegment(
            index=2,
            entry=render.TimelineTrack(render.TRACKS[1], 11.0, 20.0, 216),
            start=11.0,
            end=20.0,
        )
        cues = [
            render.Cue("T01", 1.0, 3.0, "before"),
            render.Cue("T02", 12.5, 14.0, "inside"),
        ]

        shifted = render.segment_cues(cues, segment)

        self.assertEqual(len(shifted), 1)
        self.assertEqual(shifted[0].text, "inside")
        self.assertAlmostEqual(shifted[0].start, 1.5)
        self.assertAlmostEqual(shifted[0].end, 3.0)


if __name__ == "__main__":
    unittest.main()
