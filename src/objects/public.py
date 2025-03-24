from selenium.webdriver import Chrome
import dotenv

import os

from src.objects.interceptor import Interceptor
from src.objects.video_queue import VideoQueue, DebugVideoQueue
from src.objects.authorizer import UserAuthorizer
from src.settings import Settings
from src.logger import public_logger
from src.my_exceptions import (NotFoundVideoException, OverOneStartedException,
                               QueueLenException, AccessDeniedException)


class Public:
    settings = Settings()
    
    ANONYM_LINK = 'https://vk.com/icollbelgu'
    LOCAL_STORAGE_KEY = '6287487:get_anonym_token:login:auth'
    
    def __init__(self, public_id: str, interceptor: Interceptor, video_queue: VideoQueue):
        self.interceptor = interceptor
        self.video_queue = video_queue
        self.inter_public = interceptor.inter_public
        self.public_id = public_id
        
        self.started = False
        self.stop = False
    
    def synchronize(self):
        list_dir = os.listdir('./media')
        
        if not self.inter_public in list_dir:
            self.interceptor.intercept_video()
        
        list_media = os.listdir(f'./media/{self.inter_public}/')
        diff = self.settings.MAX_LEN_QUEUE - len(list_media)
        
        for i in range(diff):
            try:
                self.interceptor.intercept_video()
            except AccessDeniedException:
                self.refresh_anonym_token()
                self.interceptor.intercept_video()
                
        for i in os.listdir(f'./media/{self.inter_public}/'):       
            self.video_queue.add_video(i.replace('.mp4', ''))         
                        
    async def start(self):
        if not self.started:
            self.started = True
            self.synchronize()
            
            video = await self.video_queue.run_next_video(self.inter_public, 
                                                          self.public_id)
            os.remove(f'./media/{self.inter_public}/{video}.mp4')
            
            while True:
                if not self.stop:
                    
                    try:
                        self.video_queue.add_video(str(self.interceptor.intercept_video()))
                    except AccessDeniedException:
                        self.refresh_anonym_token()
                        self.video_queue.add_video(str(self.interceptor.intercept_video()))
                    
                    video = await self.video_queue.run_next_video(self.inter_public, 
                                                                  self.public_id)
                    
                    os.remove(f'./media/{self.inter_public}/{video}.mp4')
                else:
                    self.started = False
                    break
        else:
            raise OverOneStartedException
    
    def add_video(self, video_id: str):
        if len(self.video_queue.queue) < self.settings.MAX_LEN_QUEUE:
            try:
                self.interceptor.DOWNLOADER.download(public_id=self.inter_public,
                                            video_id=video_id)
            except AccessDeniedException:
                self.refresh_anonym_token()
                self.interceptor.DOWNLOADER.download(public_id=self.inter_public,
                                            video_id=video_id)
            except Exception:
                raise NotFoundVideoException
            
            self.video_queue.add_video(video_id=video_id)
        else:
            raise QueueLenException
        
    def refresh_anonym_token(self):
        dotenv.load_dotenv()
        
        driver = Chrome()
        driver.get(self.ANONYM_LINK)
        
        authorizer = UserAuthorizer()
        
        authorizer.driver = driver
        authorizer.LOCAL_STORAGE_KEY = self.LOCAL_STORAGE_KEY
        
        authorizer.save_session_creds(file_name=os.getenv('ANONYM_FILE_NAME'), 
                                      out_session=True)
    
    def delete_video(self):
        if len(self.video_queue.queue) > 2:
            video = self.video_queue.delete_video()
            os.remove(f'./media/{self.inter_public}/{video}.mp4')
        else:
            raise QueueLenException
        

class DebugPublic(Public):
    
        def __init__(self, public_id: str, interceptor: Interceptor, video_queue: DebugVideoQueue):
            self.interceptor = interceptor
            self.video_queue = video_queue
            self.inter_public = interceptor.inter_public
            self.public_id = public_id
            
            self.started = False
            self.stop = False
        
        def start(self):
            if not self.started:
                self.started = True
                self.synchronize()
            
                video = self.video_queue.run_next_video(self.inter_public, 
                                                        self.public_id)
                os.remove(f'./media/{self.inter_public}/{video}.mp4')
                
                while True:
                    if not self.stop:
                        
                        try:
                            self.video_queue.add_video(str(self.interceptor.intercept_video()))
                        except AccessDeniedException:
                            self.refresh_anonym_token()
                            self.video_queue.add_video(str(self.interceptor.intercept_video()))
                        
                        video = self.video_queue.run_next_video(self.inter_public, 
                                                                self.public_id)
                        
                        os.remove(f'./media/{self.inter_public}/{video}.mp4')
                    else:
                        self.started = False
                        break
            else:
                raise OverOneStartedException