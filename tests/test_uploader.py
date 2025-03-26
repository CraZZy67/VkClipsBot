import dotenv

import os
import unittest

from src.objects.uploader import VideoUploader
from src.my_exceptions import NoValidOwnPublicException, NoValidVideoPathException


class TestUploader(unittest.TestCase):
    
    @unittest.skip('При автономном тестировании будет флудить в группу.')
    def test_upload(self):
        dotenv.load_dotenv()
        
        VideoUploader().upload(own_public=os.getenv('OWN_TEST_PUBLIC_ID'),
                               inter_public=os.getenv('PUBLIC_ID_FOR_TEST'), 
                               video_id=os.getenv('VIDEO_ID_FOR_TEST'), headless=False)
        
        with self.assertRaises(NoValidOwnPublicException):
            VideoUploader().upload(own_public=os.getenv('NO_VALID_OWN_PUBLIC_ID_TEST'),
                                inter_public=os.getenv('PUBLIC_ID_FOR_TEST'), 
                                video_id=os.getenv('VIDEO_ID_FOR_TEST'), headless=False)
        
        with self.assertRaises(NoValidVideoPathException):
            VideoUploader().upload(own_public=os.getenv('OWN_TEST_PUBLIC_ID'),
                                inter_public=os.getenv('NO_VALID_PUBLIC_ID_FOR_TEST'), 
                                video_id=os.getenv('VIDEO_ID_FOR_TEST'), headless=False)
