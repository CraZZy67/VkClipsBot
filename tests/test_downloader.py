import dotenv

import os
import unittest

from src.objects.downloader import VideoDownloader

class TestVideoDownloader(unittest.TestCase):
    
    def test_download(self):
        dotenv.load_dotenv()
        
        video_id = os.getenv('VIDEO_ID_FOR_TEST')
        public_id = os.getenv('PUBLIC_ID_FOR_TEST')
        
        VideoDownloader().download(video_id=video_id, public_id=public_id)
        