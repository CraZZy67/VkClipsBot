import requests

import os
import pickle
import json

from src.settings import Settings
from src.logger import down_logger
from src.my_exceptions import AccessDeniedException, NoFoundVideoException


class VideoDownloader:   
    DATA = {
        'act': 'show', 'al': '1',
        'autoplay': '0', 'module': 'public',
        'show_next': '1', 'al_ad': '0',
        'video': None, 'webcast': '0',
        'screen': '0'
    }
    URL = 'https://vk.com/al_video.php?act=show'
    REFERER_LINK = 'https://vk.com/improcom?from=groups'
    
    KEYS_LIST = ['payload', 1, 4, 'player', 'params', 0]
    QUALITY_KEYS = ['url720', 'url480', 'url360', 'url240', 'url144']
    
    settings = Settings()
    settings.HEADERS = Settings.HEADERS.copy()
    settings.HEADERS['referer'] = REFERER_LINK
    
    SL = settings.SLESH
    PREF_FL = settings.PREFIX_FILE
    PREF_DIR = settings.PREFIX_DIR
    
    def refresh_creds(self):
        path = f'{self.settings.CREDS_PATH}{self.settings.ANONYM_FILE_NAME}.pkl'
        with open(path, 'rb') as file:
            self.creds = pickle.load(file)
        
        self.jar = requests.cookies.RequestsCookieJar()
        [self.jar.set(x['name'], x['value']) for x in self.creds['cookie']]
        
    def download(self, video_id: str, public_id: str):
        down_logger.info('Загрузка видео.')
               
        self.refresh_creds()
        string_info = f'{public_id}_{video_id}'
        
        self.DATA['video'] = string_info
        
        response = requests.post(self.URL, data=self.DATA, 
                                 cookies=self.jar, headers=self.settings.HEADERS)
        
        down_logger.debug(f'Заголовки ответа (url): {response.headers}')
        down_logger.debug(f'Тело ответа (url): {response.text[:1000]}')
        
        response = response.text.replace('<!--', '')
        response = json.loads(response)
        
        if 'Ошибка доступа' in response['payload'][1][0]:
            raise AccessDeniedException
        
        if 'Видеозапись недоступна' in response['payload'][1][0]:
            raise NoFoundVideoException
        
        for i in self.KEYS_LIST: response = response[i]
        
        for i in self.QUALITY_KEYS:
            if i in response:
                response = response[i]
                break
            
        response = requests.get(response, headers=self.settings.HEADERS)
        
        down_logger.debug(f'Заголовки ответа (video): {response.headers}')
        
        if not f'{self.PREF_DIR}{public_id}' in os.listdir(self.settings.VIDEO_PATH):
            os.mkdir(f'{self.settings.VIDEO_PATH}{self.PREF_DIR}{public_id}')
        
        path = f'{self.settings.VIDEO_PATH}{self.PREF_DIR}{public_id}{self.SL}{self.PREF_FL}{video_id}.mp4'
        with open(path, 'wb') as file:
            file.write(response.content)
        