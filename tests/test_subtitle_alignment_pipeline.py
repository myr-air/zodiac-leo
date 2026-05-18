import importlib.util
import sys
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "subtitle_alignment_pipeline.py"
spec = importlib.util.spec_from_file_location("subtitle_alignment_pipeline", SCRIPT_PATH)
assert spec is not None and spec.loader is not None
pipeline = importlib.util.module_from_spec(spec)
sys.modules["subtitle_alignment_pipeline"] = pipeline
spec.loader.exec_module(pipeline)


class SubtitleAlignmentPipelineTest(unittest.TestCase):
    def test_compute_track_timeline_inserts_blank_gap_between_songs(self):
        timeline = pipeline.compute_track_timeline(
            [("A01", 10.0), ("A02", 20.0), ("A03", 5.5)],
            gap_seconds=1.75,
        )

        self.assertEqual(timeline[0]["track_start"], 0.0)
        self.assertEqual(timeline[0]["track_end"], 10.0)
        self.assertEqual(timeline[0]["gap_start"], 10.0)
        self.assertEqual(timeline[0]["gap_end"], 11.75)

        self.assertEqual(timeline[1]["track_start"], 11.75)
        self.assertEqual(timeline[1]["track_end"], 31.75)
        self.assertEqual(timeline[1]["gap_start"], 31.75)
        self.assertEqual(timeline[1]["gap_end"], 33.5)

        self.assertEqual(timeline[2]["track_start"], 33.5)
        self.assertEqual(timeline[2]["track_end"], 39.0)
        self.assertIsNone(timeline[2]["gap_start"])
        self.assertIsNone(timeline[2]["gap_end"])

    def test_shift_cues_applies_early_offset_but_keeps_gap_blank(self):
        local_cues = [
            pipeline.Cue(slot="A02", start=0.10, end=1.20, text="first sung line"),
            pipeline.Cue(slot="A02", start=1.60, end=2.40, text="second sung line"),
        ]

        shifted = pipeline.shift_track_cues(
            local_cues,
            track_start=11.75,
            track_end=31.75,
            early_offset=0.25,
        )

        self.assertEqual(shifted[0].start, 11.75)
        self.assertEqual(shifted[0].end, 12.95)
        self.assertEqual(shifted[1].start, 13.10)
        self.assertEqual(shifted[1].end, 14.15)

        # The first cue must not appear inside the previous inter-song blank gap.
        self.assertTrue(all(cue.start >= 11.75 for cue in shifted))

    def test_shift_cues_applies_end_padding_clamped_before_next_cue_and_track_end(self):
        local_cues = [
            pipeline.Cue(slot="A13", start=0.00, end=1.00, text="first sung line"),
            pipeline.Cue(slot="A13", start=1.10, end=1.80, text="second sung line"),
            pipeline.Cue(slot="A13", start=2.50, end=2.92, text="closing sung line"),
        ]

        shifted = pipeline.shift_track_cues(
            local_cues,
            track_start=100.0,
            track_end=103.0,
            early_offset=0.0,
            end_padding=0.30,
            min_gap=0.02,
        )

        self.assertEqual(shifted[0].end, 101.08)
        self.assertLessEqual(shifted[0].end + 0.02, shifted[1].start)
        self.assertEqual(shifted[1].end, 102.10)
        self.assertEqual(shifted[2].end, 103.00)

    def test_serialize_srt_and_vtt_preserve_cue_gaps(self):
        cues = [
            pipeline.Cue(slot="A01", start=0.0, end=1.0, text="hello"),
            pipeline.Cue(slot="A02", start=3.0, end=4.0, text="world"),
        ]

        srt = pipeline.serialize_srt(cues)
        vtt = pipeline.serialize_vtt(cues)

        self.assertNotIn("00:00:01,000 --> 00:00:03,000", srt)
        self.assertIn("00:00:00,000 --> 00:00:01,000", srt)
        self.assertIn("00:00:03,000 --> 00:00:04,000", srt)

        self.assertTrue(vtt.startswith("WEBVTT"))
        self.assertIn("00:00:00.000 --> 00:00:01.000", vtt)
        self.assertIn("00:00:03.000 --> 00:00:04.000", vtt)

    def test_build_track_text_preserves_line_breaks_for_stable_ts_original_split(self):
        track = {
            "slot": "A01",
            "sections": [
                {"section": "verse", "lines": ["line one", "line two"]},
                {"section": "chorus", "lines": ["line three"]},
            ],
        }

        text, line_meta = pipeline.build_track_text(track)

        self.assertEqual(text, "line one\nline two\nline three")
        self.assertEqual([m["section"] for m in line_meta], ["verse", "verse", "chorus"])
        self.assertEqual([m["line_index"] for m in line_meta], [0, 1, 0])


if __name__ == "__main__":
    unittest.main()
