import dotenv

import os

from src.objects.interceptor import Interceptor
from src.objects.video_queue import VideoQueue, DebugVideoQueue
from src.settings import Settings
from src.my_exceptions import (OverOneStartedException, QueueLenException,
                               AccessDeniedException, NoFoundVideoException,
                               NoValidInterPublicException, NoValidVideoPathException,
                               NoValidOwnPublicException)


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
        dotenv.load_dotenv()

        sl = os.getenv('SLESH')
        
        list_dir = os.listdir(f'.{sl}{self.settings.VIDEO_PATH[0:-1]}')
        
        if not self.inter_public in list_dir:
            try:
                self.interceptor.intercept_video()
            except AccessDeniedException:
                raise AccessDeniedException(public_id=self.public_id)
            
            except NoValidInterPublicException:
                raise NoValidInterPublicException(public_id=self.public_id)
            
        list_media = os.listdir(f'.{sl}{self.settings.VIDEO_PATH}{self.inter_public}/')
        diff = self.settings.MAX_LEN_QUEUE - len(list_media)
        
        for i in range(diff):
            try:
                self.interceptor.intercept_video()
            except AccessDeniedException:
                raise AccessDeniedException(public_id=self.public_id)
            
            except NoValidInterPublicException:
                raise NoValidInterPublicException(public_id=self.public_id)
                 
        for i in os.listdir(f'.{sl}{self.settings.VIDEO_PATH}{self.inter_public}/'):
            i = i.replace('.mp4', '')
            
            if not i in self.video_queue.queue:       
                self.video_queue.add_video(i)         
                        
    async def start(self):
        dotenv.load_dotenv()

        sl = os.getenv('SLESH')
        
        if not self.started:
            self.synchronize()
            self.started = True
            try:
                video = await self.video_queue.run_next_video(self.inter_public, 
                                                          self.public_id)
            except NoValidOwnPublicException:
                self.started = False
                raise NoValidOwnPublicException(public_id=self.public_id)
            except NoValidVideoPathException:
                self.started = False
                raise NoValidVideoPathException(public_id=self.public_id)
            if video:
                os.remove(f'.{sl}{self.settings.VIDEO_PATH}{self.inter_public}{sl}{video}.mp4')
            
            while True:
                if not self.stop:
                    try:
                        self.video_queue.add_video(str(self.interceptor.intercept_video()))
                        
                    except NoValidInterPublicException:
                        self.started = False
                        raise NoValidInterPublicException(public_id=self.public_id)
                    except AccessDeniedException:
                        self.started = False
                        raise AccessDeniedException(public_id=self.public_id)
                    
                    try:
                        video = await self.video_queue.run_next_video(self.inter_public, 
                                                                      self.public_id)
                    except NoValidOwnPublicException:
                        self.started = False
                        raise NoValidOwnPublicException(public_id=self.public_id) 
                    except NoValidVideoPathException:
                        self.started = False
                        raise NoValidVideoPathException(public_id=self.public_id)
                    
                    if video:
                        os.remove(f'.{sl}{self.settings.VIDEO_PATH}{self.inter_public}{sl}{video}.mp4')
                else:
                    self.started = False
                    self.stop = False
                    break
        else:
            raise OverOneStartedException
    
    def add_video(self, video_id: str):
        if len(self.video_queue.queue) < self.settings.MAX_LEN_QUEUE:
            
            try:
                self.interceptor.DOWNLOADER.download(public_id=self.inter_public,
                                                     video_id=video_id)
            except AccessDeniedException:
                raise AccessDeniedException(public_id=self.public_id)
            except NoFoundVideoException:
                raise NoFoundVideoException(public_id=self.public_id)
            
            self.video_queue.add_video(video_id=video_id)
        else:
            raise QueueLenException
    
    def delete_video(self):
        dotenv.load_dotenv()

        sl = os.getenv('SLESH')
        
        if len(self.video_queue.queue) > 2:
            video = self.video_queue.delete_video()
            os.remove(f'.{sl}{self.settings.VIDEO_PATH}{self.inter_public}{sl}{video}.mp4')
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
            dotenv.load_dotenv()

            sl = os.getenv('SLESH')
        
            if not self.started:
                self.synchronize()
                
                self.started = True
                try:
                    video = self.video_queue.run_next_video(self.inter_public, 
                                                            self.public_id)
                except NoValidOwnPublicException:
                    self.started = False
                    raise NoValidOwnPublicException(public_id=self.public_id)
                except NoValidVideoPathException:
                    self.started = False
                    raise NoValidVideoPathException(public_id=self.public_id)
                
                os.remove(f'.{sl}{self.settings.VIDEO_PATH}{self.inter_public}{sl}{video}.mp4')
                
                while True:
                    if not self.stop:
                        try:
                            self.video_queue.add_video(str(self.interceptor.intercept_video()))
                            
                        except NoValidInterPublicException:
                            self.started = False
                            raise NoValidInterPublicException(public_id=self.public_id)
                        except AccessDeniedException:
                            self.started = False
                            raise AccessDeniedException(public_id=self.public_id)
                        
                        try:
                            video = self.video_queue.run_next_video(self.inter_public, 
                                                                    self.public_id)
                        except NoValidOwnPublicException:
                            self.started = False
                            raise NoValidOwnPublicException(public_id=self.public_id) 
                        except NoValidVideoPathException:
                            self.started = False
                            raise NoValidVideoPathException(public_id=self.public_id)
                        
                        os.remove(f'.{sl}{self.settings.VIDEO_PATH}{self.inter_public}{sl}{video}.mp4')
                    else:
                        self.started = False
                        break
            else:
                raise OverOneStartedException