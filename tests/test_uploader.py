import dotenv

import os
import unittest

from src import objects
from src.my_exceptions import NoValidOwnPublicException, NoValidVideoPathException


class TestUploader(unittest.TestCase):
    
    @unittest.skip('При автономном тестировании будет флудить в группу.')
    def test_upload(self):
        dotenv.load_dotenv()
        
        objects.VideoUploader().upload(own_public=os.getenv('OWN_TEST_PUBLIC_ID'),
                               inter_public=os.getenv('PUBLIC_ID_FOR_TEST'), 
                               video_id=os.getenv('VIDEO_ID_FOR_TEST'))
        
        with self.assertRaises(NoValidOwnPublicException):
            objects.VideoUploader().upload(own_public=os.getenv('NO_VALID_OWN_PUBLIC_ID_TEST'),
                                inter_public=os.getenv('PUBLIC_ID_FOR_TEST'), 
                                video_id=os.getenv('VIDEO_ID_FOR_TEST'))
        
        with self.assertRaises(NoValidVideoPathException):
            objects.VideoUploader().upload(own_public=os.getenv('OWN_TEST_PUBLIC_ID'),
                                inter_public=os.getenv('NO_VALID_PUBLIC_ID_FOR_TEST'), 
                                video_id=os.getenv('VIDEO_ID_FOR_TEST'))
