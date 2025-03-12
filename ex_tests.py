import unittest

from tests import test_authorizer, test_downloader, test_interceptor


suit = unittest.TestSuite()
suit.addTest(test_interceptor.TestInterceptor('test_intercept'))
# suit.addTest(test_authorizer.TestUserAuthorizer('test_anonym'))
# suit.addTest(test_downloader.TestVideoDownloader('test_download'))

runner = unittest.TextTestRunner()
runner.run(suit)
