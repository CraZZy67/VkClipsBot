import unittest

from tests import test_authorizer, test_downloader


suit = unittest.TestSuite()
suit.addTest(test_downloader.TestVideoDownloader('test_download'))

runner = unittest.TextTestRunner()
runner.run(suit)
