import requests

import pickle
from time import sleep

from src.objects.downloader import VideoDownloader
from src.settings import Settings
from src.logger import inter_logger
from src.my_exceptions import AccessDeniedException, NoValidInterPublicException


class Interceptor:
    ANONYM_ID = '6287487'
    DATA = {
        'owner_id': None, 
        'fields': 'about,description,followers_count,is_closed,verified,screen_name,friend_status,is_subscribed,blacklisted,domain,sex,can_write_private_message,first_name_gen,last_name_gen,first_name_acc,is_nft_photo,admin_level,member_status,members_count,is_member,ban_info,can_message',
        'count': 10,
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
    
    PREF_FL = settings.PREFIX_FILE
    
    def __init__(self, inter_public: str):
        self.inter_public = inter_public
        self.inted_video = list()

        self.cycles = int()
        self.next_hash = str()
        self.ids = list()
            
    def intercept_video(self) -> str:
        self.refresh_creds()
        
        if not self.ids: self.ids = self.get_video_ids()
        
        for i in self.ids:
            inter_logger.debug(f'Видео которое будет загружено: {i}')
            
            try:
                self.ids.pop(self.ids.index(i))
                self.DOWNLOADER.download(public_id=self.inter_public, video_id=i)
            except KeyError:
                continue
    
            return f'{self.PREF_FL}{i}'
        
        return self.intercept_video()
         
    def get_video_ids(self) -> list:
        try:
            if self.next_hash:
                response = self.get_json(next_hash=self.next_hash)['response']
                
                try:
                    self.next_hash = response['next_from']
                except KeyError:
                    self.next_hash = str()
                    self.cycles += 1
            else:
                response = self.get_json()['response']
                self.next_hash = response['next_from']
                  
        except KeyError as ex:
            inter_logger.error(f'Перехват ошибки: {ex}')
            raise AccessDeniedException
        
        ids = list()
        
        for i in response['items']:
            ids.append(i['id'])
            
        return ids
    
    def get_json(self, next_hash: str = None) -> dict:
        self.DATA['owner_id'] = self.inter_public
        self.DATA['access_token'] = self.creds['access_token']
        
        if next_hash:
            self.DATA['start_from'] = next_hash
        
        response = requests.post(url=self.URL.format(anonym_id=self.ANONYM_ID), 
                                 headers=self.settings.HEADERS, data=self.DATA,
                                 cookies=self.jar)
        
        inter_logger.debug(f'Заголовки ответа: {response.headers}')
        inter_logger.debug(f'Тело ответа: {response.text[:1000]}')
        
        return response.json()
    
    def refresh_creds(self):    
        path = f'{self.settings.CREDS_PATH}{self.settings.ANONYM_FILE_NAME}.pkl'
        with open(path, 'rb') as file:
            self.creds = pickle.load(file)
            
        self.jar = requests.cookies.RequestsCookieJar()
        [self.jar.set(x['name'], x['value']) for x in self.creds['cookie']]