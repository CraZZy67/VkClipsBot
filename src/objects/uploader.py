from selenium.webdriver import Chrome, ChromeOptions, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, InvalidArgumentException

import dotenv

import pickle
import time
import os

from src.settings import Settings
from src.logger import upload_logger
import src.my_exceptions as my_exceptions


class VideoUploader: 
    settings = Settings()
    
    DOMAIN = 'https://vk.com/'
    TIMEOUT = 500.0
    
    SL = settings.SLESH
    PREF_DIR = settings.PREFIX_DIR
    
    def upload(self, own_public: str, inter_public: str, video_id: str, headless: bool = True):
        try: 
            upload_logger.info('Выгрузка видео.')
            driver = self.get_driver(headless=headless)
            driver.get(self.DOMAIN + own_public)
            
            self.refresh_cookie(driver)
            driver.get(self.DOMAIN + own_public)
            
            upload_logger.debug(f'Cookie на текущей странице: {[(x['name'], x['domain']) for x in driver.get_cookies()]}')
            
            try:
                button = driver.find_element(By.CSS_SELECTOR, '[data-testid="posting_create_clip_button"]')
            except NoSuchElementException as ex:
                upload_logger.error(f'Перехват ошибки: {ex}')
                raise my_exceptions.NoValidOwnPublicException
                
            button.click()
            
            input = driver.find_element(By.CSS_SELECTOR, '[data-testid="video_upload_select_file"]')
            file_path = f'{os.getenv('WORK_DIR_ABS_PATH')}{self.settings.VIDEO_PATH}{self.PREF_DIR}{inter_public}{self.SL}{video_id}.mp4'
            try:
                input.send_keys(file_path)
            except InvalidArgumentException as ex:
                upload_logger.error(f'Перехват ошибки: {ex}')
                raise my_exceptions.NoValidVideoPathException
            
            time.sleep(3)
            
            status = driver.find_element(By.XPATH, '//*[@id="spa_root"]/div/section/div[3]/div[1]/div/div[2]/div/div')
            if not status.text == 'Клип загружен. Обработка...': raise my_exceptions.StatusIsRed
            
            button = driver.find_element(By.CSS_SELECTOR, '[data-testid="clips-uploadForm-publish-button"]')
            wait = WebDriverWait(driver, timeout=self.TIMEOUT)
            
            try:
                wait.until(lambda _ : button.is_enabled())
            except StaleElementReferenceException:
                button = driver.find_element(By.CSS_SELECTOR, '[data-testid="clips-uploadForm-publish-button"]')
                ActionChains(driver=driver).click(button).perform()
                
                time.sleep(1.0)
            
        finally:
            driver.quit()
         
    def get_driver(self, headless: bool) -> Chrome:
        dotenv.load_dotenv()
        
        self.options = ChromeOptions()
        
        if os.getenv('PLATFORM') == 'Linux':
            service = Service(f'{os.getenv('WORK_DIR_ABS_PATH')}chromedriver', port=os.getenv('PORT'))
        else:
            service = Service(port=os.getenv('PORT'))
        
        if os.getenv('PLATFORM') == 'Linux':
            self.options.add_argument('start-maximized')
            self.options.add_argument('enable-automation')
            self.options.add_argument('--headless')
            self.options.add_argument('--no-sandbox')
            self.options.add_argument('--disable-dev-shm-usage')
            self.options.add_argument('--disable-browser-side-navigation')
            self.options.add_argument('--disable-gpu')
        elif headless:
            self.options.add_argument('--headless')
          
        driver = Chrome(options=self.options, service=service)
        driver.implicitly_wait(15.0)
        driver.set_window_size(1200, 850)
        driver.command_executor.set_timeout(360)
        
        return driver
        
    def refresh_cookie(self, driver: Chrome):
        path = f'{self.settings.CREDS_PATH}{self.settings.USERS_FILE_NAME}.pkl'
        with open(path, 'rb') as file:
            self.creds = pickle.load(file)
            
        driver.delete_all_cookies()
        
        self.add_certain_cookie(excepted_domain='.login.vk.com', driver=driver)
                
        driver.get(self.settings.LOGIN_LINK)
        time.sleep(1.0)
        
        self.add_certain_cookie(excepted_domain='.vk.com', driver=driver)
        
    def add_certain_cookie(self, excepted_domain: str, driver: Chrome):
        for cookie in self.creds['cookie']:
            if cookie['domain'] != excepted_domain:
                driver.add_cookie({'name': cookie['name'], 'value': cookie['value'], 'domain': cookie['domain']})