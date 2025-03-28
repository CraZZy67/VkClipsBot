import requests
import dotenv

import pickle
from time import sleep
import os

from src.objects.downloader import VideoDownloader
from src.settings import Settings
from src.logger import inter_logger
from src.my_exceptions import AccessDeniedException, NoValidInterPublicException


class Interceptor:
    ANONYM_ID = '6287487'
    DATA = {
        'owner_id': None, 
        'fields': 'about,description,followers_count,is_closed,verified,screen_name,friend_status,is_subscribed,blacklisted,domain,sex,can_write_private_message,first_name_gen,last_name_gen,first_name_acc,is_nft_photo,admin_level,member_status,members_count,is_member,ban_info,can_message',
        'count': None,
        'access_token': None
    }
    URL = 'https://api.vk.com/method/shortVideo.getOwnerVideos?v=5.246&client_id={anonym_id}'
    
    settings = Settings()
    settings.HEADERS = Settings.HEADERS.copy()
    settings.HEADERS['accept-language'] = 'ru-RU,ru;q=0.9'
    settings.HEADERS['referer'] = 'https://vk.com/'
    settings.HEADERS['Accept-Encoding'] = 'gzip, deflate, br'
    settings.HEADERS.pop('x-requested-with')
    
    DOWNLOADER = VideoDownloader()
    
    def __init__(self, inter_public: str):
        self.inter_public = inter_public
        self.inted_video = list()

        self.cycles = int()
            
    def intercept_video(self) -> int:
        count = 10
        
        try:
            video_count = self.get_json()['response']['count']
        except KeyError:
            raise AccessDeniedException
        
        if not video_count: raise NoValidInterPublicException
        
        while True:
            ids = self.get_video_ids(count=str(count))
            sleep(1.0)
            
            for i in ids:
                if not i in self.inted_video:
                    inter_logger.debug(f'Видео которое будет загружено: {i}')
                    
                    self.DOWNLOADER.download(public_id=self.inter_public, video_id=i)
                    self.inted_video.append(i)
                    return i
            
            count += 10
            
            if video_count - count < 0:
                self.cycles += 1
                self.inted_video = list()
                count = 10       
                
    def get_video_ids(self, count: str) -> list:
        try:
            response = self.get_json(count=count)['response']
        except KeyError:
            raise AccessDeniedException
        
        ids = list()
        
        for i in response['items']:
            ids.append(i['id'])
        return ids
    
    def get_json(self, count: str = '1') -> dict:
        self.refresh_creds()
        
        self.DATA['owner_id'] = self.inter_public
        self.DATA['count'] = count
        self.DATA['access_token'] = self.creds['access_token']
        
        response = requests.post(url=self.URL.format(anonym_id=self.ANONYM_ID), 
                                 headers=self.settings.HEADERS, data=self.DATA,
                                 cookies=self.jar)
        
        inter_logger.debug(f'Заголовки ответа: {response.headers}')
        inter_logger.debug(f'Тело ответа: {response.text[:1000]}')
        
        return response.json()
    
    def refresh_creds(self):
        dotenv.load_dotenv()

        sl = os.getenv('SLESH')
        
        path = f'{self.settings.CREDS_PATH}{sl}{self.settings.ANONYM_FILE_NAME}.pkl'
        with open(path, 'rb') as file:
            self.creds = pickle.load(file)
            
        self.jar = requests.cookies.RequestsCookieJar()
        [self.jar.set(x['name'], x['value']) for x in self.creds['cookie']]