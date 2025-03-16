import dotenv

import os
import unittest

from src.objects.uploader import Uploader


class TestUploader(unittest.TestCase):
    def test_upload(self):
        dotenv.load_dotenv()
        
        Uploader().upload(own_public_id=os.getenv('OWN_TEST_PUBLIC_ID'),
                          inter_public_id=os.getenv('PUBLIC_ID_FOR_TEST'), 
                          video_id=os.getenv('VIDEO_ID_FOR_TEST'), headless=False)
