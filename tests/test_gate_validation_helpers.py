import sys
import unittest
import tempfile
import json
import wave
from pathlib import Path

# Add scripts directory to path to import gate_validation_helpers
sys.path.append(str(Path(__file__).resolve().parents[1] / "scripts"))
import gate_validation_helpers

class GateValidationHelpersTest(unittest.TestCase):
    def test_parse_srt_time(self):
        self.assertEqual(gate_validation_helpers.parse_srt_time("00:00:00,000"), 0.0)
        self.assertEqual(gate_validation_helpers.parse_srt_time("00:01:05,123"), 65.123)
        self.assertEqual(gate_validation_helpers.parse_srt_time("02:00:00.500"), 7200.5)
        with self.assertRaises(ValueError):
            gate_validation_helpers.parse_srt_time("invalid")

    def test_normalize_text_simple(self):
        self.assertEqual(gate_validation_helpers.normalize_text_simple("Hello, World!"), "helloworld")
        self.assertEqual(gate_validation_helpers.normalize_text_simple("  test...   one two "), "testonetwo")

    def test_parse_srt_cues(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            srt_path = Path(tmpdir) / "test.srt"
            srt_content = (
                "1\n"
                "00:00:01,000 --> 00:00:03,500\n"
                "Hello World\n"
                "\n"
                "2\n"
                "00:00:04,100 --> 00:00:06,200\n"
                "Line Two\n"
            )
            srt_path.write_text(srt_content, encoding="utf-8")
            cues = gate_validation_helpers.parse_srt_cues(srt_path)
            self.assertEqual(len(cues), 2)
            self.assertEqual(cues[0]["start"], 1.0)
            self.assertEqual(cues[0]["end"], 3.5)
            self.assertEqual(cues[0]["text"], "Hello World")
            self.assertEqual(cues[1]["start"], 4.10)
            self.assertEqual(cues[1]["end"], 6.20)
            self.assertEqual(cues[1]["text"], "Line Two")

    def test_run_subtitle_alignment_check_success(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            episode_id = "s01e99-test-episode"

            # Create structure
            audio_dir = workspace / "candidates" / episode_id / "audio" / "selected"
            audio_dir.mkdir(parents=True)
            align_pack_dir = workspace / "candidates" / episode_id / "subtitles" / "proofs" / "longplay" / "align-pack"
            align_pack_dir.mkdir(parents=True)
            subtitles_dir = workspace / "channel" / "episodes" / episode_id / "subtitles"
            subtitles_dir.mkdir(parents=True)

            # Create mock wave files
            def create_mock_wav(path, duration):
                with wave.open(str(path), "wb") as wav:
                    wav.setparams((2, 2, 48000, int(duration * 48000), "NONE", "not compressed"))
                    wav.writeframes(b"\x00" * int(duration * 48000) * 4)

            create_mock_wav(audio_dir / "aud-t01_c01--song-one.wav", 10.0)
            create_mock_wav(audio_dir / "aud-t02_c01--song-two.wav", 15.0)

            # Create local alignment JSONs
            # Track 1: start 1.0, end 9.0 relative to song
            # Track 2: start 0.5, end 14.0 relative to song
            track1_dir = align_pack_dir / "track-01"
            track1_dir.mkdir()
            track1_json = track1_dir / "s01e99-track-01-subtitle-alignment-draft-01.json"
            track1_json.write_text(json.dumps({
                "track_number": 1,
                "display_cues": [
                    {"start": 1.0, "end": 9.0, "text": "Song one lyrics"}
                ]
            }))

            track2_dir = align_pack_dir / "track-02"
            track2_dir.mkdir()
            track2_json = track2_dir / "s01e99-track-02-subtitle-alignment-draft-01.json"
            track2_json.write_text(json.dumps({
                "track_number": 2,
                "display_cues": [
                    {"start": 0.5, "end": 14.0, "text": "Song two lyrics"}
                ]
            }))

            # Create promoted SRT file
            # Timeline is:
            # Track 1 starts at 0.0, ends at 10.0.
            # Gap of 1.0s.
            # Track 2 starts at 11.0, ends at 26.0.
            # So expected cues:
            # Cue 1: start 1.0, end 9.0
            # Cue 2: start 11.5, end 25.0
            srt_path = subtitles_dir / f"{episode_id}.en.srt"
            srt_content = (
                "1\n"
                "00:00:01,000 --> 00:00:09,000\n"
                "Song one lyrics\n"
                "\n"
                "2\n"
                "00:00:11,500 --> 00:00:25,000\n"
                "Song two lyrics\n"
            )
            srt_path.write_text(srt_content, encoding="utf-8")

            # Run check
            errors = gate_validation_helpers.run_subtitle_alignment_check(episode_id, workspace_root=workspace)
            self.assertEqual(errors, [])

    def test_run_subtitle_alignment_check_failure(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir)
            episode_id = "s01e99-test-episode"

            audio_dir = workspace / "candidates" / episode_id / "audio" / "selected"
            audio_dir.mkdir(parents=True)
            align_pack_dir = workspace / "candidates" / episode_id / "subtitles" / "proofs" / "longplay" / "align-pack"
            align_pack_dir.mkdir(parents=True)
            subtitles_dir = workspace / "channel" / "episodes" / episode_id / "subtitles"
            subtitles_dir.mkdir(parents=True)

            def create_mock_wav(path, duration):
                with wave.open(str(path), "wb") as wav:
                    wav.setparams((2, 2, 48000, int(duration * 48000), "NONE", "not compressed"))
                    wav.writeframes(b"\x00" * int(duration * 48000) * 4)

            create_mock_wav(audio_dir / "aud-t01_c01--song-one.wav", 10.0)
            create_mock_wav(audio_dir / "aud-t02_c01--song-two.wav", 15.0)

            # Local alignment JSONs
            track1_dir = align_pack_dir / "track-01"
            track1_dir.mkdir()
            (track1_dir / "s01e99-track-01-subtitle-alignment-draft-01.json").write_text(json.dumps({
                "track_number": 1,
                "display_cues": [
                    {"start": 1.0, "end": 9.0, "text": "Song one lyrics"}
                ]
            }))

            track2_dir = align_pack_dir / "track-02"
            track2_dir.mkdir()
            (track2_dir / "s01e99-track-02-subtitle-alignment-draft-01.json").write_text(json.dumps({
                "track_number": 2,
                "display_cues": [
                    {"start": 0.5, "end": 14.0, "text": "Song two lyrics"}
                ]
            }))

            # Bad promoted SRT file (cue 2 starts at 20.0s instead of 11.5s, representing out of sync swap)
            srt_path = subtitles_dir / f"{episode_id}.en.srt"
            srt_content = (
                "1\n"
                "00:00:01,000 --> 00:00:09,000\n"
                "Song one lyrics\n"
                "\n"
                "2\n"
                "00:00:20,000 --> 00:00:33,500\n"
                "Song two lyrics\n"
            )
            srt_path.write_text(srt_content, encoding="utf-8")

            # Run check - should detect timing misalignment error!
            errors = gate_validation_helpers.run_subtitle_alignment_check(episode_id, workspace_root=workspace)
            self.assertTrue(len(errors) > 0)
            self.assertTrue(any("timing misalignment" in err or "out-of-sync" in err for err in errors))

if __name__ == "__main__":
    unittest.main()
