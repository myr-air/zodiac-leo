import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = PROJECT_ROOT / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

COMMENT_SCRIPT = SCRIPT_DIR / "youtube_api_comment.py"
spec = importlib.util.spec_from_file_location("youtube_api_comment", COMMENT_SCRIPT)
assert spec is not None and spec.loader is not None
comment_helper = importlib.util.module_from_spec(spec)
sys.modules["youtube_api_comment"] = comment_helper
spec.loader.exec_module(comment_helper)


class YoutubeApiCommentTest(unittest.TestCase):
    def test_comment_insert_plan_is_comment_only_and_pin_blocked(self):
        plan = comment_helper.build_comment_insert_plan(
            expected_channel_id="UCEXPECTED",
            video_id="VIDEO123",
            comment_text="What little after-school detail should we make next?",
            episode_id="s01e02-next-longplay",
            comment_source=Path("channel/episodes/s01e02-next-longplay/source/metadata.md"),
        )

        self.assertEqual(
            plan["operations"],
            [
                "channels.list(mine=true)",
                "commentThreads.list(top-level duplicate guard)",
                "commentThreads.insert(top-level)",
            ],
        )
        self.assertEqual(plan["expected_channel_id"], "UCEXPECTED")
        self.assertEqual(plan["video_id"], "VIDEO123")
        self.assertEqual(plan["episode_id"], "s01e02-next-longplay")
        self.assertTrue(plan["api_comment_post_allowed_after_gate"])
        self.assertFalse(plan["api_comment_pin_supported"])
        self.assertFalse(plan["force_repost"])
        self.assertIn("duplicate", plan["duplicate_comment_guard"])
        self.assertIn("comment pinning", plan["blocked_operations"])
        self.assertIn("videos.insert", plan["blocked_operations"])
        self.assertIn("thumbnails.set", plan["blocked_operations"])
        self.assertIn("youtubeAnalytics.*", plan["blocked_operations"])

    def test_comment_execute_requires_video_id_and_text(self):
        with self.assertRaises(ValueError):
            comment_helper.validate_comment_execute_preconditions(
                execute=True,
                expected_channel_id="UCEXPECTED",
                video_id="",
                comment_text="hello",
            )

        with self.assertRaises(ValueError):
            comment_helper.validate_comment_execute_preconditions(
                execute=True,
                expected_channel_id="UCEXPECTED",
                video_id="VIDEO123",
                comment_text="",
            )

    def test_comment_env_file_loads_video_id_comment_file_and_rejects_repo_path(self):
        with tempfile.TemporaryDirectory(dir=None) as tmpdir:
            temp_root = Path(tmpdir)
            comment_file = temp_root / "comment.txt"
            env_file = temp_root / "comment.env"
            env_file.write_text(
                "MELLOW_YOUTUBE_EXPECTED_CHANNEL_ID=UCEXPECTED\n"
                "MELLOW_YOUTUBE_VIDEO_ID=VIDEO123\n"
                f"MELLOW_YOUTUBE_COMMENT_FILE={comment_file}\n"
                f"MELLOW_YOUTUBE_CLIENT_SECRETS={temp_root / 'client_secret.json'}\n"
                f"MELLOW_YOUTUBE_TOKEN_CACHE={temp_root / 'youtube-token.json'}\n",
                encoding="utf-8",
            )

            values = comment_helper.load_comment_env_file(env_file)

        self.assertEqual(values["expected_channel_id"], "UCEXPECTED")
        self.assertEqual(values["video_id"], "VIDEO123")
        self.assertEqual(values["comment_file"], comment_file)

        with self.assertRaises(ValueError):
            comment_helper.load_comment_env_file(PROJECT_ROOT / ".env")

    def test_comment_env_file_expands_environment_variables_in_paths(self):
        with tempfile.TemporaryDirectory(dir=None) as tmpdir:
            temp_root = Path(tmpdir)
            env_file = temp_root / "comment.env"
            os.environ["MELLOW_TEST_SECRET_ROOT"] = str(temp_root)
            env_file.write_text(
                "MELLOW_YOUTUBE_EXPECTED_CHANNEL_ID=UCEXPECTED\n"
                "MELLOW_YOUTUBE_VIDEO_ID=VIDEO123\n"
                "MELLOW_YOUTUBE_COMMENT_FILE=$MELLOW_TEST_SECRET_ROOT/comment.txt\n"
                "MELLOW_YOUTUBE_CLIENT_SECRETS=$MELLOW_TEST_SECRET_ROOT/client_secret.json\n"
                "MELLOW_YOUTUBE_TOKEN_CACHE=$MELLOW_TEST_SECRET_ROOT/youtube-token.json\n",
                encoding="utf-8",
            )

            values = comment_helper.load_comment_env_file(env_file)

        self.assertEqual(values["comment_file"], temp_root / "comment.txt")
        self.assertEqual(values["client_secrets"], temp_root / "client_secret.json")
        self.assertEqual(values["token_cache"], temp_root / "youtube-token.json")

    def test_read_comment_text_prefers_inline_and_reads_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            comment_file = Path(tmpdir) / "comment.txt"
            comment_file.write_text("  file comment  \n", encoding="utf-8")

            self.assertEqual(comment_helper.read_comment_text("  inline comment  ", comment_file), "inline comment")
            self.assertEqual(comment_helper.read_comment_text("", comment_file), "file comment")

    def test_find_existing_channel_comment_detects_same_text_from_authenticated_channel(self):
        youtube = FakeYouTubeCommentList(
            [
                {
                    "id": "THREAD1",
                    "snippet": {
                        "topLevelComment": {
                            "id": "COMMENT1",
                            "snippet": {
                                "authorChannelId": {"value": "UCEXPECTED"},
                                "textOriginal": "Thanks\nfor listening",
                            },
                        }
                    },
                }
            ]
        )

        match = comment_helper.find_existing_channel_comment(
            youtube,
            channel_id="UCEXPECTED",
            video_id="VIDEO123",
            comment_text="Thanks\nfor listening",
        )

        self.assertEqual(match["comment_thread_id"], "THREAD1")
        self.assertEqual(match["comment_id"], "COMMENT1")

    def test_find_existing_channel_comment_ignores_other_channels(self):
        youtube = FakeYouTubeCommentList(
            [
                {
                    "id": "THREAD1",
                    "snippet": {
                        "topLevelComment": {
                            "id": "COMMENT1",
                            "snippet": {
                                "authorChannelId": {"value": "UCOTHER"},
                                "textOriginal": "same comment",
                            },
                        }
                    },
                }
            ]
        )

        self.assertIsNone(
            comment_helper.find_existing_channel_comment(
                youtube,
                channel_id="UCEXPECTED",
                video_id="VIDEO123",
                comment_text="same comment",
            )
        )

    def test_comment_scopes_include_force_ssl_for_insert_and_readonly_for_channel_check(self):
        self.assertIn("https://www.googleapis.com/auth/youtube.force-ssl", comment_helper.COMMENT_SCOPES)
        self.assertIn("https://www.googleapis.com/auth/youtube.readonly", comment_helper.COMMENT_SCOPES)


class FakeYouTubeCommentList:
    def __init__(self, items):
        self.items = items

    def commentThreads(self):
        return self

    def list(self, **kwargs):
        self.last_list_kwargs = kwargs
        return self

    def execute(self):
        return {"items": self.items}


if __name__ == "__main__":
    unittest.main()
