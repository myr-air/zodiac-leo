import importlib.util
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = PROJECT_ROOT / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

FLOW_SCRIPT = SCRIPT_DIR / "episode_hil_flow.py"
spec = importlib.util.spec_from_file_location("episode_hil_flow", FLOW_SCRIPT)
assert spec is not None and spec.loader is not None
episode_hil_flow = importlib.util.module_from_spec(spec)
sys.modules["episode_hil_flow"] = episode_hil_flow
spec.loader.exec_module(episode_hil_flow)


class EpisodeHilFlowSourceQualityTest(unittest.TestCase):
    def test_prompt_control_gate_flags_thin_suno_pack(self):
        issues = episode_hil_flow._detect_prompt_control_issues(
            Path("01-thin.md"),
            "[Verse]\nA line about a room\n[Chorus]\nA line about a feeling",
            "cozy chill vocal, soft R&B, warm keys, approx. 82 BPM",
            "trap, hard rock",
        )

        self.assertTrue(any("Lyrics missing pre-song context/control section" in issue for issue in issues))
        self.assertTrue(any("Lyrics start directly with song section" in issue for issue in issues))
        self.assertTrue(any("Styles missing control groups" in issue for issue in issues))
        self.assertTrue(any("Exclude Styles missing drift guards" in issue for issue in issues))

    def test_prompt_control_gate_accepts_richer_custom_mode_source(self):
        lyrics = """[Song Context]
Quiet bookstore first-love moment, restrained and close, no invented lyric changes.

[Vocal Direction]
Natural adult female vocal, close and calm, no childlike tone.

[Arrangement Map]
Eight-bar intro, verse-led first minute, chorus lift after verse two, short bridge, clean outro.

[Duration Target]
Full-length three-minute song, do not end before 3:00.

[Verse 1]
The receipt folds once beside the register
Your thumb keeps the corner from flying

[Chorus]
Stay near the counter when the rain lets go
We can read the weather without trying
"""
        styles = (
            "soft R&B, mellow city-pop, natural adult female vocal, approx. 84 BPM, "
            "warm electric keys, clean guitar, rounded bass, soft brushed drums, airy pads, "
            "verse-led arrangement arc with restrained chorus lift and short bridge, close-mic warm mix, "
            "full-length 3:05 target"
        )
        exclude = (
            "named-artist imitation, known-song imitation, auto-generated lyrics, lyric rewrite, "
            "random vocalist, childlike vocal, under 3 minutes, short sketch, abrupt ending, trap, EDM drop"
        )

        issues = episode_hil_flow._detect_prompt_control_issues(Path("01-rich.md"), lyrics, styles, exclude)

        self.assertEqual(issues, [])


if __name__ == "__main__":
    unittest.main()
