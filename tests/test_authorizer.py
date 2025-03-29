import dotenv
from selenium.webdriver import Chrome

import os
import unittest

from src import objects
from src.my_exceptions import NoValidDataException

class TestUserAuthorizer(unittest.TestCase):
    
    @unittest.skip('Не возможно автономно тестировать')
    def test_main(self):
        dotenv.load_dotenv()
        
        authorizer = objects.UserAuthorizer()
        authorizer.send_verify_code(phone_number=os.getenv('NUMBER_FOR_TEST'))
        
        code = input('Код верификации: ')
        
        authorizer.enter_verify_code(verify_code=code)
        authorizer.enter_password(password=os.getenv('PASSWORD_FOR_TEST'))
        authorizer.save_session_creds()
    
    @unittest.skip('Не возможно автономно тестировать')    
    def test_error(self):
        authorizer = objects.UserAuthorizer()
        authorizer.send_verify_code(phone_number=os.getenv('NUMBER_FOR_TEST'))
        
        code = '24321'
        
        with self.assertRaises(NoValidDataException):
            authorizer.enter_verify_code(verify_code=code)
        
        authorizer = objects.UserAuthorizer(headless=False)
        authorizer.send_verify_code(phone_number=os.getenv('NUMBER_FOR_TEST'))
        
        code = input('Код верификации: ')
        
        authorizer.enter_verify_code(verify_code=code)
        with self.assertRaises(NoValidDataException):
            authorizer.enter_password(password=os.getenv('NO_VALID_PASSWORD_FOR_TEST'))
    
    def test_anonym(self):
        authorizer = objects.UserAuthorizer()
        authorizer.refresh_anonym_token()