import dotenv
import unittest

import os

from src import objects
from src.my_exceptions import QueueLenException


class TestPublic(unittest.TestCase):
    
    @unittest.skip('Автономное тестирование без асинхронной функции не возможно')
    def test_start(self):
        dotenv.load_dotenv()
        
        _interceptor = objects.Interceptor(os.getenv('PUBLIC_ID_FOR_TEST'))
        _video_queue = objects.DebugVideoQueue(1)
        
        public = objects.DebugPublic(os.getenv('OWN_TEST_PUBLIC_ID'), _interceptor, _video_queue)
        public.start()
    
    def test_add(self):
        dotenv.load_dotenv()
        
        _interceptor = objects.Interceptor(os.getenv('PUBLIC_ID_FOR_TEST'))
        _video_queue = objects.DebugVideoQueue(1)
        
        public = objects.DebugPublic(os.getenv('OWN_TEST_PUBLIC_ID'), _interceptor, _video_queue)
        
        with self.assertRaises(QueueLenException):
            [public.add_video(os.getenv('VIDEO_ID_FOR_TEST')) for x in range(6)]
        
        [public.video_queue.delete_video() for x in range(5)]
        
    
    def test_delete(self):
        dotenv.load_dotenv()
        
        _interceptor = objects.Interceptor(os.getenv('PUBLIC_ID_FOR_TEST'))
        _video_queue = objects.DebugVideoQueue(1)
        
        public = objects.DebugPublic(os.getenv('OWN_TEST_PUBLIC_ID'), _interceptor, _video_queue)
        [public.add_video(os.getenv('VIDEO_ID_FOR_TEST')) for x in range(3)]
        
        public.delete_video()
        
        with self.assertRaises(QueueLenException):
            public.delete_video()