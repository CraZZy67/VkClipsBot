import dotenv
import unittest

import os

from src.objects.public import DebugPublic
from src.objects.interceptor import Interceptor
from src.objects.video_queue import DebugVideoQueue
from src.objects.collector import Collector
from src.my_exceptions import NoValidIdException, PublicsLenException


class TestCollector(unittest.TestCase): 
    
    def test_add_del_get(self):
        dotenv.load_dotenv()
        
        _interceptor = Interceptor(os.getenv('PUBLIC_ID_FOR_TEST'))
        _video_queue = DebugVideoQueue(1)
        public1 = DebugPublic(os.getenv('OWN_TEST_PUBLIC_ID'), _interceptor, _video_queue)
        
        _interceptor = Interceptor(os.getenv('PUBLIC_ID_FOR_TEST'))
        _video_queue = DebugVideoQueue(1)
        public2 = DebugPublic(os.getenv('OWN_TEST_PUBLIC_ID_SECOND'), _interceptor, _video_queue)
        
        collector = Collector(3)
        collector.add_public(public=public2, id='11')
        collector.add_public(public=public1, id='12')
        
        self.assertEqual(len(collector.publics), 2)
        
        collector.add_public(public=public2, id='13')
        
        with self.assertRaises(PublicsLenException):
            collector.add_public(public=public2, id='14')
        
        self.assertIsInstance(collector.get_public('12'), DebugPublic)
        
        collector.delete_public('11')
        
        with self.assertRaises(NoValidIdException):
            collector.add_public(public=public2, id='13')
        
        collector.delete_public('12')
        collector.delete_public('13')
        
        self.assertEqual(len(collector.publics), 0)
    
    def test_save_load_state(self):
        _interceptor = Interceptor(os.getenv('PUBLIC_ID_FOR_TEST'))
        _video_queue = DebugVideoQueue(1)
        public1 = DebugPublic(os.getenv('OWN_TEST_PUBLIC_ID'), _interceptor, _video_queue)
        
        _interceptor = Interceptor(os.getenv('PUBLIC_ID_FOR_TEST'))
        _video_queue = DebugVideoQueue(1)
        public2 = DebugPublic(os.getenv('OWN_TEST_PUBLIC_ID_SECOND'), _interceptor, _video_queue)
        
        collector = Collector(3)
        collector.add_public(public=public2, id='11')
        collector.add_public(public=public1, id='12')
        
        collector.save_state()
        
        collector.delete_public('11')
        
        collector.load_state()
        
        self.assertEqual(len(collector.publics), 2)
          