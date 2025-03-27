import unittest

import asyncio

from src.objects.video_queue import VideoQueue
from src.objects.interceptor import Interceptor
from src.objects.public import Public

from tests import (test_authorizer, test_downloader, test_video_queue,
                   test_interceptor, test_uploader)


suit = unittest.TestSuite()

# suit.addTest(test_interceptor.TestInterceptor('test_cycles'))
# suit.addTest(test_interceptor.TestInterceptor('test_intercept'))

# suit.addTest(test_authorizer.TestUserAuthorizer('test_error'))
# suit.addTest(test_authorizer.TestUserAuthorizer('test_anonym'))

# suit.addTest(test_downloader.TestVideoDownloader('test_download'))

# suit.addTest(test_uploader.TestUploader('test_upload'))

# suit.addTest(test_video_queue.TestVideoQueue('test_main'))
# suit.addTest(test_video_queue.TestVideoQueue('test_stop'))
# suit.addTest(test_video_queue.TestVideoQueue('test_len'))
# suit.addTest(test_video_queue.TestVideoQueue('test_main'))

# runner = unittest.TextTestRunner()
# runner.run(suit)

async def test_async():
        ex = VideoQueue(1)
        ex2 = Interceptor('-203677279')
        pub = Public('club226910620', ex2, ex)
        await pub.start()

asyncio.run(test_async())