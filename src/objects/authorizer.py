from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import dotenv

import pickle
from time import sleep
import os

from src.settings import Settings
from src.logger import auth_logger
from src.my_exceptions import NoValidDataException


class UserAuthorizer:
    MESSENGER_LINK = 'https://vk.com/im'
    ANONYM_LINK = 'https://vk.com/icollbelgu'
    
    LOCAL_STORAGE_KEY = '6287487:web_token:login:auth'
    ANONYM_LOCAL_STORAGE_KEY = '6287487:get_anonym_token:login:auth'
    
    settings = Settings()
    
    def __init__(self, headless: bool = True):
        dotenv.load_dotenv()
        
        self.options = ChromeOptions()
        
        if os.getenv('PLATFORM') == 'Linux':
            self.options.add_argument('--headless')
            self.options.add_argument("--no-sandbox")
            self.options.add_argument("--disable-dev-shm-usage")
        elif headless:
            self.options.add_argument('--headless')
            
        self.driver = Chrome(options=self.options)
        self.driver.implicitly_wait(15.0)
    
    def send_verify_code(self, phone_number: str):
        self.driver.get(self.MESSENGER_LINK)
        
        button = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="enter-another-way"]')
        button.click()
        
        div = self.driver.find_element(By.CLASS_NAME, 'vkuiFormField__content')
        div.find_element(By.TAG_NAME, 'input').send_keys(phone_number)
        
        button = self.driver.find_element(By.CSS_SELECTOR, '[data-test-id="submit_btn"]')
        button.click()
    
    def enter_verify_code(self, verify_code: str):
        splited_code = list(verify_code)
        cells_input = self.driver.find_elements(By.NAME, 'otp-cell')
        
        for number, cell in zip(splited_code, cells_input):
            cell.send_keys(number)
        
        try:
            self.driver.find_element(By.CLASS_NAME, 'vkc__Password__Wrapper')
        except NoSuchElementException as ex:
            auth_logger.error(f'Перехват ошибки: {ex}')
            raise NoValidDataException
    
    def enter_password(self, password: str):
        div = self.driver.find_element(By.CLASS_NAME, 'vkc__Password__Wrapper')
        div.find_element(By.NAME, 'password').send_keys(password)
        
        div = self.driver.find_element(By.CLASS_NAME, 'vkc__EnterPasswordNoUserInfo__buttonWrap')
        div.find_element(By.TAG_NAME, 'button').click()
        
        try:
            self.driver.find_element(By.CSS_SELECTOR, '[data-testid="posting_create_post_button"]')
        except NoSuchElementException as ex:
            auth_logger.error(f'Перехват ошибки: {ex}')
            raise NoValidDataException
        
        sleep(2.0)
    
    def save_session_creds(self, file_name: str = Settings.USERS_FILE_NAME, out_session: bool = False):
        creds = self.driver.execute_script(
            f'return JSON.parse(localStorage.getItem("{self.LOCAL_STORAGE_KEY}"));')
        
        if not out_session:
            self.driver.get(self.settings.LOGIN_LINK)
            sleep(1.0)
        
        cookie = self.driver.get_cookies()
        
        auth_logger.debug(f'Пойманые Cookie: {[x['name'] for x in cookie]}')
        auth_logger.debug(f'Пойманный токен: {creds}')
        
        with open(Settings.CREDS_PATH + file_name + '.pkl', 'wb') as file:
            pickle.dump(dict(cookie=cookie, access_token=creds['access_token']), file)
        
        self.driver.quit()
    
    def refresh_anonym_token(self):
        try:
            auth_logger.info('Обновление анонимного токена.')
            
            self.driver.get(self.ANONYM_LINK)
            sleep(1.0)

            self.LOCAL_STORAGE_KEY = self.ANONYM_LOCAL_STORAGE_KEY

            self.save_session_creds(file_name=self.settings.ANONYM_FILE_NAME, out_session=True)
        finally:
            self.driver.quit()