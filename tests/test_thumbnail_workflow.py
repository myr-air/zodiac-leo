import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = PROJECT_ROOT / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

THUMBNAIL_SCRIPT = SCRIPT_DIR / "create_layered_thumbnail.py"
thumb_spec = importlib.util.spec_from_file_location("create_layered_thumbnail", THUMBNAIL_SCRIPT)
assert thumb_spec is not None and thumb_spec.loader is not None
thumbnail = importlib.util.module_from_spec(thumb_spec)
sys.modules["create_layered_thumbnail"] = thumbnail
thumb_spec.loader.exec_module(thumbnail)

UPLOAD_SCRIPT = SCRIPT_DIR / "youtube_api_thumbnail.py"
upload_spec = importlib.util.spec_from_file_location("youtube_api_thumbnail", UPLOAD_SCRIPT)
assert upload_spec is not None and upload_spec.loader is not None
thumbnail_upload = importlib.util.module_from_spec(upload_spec)
sys.modules["youtube_api_thumbnail"] = thumbnail_upload
upload_spec.loader.exec_module(thumbnail_upload)


class ThumbnailWorkflowTest(unittest.TestCase):
    def test_layered_thumbnail_s01e01_generation(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_root = Path(tmpdir)
            background = temp_root / "bg.png"
            output = temp_root / "thumbnail_s01e01.png"
            Image.new("RGB", (1672, 941), (220, 190, 150)).save(background)

            thumbnail.process_episode("s01e01", background, output)

            with Image.open(output) as result:
                self.assertEqual(result.size, (1280, 720))

    def test_layered_thumbnail_s01e02_generation(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_root = Path(tmpdir)
            background = temp_root / "bg.png"
            output = temp_root / "thumbnail_s01e02.png"
            Image.new("RGB", (1672, 941), (220, 190, 150)).save(background)

            thumbnail.process_episode("s01e02", background, output)

            with Image.open(output) as result:
                self.assertEqual(result.size, (1280, 720))

    def test_layered_thumbnail_s01e03_generation(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_root = Path(tmpdir)
            background = temp_root / "bg.png"
            output = temp_root / "thumbnail_s01e03.png"
            Image.new("RGB", (1672, 941), (220, 190, 150)).save(background)

            thumbnail.process_episode("s01e03", background, output)

            with Image.open(output) as result:
                self.assertEqual(result.size, (1280, 720))

    def test_thumbnail_upload_plan_is_thumbnail_only(self):
        plan = thumbnail_upload.build_thumbnail_upload_plan(
            expected_channel_id="UCEXPECTED",
            video_id="VIDEO123",
            episode_id="s01e02-next-longplay",
            thumbnail_path=Path("candidates/s01e02-next-longplay/thumbnail/final.png"),
            thumbnail_source=Path("channel/episodes/s01e02-next-longplay/source/youtube-api-thumbnail-upload-package.md"),
        )

        self.assertEqual(plan["operations"], ["channels.list(mine=true)", "thumbnails.set"])
        self.assertEqual(plan["expected_channel_id"], "UCEXPECTED")
        self.assertEqual(plan["video_id"], "VIDEO123")
        self.assertEqual(plan["episode_id"], "s01e02-next-longplay")
        self.assertEqual(plan["thumbnail_path"], "candidates/s01e02-next-longplay/thumbnail/final.png")
        self.assertTrue(plan["thumbnail_upload_allowed"])
        self.assertIn("videos.insert", plan["blocked_operations"])
        self.assertIn("captions.insert", plan["blocked_operations"])
        self.assertIn("videos.update(public)", plan["blocked_operations"])

    def test_thumbnail_upload_requires_video_id(self):
        with self.assertRaises(ValueError):
            thumbnail_upload.validate_thumbnail_execute_preconditions(
                execute=True,
                expected_channel_id="UCEXPECTED",
                video_id="",
            )

    def test_thumbnail_env_file_loads_video_id_and_rejects_repo_path(self):
        with tempfile.TemporaryDirectory(dir=None) as tmpdir:
            temp_root = Path(tmpdir)
            env_file = temp_root / "thumbnail.env"
            env_file.write_text(
                "MELLOW_YOUTUBE_EXPECTED_CHANNEL_ID=UCEXPECTED\n"
                "MELLOW_YOUTUBE_VIDEO_ID=VIDEO123\n"
                f"MELLOW_YOUTUBE_CLIENT_SECRETS={temp_root / 'client_secret.json'}\n"
                f"MELLOW_YOUTUBE_TOKEN_CACHE={temp_root / 'youtube-token.json'}\n",
                encoding="utf-8",
            )

            values = thumbnail_upload.load_thumbnail_env_file(env_file)

        self.assertEqual(values["expected_channel_id"], "UCEXPECTED")
        self.assertEqual(values["video_id"], "VIDEO123")

        with self.assertRaises(ValueError):
            thumbnail_upload.load_thumbnail_env_file(PROJECT_ROOT / ".env")

    def test_thumbnail_env_file_expands_environment_variables_in_paths(self):
        with tempfile.TemporaryDirectory(dir=None) as tmpdir:
            temp_root = Path(tmpdir)
            env_file = temp_root / "thumbnail.env"
            os.environ["MELLOW_TEST_SECRET_ROOT"] = str(temp_root)
            env_file.write_text(
                "MELLOW_YOUTUBE_EXPECTED_CHANNEL_ID=UCEXPECTED\n"
                "MELLOW_YOUTUBE_VIDEO_ID=VIDEO123\n"
                "MELLOW_YOUTUBE_CLIENT_SECRETS=$MELLOW_TEST_SECRET_ROOT/client_secret.json\n"
                "MELLOW_YOUTUBE_TOKEN_CACHE=$MELLOW_TEST_SECRET_ROOT/youtube-token.json\n",
                encoding="utf-8",
            )

            values = thumbnail_upload.load_thumbnail_env_file(env_file)

        self.assertEqual(values["client_secrets"], temp_root / "client_secret.json")
        self.assertEqual(values["token_cache"], temp_root / "youtube-token.json")


if __name__ == "__main__":
    unittest.main()
