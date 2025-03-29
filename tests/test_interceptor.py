import dotenv

import os
import unittest

from src import objects
from src.my_exceptions import NoValidInterPublicException

class TestInterceptor(unittest.TestCase):
    
    def test_intercept(self):
        dotenv.load_dotenv()
        
        inter = objects.Interceptor(inter_public=os.getenv('PUBLIC_ID_FOR_TEST'))
        inter.intercept_video()
        
        inter = objects.Interceptor(inter_public=os.getenv('NO_VALID_PUBLIC_ID_FOR_TEST'))
        with self.assertRaises(NoValidInterPublicException):
            inter.intercept_video()
    
    @unittest.skip('Слишком длительный тест')
    def test_cycles(self):
        dotenv.load_dotenv()
        
        inter = objects.Interceptor(inter_public=os.getenv('PUBLIC_ID_FOR_CYCLE_TEST'))
        for i in range(50):
            print(f'Айди видео: {inter.intercept_video()}, номер: {i}')
            
        self.assertEqual(inter.cycles, 1)