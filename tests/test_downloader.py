import dotenv

import os
import unittest

from src.objects.downloader import VideoDownloader
from src.settings import Settings
from src.my_exceptions import NoFoundVideoException


class TestVideoDownloader(unittest.TestCase):
    settings = Settings()
    
    def test_download(self):
        dotenv.load_dotenv()
        
        video_id = os.getenv('VIDEO_ID_FOR_TEST')
        public_id = os.getenv('PUBLIC_ID_FOR_TEST')
        
        VideoDownloader().download(video_id=video_id, public_id=public_id)
        os.remove(f'./{self.settings.VIDEO_PATH}{public_id}/{video_id}.mp4')
        
        video_id = os.getenv('NO_VALID_VIDEO_ID_TEST')
        with self.assertRaises(NoFoundVideoException):
            VideoDownloader().download(video_id=video_id, public_id=public_id)
        