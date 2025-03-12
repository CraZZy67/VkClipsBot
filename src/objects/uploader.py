from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

import pickle
import time

from src.settings import Settings


class Uploader: 
    settings = Settings()
    
    DOMAIN = 'https://vk.com/'
    TIMEOUT = 300.0
    
    def upload(self, public_id: str, video_id: str, headless: bool = True):
        driver = self.get_driver(headless=headless)
        driver.get(self.DOMAIN + public_id)
        
        self.refresh_cookie(driver)
        driver.refresh()
        
        button = driver.find_element(By.CSS_SELECTOR, '[data_testid="posting_create_clip_button"]')
        button.click()
        
        input = driver.find_element(By.CSS_SELECTOR, '[multiple data-testid="video_upload_select_file"]')
        input.send_keys(f'{self.settings.VIDEO_PATH}{public_id}/{video_id}.mp4')
        
        button = driver.find_element(By.CSS_SELECTOR, '[data-testid="clips-uploadForm-publish-button"]')
        
        wait = WebDriverWait(driver, timeout=self.TIMEOUT)
        wait.until('vkui-focus-visible' in button.get_property('class'))
        
        button.click()
        time.sleep(2.0)
        
        driver.quit()
         
    def get_driver(self, headless: bool) -> Chrome:
        options = ChromeOptions()
        
        if headless:
            options.add_argument('--headless')
            
        driver = Chrome(options=options)
        driver.implicitly_wait(30.0)
        
        return driver
        
    def refresh_cookie(self, driver: Chrome):
        path = f'{self.settings.CREDS_PATH}/{self.settings.USERS_FILE_NAME}.pkl'
        with open(path, 'rb') as file:
            self.creds = pickle.load(file)
        
        [driver.add_cookie(x['name'], x['value']) for x in self.creds['cookie']]
        