import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PROJECT_ROOT / "scripts" / "youtube_api_video_upload.py"
RESOURCE_PATH = PROJECT_ROOT / "channel" / "episodes" / "s01e01-campus-cafe-longplay" / "source" / "youtube-video-resource.json"
spec = importlib.util.spec_from_file_location("youtube_api_video_upload", SCRIPT_PATH)
assert spec is not None and spec.loader is not None
uploader = importlib.util.module_from_spec(spec)
sys.modules["youtube_api_video_upload"] = uploader
spec.loader.exec_module(uploader)


class YoutubeApiVideoUploadTest(unittest.TestCase):
    def test_upload_resource_is_video_only_private_and_synthetic_disclosed(self):
        resource = uploader.load_video_resource(RESOURCE_PATH)

        self.assertEqual(resource["snippet"]["categoryId"], "10")
        self.assertEqual(resource["snippet"]["defaultLanguage"], "en")
        self.assertEqual(resource["status"]["privacyStatus"], "private")
        self.assertIs(resource["status"]["containsSyntheticMedia"], True)
        self.assertIs(resource["status"]["selfDeclaredMadeForKids"], False)
        self.assertNotIn("captions", resource)
        self.assertNotIn("thumbnail", resource)

    def test_plan_has_no_caption_or_thumbnail_operation(self):
        plan = uploader.build_upload_plan(
            expected_channel_id="UCEXPECTED",
            episode_id="s01e02-next-longplay",
            video_path=Path("candidates/s01e02-next-longplay/render/final.mp4"),
            resource_json=Path("channel/episodes/s01e02-next-longplay/source/youtube-video-resource.json"),
            metadata_source=Path("channel/episodes/s01e02-next-longplay/source/youtube-api-video-upload-package.md"),
            resource={"snippet": {"title": "Next"}, "status": {"privacyStatus": "private"}},
        )

        self.assertEqual(plan["operations"], ["channels.list(mine=true)", "videos.insert"])
        self.assertEqual(plan["expected_channel_id"], "UCEXPECTED")
        self.assertEqual(plan["episode_id"], "s01e02-next-longplay")
        self.assertEqual(plan["video_path"], "candidates/s01e02-next-longplay/render/final.mp4")
        self.assertTrue(plan["caption_upload_blocked"])
        self.assertTrue(plan["thumbnail_upload_blocked"])

    def test_execution_gate_open_is_private_video_only(self):
        plan = uploader.build_upload_plan(expected_channel_id="UCEXPECTED")
        gate = plan["execution_gate"]

        self.assertEqual(gate["status"], "open_private_video_upload_only")
        self.assertEqual(gate["allowed_operations"], ["channels.list(mine=true)", "videos.insert(private)"])
        self.assertIn("captions.insert", gate["blocked_operations"])
        self.assertIn("thumbnails.set", gate["blocked_operations"])
        self.assertIn("videos.update(public)", gate["blocked_operations"])
        self.assertIn("youtubeAnalytics.*", gate["blocked_operations"])
        self.assertIn("Content ID action", gate["blocked_operations"])
        self.assertFalse(gate["allows_caption_upload"])
        self.assertFalse(gate["allows_public_publish"])

    def test_execute_requires_expected_channel_id(self):
        with self.assertRaises(ValueError):
            uploader.validate_execute_preconditions(execute=True, expected_channel_id="")

    def test_load_external_env_file_for_execution_inputs(self):
        with tempfile.TemporaryDirectory(dir="/var/folders/_5/tcpqynxn5y34vhqy2v98xmxh0000gn/T/opencode") as tmpdir:
            temp_root = Path(tmpdir)
            env_file = temp_root / "mellow-youtube-channel.env"
            env_file.write_text(
                "MELLOW_YOUTUBE_EXPECTED_CHANNEL_ID=UCEXPECTED\n"
                f"MELLOW_YOUTUBE_CLIENT_SECRETS={temp_root / 'client_secret.json'}\n"
                f"MELLOW_YOUTUBE_TOKEN_CACHE={temp_root / 'youtube-token.json'}\n",
                encoding="utf-8",
            )

            values = uploader.load_env_file(env_file)

        self.assertEqual(values["expected_channel_id"], "UCEXPECTED")
        self.assertEqual(values["client_secrets"].name, "client_secret.json")
        self.assertEqual(values["token_cache"].name, "youtube-token.json")

    def test_env_file_inside_repo_is_rejected(self):
        with self.assertRaises(ValueError):
            uploader.load_env_file(PROJECT_ROOT / ".env")

    def test_cli_values_override_env_file_values(self):
        with tempfile.TemporaryDirectory(dir="/var/folders/_5/tcpqynxn5y34vhqy2v98xmxh0000gn/T/opencode") as tmpdir:
            temp_root = Path(tmpdir)
            env_file = temp_root / "mellow-youtube-channel.env"
            env_file.write_text(
                "MELLOW_YOUTUBE_EXPECTED_CHANNEL_ID=UCENV\n"
                f"MELLOW_YOUTUBE_CLIENT_SECRETS={temp_root / 'env_client.json'}\n"
                f"MELLOW_YOUTUBE_TOKEN_CACHE={temp_root / 'env_token.json'}\n",
                encoding="utf-8",
            )

            args = uploader.resolve_execution_inputs(
                uploader.parse_args([
                    "--env-file",
                    str(env_file),
                    "--expected-channel-id",
                    "UCCLI",
                ])
            )

        self.assertEqual(args.expected_channel_id, "UCCLI")
        self.assertEqual(args.client_secrets.name, "env_client.json")
        self.assertEqual(args.token_cache.name, "env_token.json")

    def test_channel_mismatch_blocks_upload(self):
        with self.assertRaises(ValueError):
            uploader.assert_expected_channel(actual_channel_id="UCACTUAL", expected_channel_id="UCEXPECTED")

    def test_video_resource_json_must_remain_private(self):
        with tempfile.TemporaryDirectory(dir="/var/folders/_5/tcpqynxn5y34vhqy2v98xmxh0000gn/T/opencode") as tmpdir:
            resource_json = Path(tmpdir) / "resource.json"
            resource_json.write_text(
                '{"snippet":{"title":"Bad"},"status":{"privacyStatus":"public"}}',
                encoding="utf-8",
            )

            with self.assertRaises(ValueError):
                uploader.load_video_resource(resource_json)


if __name__ == "__main__":
    unittest.main()
