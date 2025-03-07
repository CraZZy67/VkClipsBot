import requests

import os
import pickle
from abc import ABC, abstractmethod

from src.settings import Settings


class Downloader(ABC):
    
    @abstractmethod
    def download(self, video_id: str, public_id: str) -> str:
        pass

class VideoDownloader(Downloader):   
    DATA = {
        'act': 'show', 'al': '1',
        'autoplay': '0', 'module': 'public',
        'show_next': '1', 'al_ad': '0',
        'video': None, 'webcast': '0',
        'screen': '0'
    }
    URL = 'https://vk.com/al_video.php?act=show'
    REFERER_LINK = 'https://vk.com/improcom?from=groups&z=clip'
    
    KEYS_LIST = ['payload', 1, 4, 'player', 'params', 0, 'url1080']
    
    def __init__(self):
        path = f'{Settings.CREDS_PATH}/{Settings.ANONYM_FILE_NAME}.pkl'
        with open(path, 'rb') as file:
            self.creds = pickle.load(file)
        
        self.jar = requests.cookies.RequestsCookieJar()
        [self.jar.set(x['name'], x['value']) for x in self.creds['cookie']]
        
    def download(self, video_id: str, public_id: str):
        string_info = f'{public_id}_{video_id}'
        
        self.DATA['video'] = string_info
        Settings.HEADERS['referer'] = self.REFERER_LINK + string_info
        
        response = requests.post(self.URL, data=self.DATA, 
                                 cookies=self.jar, headers=Settings.HEADERS).json()
        for i in self.KEYS_LIST: response = response[i]

        response = requests.get(response, headers=Settings.HEADERS)
        if not public_id in os.listdir('media/'):
            os.mkdir(f'media/{public_id}')
        
        path = f'{Settings.VIDEO_PATH}/{public_id}/{video_id}.mp4'
        with open(path, 'wb') as file:
            file.write(response.content)
        