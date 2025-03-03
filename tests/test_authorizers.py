import dotenv

import os
import unittest

from src.objects.authorizers import UserAuthorizer

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
        