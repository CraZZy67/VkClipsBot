import requests

import pickle

from abc import ABC, abstractmethod

import requests.cookies
from src.settings import Settings


class Downloader(ABC):
    SITE_PATH: str
    
    @abstractmethod
    def download(self, video_id: str, public_id: str) -> str:
        pass

class VideoDownloader(Downloader):   
    DATA = {
        'act': 'show', 'al': '1',
        'autoplay': '0', 'module': 'clips_item',
        'screen': '0', 'show_next': '1',
        'video': None, 'webcast': '0'
    }
    URL = 'https://vk.com/al_video.php?act=show'
    KEYS_LIST = ['payload', 1, 4, 'player', 'params', 0]
    
    def __init__(self):
        with open(f'{Settings.CREDS_PATH}/{Settings.ANONYM_FILE_NAME}.pkl', 'rb') as file:
            self.creds = pickle.load(file)
        
    def download(self, video_id: str, public_id: str):
        jar = requests.cookies.RequestsCookieJar()
        [jar.set(x['name'], x['value']) for x in self.creds['cookie']]
        
        self.DATA['video'] = f'{public_id}_{video_id}'
        
        response = requests.get(self.URL, data=self.DATA, cookies=jar).json()
        for i in self.KEYS_LIST: response = response[i]
        
        requests.get(response.replace('\\', ''))
        
        