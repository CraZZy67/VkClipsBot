import dotenv
from selenium.webdriver import Chrome

import os
import unittest

from src.objects.authorizer import UserAuthorizer

class TestUserAuthorizer(unittest.TestCase):
    
    def test_main(self):
        dotenv.load_dotenv()
        
        authorizer = UserAuthorizer(headless=False)
        authorizer.send_verify_code(phone_number=os.getenv('NUMBER_FOR_TEST'))
        
        code = input('Код верификации: ')
        
        authorizer.enter_verify_code(verify_code=code)
        authorizer.enter_password(password=os.getenv('PASSWORD_FOR_TEST'))
        authorizer.save_session_creds()
        
        self.assertTrue(True)
    
    def test_anonym(self):
        driver = Chrome()
        driver.get('https://vk.com/icollbelgu')
        
        authorizer = UserAuthorizer(headless=False)
        
        authorizer.driver = driver
        authorizer.LOCAL_STORAGE_KEY = '6287487:get_anonym_token:login:auth'
        
        authorizer.save_session_creds(file_name='anonym_creds', out_session=True)