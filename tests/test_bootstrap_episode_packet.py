import csv
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PROJECT_ROOT / "scripts" / "bootstrap_episode_packet.py"
spec = importlib.util.spec_from_file_location("bootstrap_episode_packet", SCRIPT_PATH)
assert spec is not None and spec.loader is not None
bootstrap = importlib.util.module_from_spec(spec)
sys.modules["bootstrap_episode_packet"] = bootstrap
spec.loader.exec_module(bootstrap)


class BootstrapEpisodePacketTest(unittest.TestCase):
    def config(self):
        return bootstrap.EpisodeBootstrapConfig(
            episode_id="s01e02-classroom-window-longplay",
            working_longplay="Classroom Window Longplay",
            hook="college classroom light, afternoon window, desk notes",
            lyric_lane="curiosity, almost-said feelings, study-day warmth",
            prepared_by="Mayr",
            prepared_date="2026-05-26",
        )

    def test_dry_run_lists_packet_files_without_creating_them(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)

            summary = bootstrap.bootstrap_episode_packet(self.config(), root=root, dry_run=True)

            self.assertEqual(summary["mode"], "dry_run")
            self.assertIn(
                "channel/episodes/s01e02-classroom-window-longplay/manifest.json",
                summary["planned_files"],
            )
            self.assertIn(
                "channel/episodes/s01e02-classroom-window-longplay/reviews/release-decision-plan.md",
                summary["planned_files"],
            )
            self.assertFalse((root / "channel" / "episodes" / "s01e02-classroom-window-longplay").exists())

    def test_create_packet_writes_valid_source_only_scaffold_without_candidates(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)

            summary = bootstrap.bootstrap_episode_packet(self.config(), root=root)
            packet = root / "channel" / "episodes" / "s01e02-classroom-window-longplay"

            self.assertEqual(summary["mode"], "write")
            self.assertTrue((packet / "manifest.json").is_file())
            self.assertFalse((root / "candidates" / "s01e02-classroom-window-longplay").exists())

            manifest = json.loads((packet / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["episode_id"], "s01e02-classroom-window-longplay")
            self.assertEqual(manifest["status"], "gate_0_scaffolded_source_only")
            self.assertEqual(manifest["gate"], "gate_0_bootstrap")
            self.assertIn("Not public publish", manifest["claim_boundary"])

            current_state = (packet / "reviews" / "current-state.md").read_text(encoding="utf-8")
            self.assertIn("public publish remains blocked", current_state)
            self.assertIn("Gate 1 source packet is not locked yet", current_state)

            release_plan = (packet / "reviews" / "release-decision-plan.md").read_text(encoding="utf-8")
            self.assertIn("not opened", release_plan)
            self.assertIn("Public publish remains blocked", release_plan)

            with (packet / "tracking" / "status.csv").open(newline="", encoding="utf-8") as handle:
                status_rows = list(csv.DictReader(handle))
            self.assertEqual(status_rows[0]["gate"], "gate_0_bootstrap")
            self.assertEqual(status_rows[-1]["status"], "blocked")
            self.assertIn("Upload publish", status_rows[-1]["notes"])

    def test_invalid_episode_id_is_rejected_before_paths_are_created(self):
        config = self.config()
        config.episode_id = "../bad"

        with tempfile.TemporaryDirectory() as tmpdir:
            with self.assertRaises(ValueError):
                bootstrap.bootstrap_episode_packet(config, root=Path(tmpdir))

    def test_existing_packet_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            packet = root / "channel" / "episodes" / "s01e02-classroom-window-longplay"
            packet.mkdir(parents=True)

            with self.assertRaises(FileExistsError):
                bootstrap.bootstrap_episode_packet(self.config(), root=root)

    def test_s01e02_cli_preset_uses_roadmap_seed(self):
        args = bootstrap.parse_args(["--s01e02", "--dry-run", "--prepared-date", "2026-05-26"])
        config = bootstrap.config_from_args(args)

        self.assertEqual(config.episode_id, "s01e02-classroom-window-longplay")
        self.assertEqual(config.working_longplay, "Classroom Window Longplay")
        self.assertEqual(config.hook, "college classroom light, afternoon window")
        self.assertIn("almost-said", config.lyric_lane)


if __name__ == "__main__":
    unittest.main()
