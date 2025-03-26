import unittest

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

runner = unittest.TextTestRunner()
runner.run(suit)
