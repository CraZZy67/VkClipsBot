import unittest
import dotenv

import os

from src.objects.video_queue import DebugVideoQueue
from src.my_exceptions import QueueLenException


class TestVideoQueue(unittest.TestCase):
    def test_main(self):
        dotenv.load_dotenv()
        
        ex = DebugVideoQueue(1)
        
        ex.add_video(os.getenv('VIDEO_ID_FOR_TEST'))
        ex.add_video(os.getenv('VIDEO_ID_FOR_TEST'))
        self.assertEqual(len(ex.queue), 2)
        
        ex.run_next_video(os.getenv('PUBLIC_ID_FOR_TEST'),
                          os.getenv('OWN_TEST_PUBLIC_ID'))
        
        ex.delete_video()
        self.assertEqual(len(ex.queue), 0)
    
    def test_stop(self):
        dotenv.load_dotenv()
        
        ex = DebugVideoQueue(1)
        
        ex.add_video(os.getenv('VIDEO_ID_FOR_TEST'))
        
        ex.run = False
        ex.run_next_video()
        
        print('Остановленно')
    
    def test_error(self):
        dotenv.load_dotenv()
        
        ex = DebugVideoQueue(1)
        
        with self.assertRaises(QueueLenException):
            ex.run_next_video(os.getenv('PUBLIC_ID_FOR_TEST'),
                              os.getenv('OWN_TEST_PUBLIC_ID'))
        with self.assertRaises(QueueLenException):
            ex.delete_video()
    
    def test_len(self):
        dotenv.load_dotenv()
        
        ex = DebugVideoQueue(1)
        
        [ex.add_video(os.getenv('VIDEO_ID_FOR_TEST')) for x in range(8)]
        
        self.assertEqual(len(ex.queue), 5)
        