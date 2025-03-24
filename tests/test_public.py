import dotenv
import unittest

import os

from src.objects.public import DebugPublic
from src.objects.interceptor import Interceptor
from src.objects.video_queue import DebugVideoQueue
from src.my_exceptions import QueueLenException, NotFoundVideoException


class TestPublic(unittest.TestCase):
    
    def test_start(self):
        dotenv.load_dotenv()
        
        _interceptor = Interceptor(os.getenv('PUBLIC_ID_FOR_TEST'))
        _video_queue = DebugVideoQueue(1)
        
        public = DebugPublic(os.getenv('OWN_TEST_PUBLIC_ID'), _interceptor, _video_queue)
        public.start()
    
    def test_add(self):
        dotenv.load_dotenv()
        
        _interceptor = Interceptor(os.getenv('PUBLIC_ID_FOR_TEST'))
        _video_queue = DebugVideoQueue(1)
        
        public = DebugPublic(os.getenv('OWN_TEST_PUBLIC_ID'), _interceptor, _video_queue)
        
        with self.assertRaises(QueueLenException):
            [public.add_video(os.getenv('VIDEO_ID_FOR_TEST')) for x in range(6)]
        
        [public.video_queue.delete_video() for x in range(5)]
        
        with self.assertRaises(NotFoundVideoException):
            public.add_video(os.getenv('NO_VALID_VIDEO_ID_TEST'))
    
    def test_delete(self):
        dotenv.load_dotenv()
        
        _interceptor = Interceptor(os.getenv('PUBLIC_ID_FOR_TEST'))
        _video_queue = DebugVideoQueue(1)
        
        public = DebugPublic(os.getenv('OWN_TEST_PUBLIC_ID'), _interceptor, _video_queue)
        [public.add_video(os.getenv('VIDEO_ID_FOR_TEST')) for x in range(3)]
        
        public.delete_video()
        
        with self.assertRaises(QueueLenException):
            public.delete_video()