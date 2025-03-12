import dotenv

import os
import unittest

from src.objects.interceptor import Interceptor


class TestInterceptor(unittest.TestCase):
    
    def test_intercept(self):
        dotenv.load_dotenv()
        
        inter = Interceptor(inter_public=os.getenv('PUBLIC_ID_FOR_TEST'))
        inter.intercept_video()