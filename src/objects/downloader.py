import requests

import os
import pickle
import json

from src.settings import Settings
from src.logger import down_logger
from src.my_exceptions import AccessDeniedException


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
    
    KEYS_LIST = ['payload', 1, 4, 'player', 'params', 0, 'url1080']
    
    settings = Settings()
    settings.HEADERS = Settings.HEADERS.copy()
    settings.HEADERS['referer'] = REFERER_LINK
    
    def refresh_creds(self):
        path = f'{self.settings.CREDS_PATH}/{self.settings.ANONYM_FILE_NAME}.pkl'
        with open(path, 'rb') as file:
            self.creds = pickle.load(file)
        
        self.jar = requests.cookies.RequestsCookieJar()
        [self.jar.set(x['name'], x['value']) for x in self.creds['cookie']]
        
    def download(self, video_id: str, public_id: str):
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
        
        for i in self.KEYS_LIST: response = response[i]

        response = requests.get(response, headers=self.settings.HEADERS)
        
        down_logger.debug(f'Заголовки ответа (video): {response.headers}')
        
        if not public_id in os.listdir('media/'):
            os.mkdir(f'media/{public_id}')
        
        path = f'{self.settings.VIDEO_PATH}/{public_id}/{video_id}.mp4'
        with open(path, 'wb') as file:
            file.write(response.content)
        