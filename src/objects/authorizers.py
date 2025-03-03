from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By

import pickle
from time import sleep

from src.settings import Settings
from src.logger import logger


class UserAuthorizer:
    LOGIN_LINK = 'https://login.vk.com/?act=web_token'
    MESSENGER_LINK = 'https://vk.com/im'
    LOCAL_STORAGE_KEY = '6287487:web_token:login:auth'
    
    def __init__(self, headless: bool = True):
        options = ChromeOptions()
        
        if headless:
            options.add_argument('--headless')
            
        self.driver = Chrome(options=options)
        self.driver.implicitly_wait(30.0)
    
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
    
    def enter_password(self, password: str):
        div = self.driver.find_element(By.CLASS_NAME, 'vkc__Password__Wrapper')
        div.find_element(By.NAME, 'password').send_keys(password)
        
        div = self.driver.find_element(By.CLASS_NAME, 'vkc__EnterPasswordNoUserInfo__buttonWrap')
        div.find_element(By.TAG_NAME, 'button').click()
        
        sleep(4.0)
    
    def save_session_creds(self, creds_path: str = Settings.CREDS_PATH):
        creds = self.driver.execute_script(
            f'return JSON.parse(localStorage.getItem("{self.LOCAL_STORAGE_KEY}"));')
        self.driver.get(self.LOGIN_LINK)
        
        sleep(2.0)
        
        cookie = self.driver.get_cookies()
        
        logger.debug(f'Пойманые Cookie: {[x['name'] for x in cookie]}')
        logger.debug(f'Пойманный токен: {creds}')
        
        with open(creds_path + 'user_creds.pkl', 'wb') as file:
            pickle.dump(dict(cookie=cookie, access_token=creds['access_token']), file)
