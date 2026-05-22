import importlib.util
import argparse
import sys
import tempfile
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

    def test_serialize_final_vtt_has_no_draft_note(self):
        vtt = pipeline.serialize_final_vtt([
            pipeline.Cue(slot="T01", start=0.0, end=1.0, text="hello"),
        ])

        self.assertTrue(vtt.startswith("WEBVTT"))
        self.assertNotIn("DRAFT", vtt)
        self.assertIn("00:00:00.000 --> 00:00:01.000", vtt)

    def test_promote_reviewed_display_cues_shifts_to_track_starts_and_keeps_gap_blank(self):
        drafts = [
            {
                "track_number": 1,
                "audio_duration_seconds": 10.0,
                "display_cue_count": 1,
                "display_cues": [
                    {"slot": "T01", "start": 1.0, "end": 2.0, "text": "first line"},
                ],
            },
            {
                "track_number": 2,
                "audio_duration_seconds": 5.0,
                "display_cue_count": 1,
                "display_cues": [
                    {"slot": "T02", "start": 0.5, "end": 1.25, "text": "second line"},
                ],
            },
        ]

        cues, timeline, summary = pipeline.promote_reviewed_display_cues(drafts, gap_seconds=1.0)

        self.assertEqual(timeline[0]["track_end"], 10.0)
        self.assertEqual(timeline[0]["gap_end"], 11.0)
        self.assertEqual(cues[0].start, 1.0)
        self.assertEqual(cues[1].start, 11.5)
        self.assertTrue(all(not (10.0 < cue.start < 11.0) for cue in cues))
        self.assertEqual(summary["cue_count"], 2)

    def test_final_sidecar_path_guard_rejects_paths_outside_episode_subtitles(self):
        with self.assertRaises(ValueError):
            pipeline.assert_safe_final_sidecar_path(Path("outputs/bad.srt"), "s01e01-campus-cafe-longplay")

    def test_promote_final_sidecars_checks_path_before_mkdir(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            proof_root = temp_root / "proofs"
            track_dir = proof_root / "track-01"
            track_dir.mkdir(parents=True)
            (track_dir / "s01e01-track-01-subtitle-alignment-draft-01.json").write_text(
                """
{
  "track_number": 1,
  "audio_duration_seconds": 10.0,
  "line_count_matches": true,
  "display_cue_count": 1,
  "display_cues": [
    {"slot": "T01", "start": 1.0, "end": 2.0, "text": "first line"}
  ]
}
""".strip()
                + "\n",
                encoding="utf-8",
            )
            bad_out_dir = temp_root / "outside" / "unsafe"
            args = argparse.Namespace(
                episode_id="s01e01-campus-cafe-longplay",
                proof_root=str(proof_root),
                out_dir=str(bad_out_dir),
                proof_prefix="s01e01",
                prefix="s01e01-campus-cafe-longplay",
                gap_seconds=1.0,
                max_line_chars=37,
                tracks=[1],
                print_json=False,
            )

            with self.assertRaises(ValueError):
                pipeline.promote_final_sidecars(args)

            self.assertFalse(bad_out_dir.exists())

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

    def test_build_track_text_can_exclude_absent_sections(self):
        track = {
            "slot": "T13",
            "sections": [
                {"section": "Dialogue First", "lines": ["missing line"]},
                {"section": "Verse 1", "lines": ["sung line"]},
            ],
        }

        text, line_meta = pipeline.build_track_text(track, excluded_sections=["dialogue first"])

        self.assertEqual(text, "sung line")
        self.assertEqual(len(line_meta), 1)
        self.assertEqual(line_meta[0]["section"], "Verse 1")

    def test_apply_subtitle_display_timing_adds_padding_without_overlap(self):
        vocal_cues = [
            pipeline.Cue(slot="T01", start=10.0, end=11.0, text="first line", vocal_start=10.0, vocal_end=11.0),
            pipeline.Cue(slot="T01", start=11.25, end=12.0, text="second line", vocal_start=11.25, vocal_end=12.0),
        ]

        display = pipeline.apply_subtitle_display_timing(
            vocal_cues,
            lead_in=0.20,
            tail_hold=0.24,
            fade_out=0.16,
            min_gap=0.08,
            track_end=20.0,
        )

        self.assertEqual(display[0].start, 9.8)
        self.assertEqual(display[1].start, 11.05)
        self.assertLessEqual(display[0].end + 0.08, display[1].start)
        self.assertEqual(display[0].vocal_start, 10.0)
        self.assertEqual(display[0].vocal_end, 11.0)

    def test_adjusted_segment_bounds_repairs_stretched_low_confidence_first_word(self):
        start, end, corrected = pipeline.adjusted_segment_bounds(
            {
                "start": 0.42,
                "end": 16.30,
                "words": [
                    {"word": " After", "start": 0.42, "end": 14.24, "probability": 0.008},
                    {"word": " school,", "start": 14.24, "end": 15.16, "probability": 0.55},
                    {"word": " down", "start": 15.82, "end": 16.30, "probability": 0.99},
                ],
            }
        )

        self.assertTrue(corrected)
        self.assertEqual(start, 13.24)
        self.assertEqual(end, 16.3)

    def test_align_song_source_track_defaults_to_accurate_alignment(self):
        observed = {}
        original = pipeline.align_song_source_track

        def fake_align_song_source_track(args):
            observed["fast_mode"] = args.fast_mode
            observed["fade_in"] = args.fade_in
            observed["fade_out"] = args.fade_out
            observed["motion_fade_in"] = args.motion_fade_in
            observed["motion_fade_out"] = args.motion_fade_out
            observed["motion_slide_pixels"] = args.motion_slide_pixels
            observed["motion_slide_out_pixels"] = args.motion_slide_out_pixels

        pipeline.align_song_source_track = fake_align_song_source_track
        try:
            self.assertEqual(pipeline.main(["align-song-source-track", "--no-render"]), 0)
        finally:
            pipeline.align_song_source_track = original

        self.assertFalse(observed["fast_mode"])
        self.assertEqual(observed["fade_in"], 0.34)
        self.assertEqual(observed["fade_out"], 0.30)
        self.assertEqual(observed["motion_fade_in"], 1.50)
        self.assertEqual(observed["motion_fade_out"], 1.00)
        self.assertEqual(observed["motion_slide_pixels"], 18.0)
        self.assertEqual(observed["motion_slide_out_pixels"], 0.0)

    def test_parse_track_from_song_source_accepts_bonus_track_header(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source_path = Path(temp_dir) / "songs.md"
            source_path.write_text(
                "### Track 13 Bonus \u2014 Latch Click at the Courtyard Gate\n"
                "```text\n"
                "[Verse]\n"
                "One closing line\n"
                "```\n",
                encoding="utf-8",
            )

            track = pipeline.parse_track_from_song_source(source_path, 13)

        self.assertEqual(track["slot"], "T13")
        self.assertEqual(track["working_title"], "Latch Click at the Courtyard Gate")
        self.assertEqual(track["sections"][0]["lines"], ["One closing line"])

    def test_subtitle_motion_slides_in_then_fades_out_without_slide(self):
        fade_in = 1.50
        fade_out = 1.00

        alpha_start, offset_start = pipeline.subtitle_motion_alpha_and_offset(
            10.0,
            10.0,
            14.0,
            fade_in=fade_in,
            fade_out=fade_out,
        )
        alpha_mid, offset_mid = pipeline.subtitle_motion_alpha_and_offset(
            12.0,
            10.0,
            14.0,
            fade_in=fade_in,
            fade_out=fade_out,
        )
        alpha_end, offset_end = pipeline.subtitle_motion_alpha_and_offset(
            14.0,
            10.0,
            14.0,
            fade_in=fade_in,
            fade_out=fade_out,
        )
        alpha_fading_out, offset_fading_out = pipeline.subtitle_motion_alpha_and_offset(
            13.5,
            10.0,
            14.0,
            fade_in=fade_in,
            fade_out=fade_out,
        )

        self.assertEqual(alpha_start, 0.0)
        self.assertEqual(alpha_mid, 1.0)
        self.assertEqual(alpha_end, 0.0)
        self.assertEqual(offset_start, 18.0)
        self.assertEqual(offset_mid, 0.0)
        self.assertEqual(offset_end, 0.0)
        self.assertLess(alpha_fading_out, 1.0)
        self.assertEqual(offset_fading_out, 0.0)


if __name__ == "__main__":
    unittest.main()
