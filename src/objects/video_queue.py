from collections import deque
import asyncio
from datetime import datetime
import time

from src.objects.uploader import VideoUploader
from src.my_exceptions import QueueLenException
from src.settings import Settings
from src.objects.authorizer import UserAuthorizer
from src.logger import queue_logger
import src.my_exceptions as my_exception


class VideoQueue:
    UPLOADER = VideoUploader()
    settings = Settings()
    
    def __init__(self, interval: int):
        self.interval = interval
        
        self.queue = deque(maxlen=self.settings.MAX_LEN_QUEUE)
        self.run = True
        self.started_time = None
    
    def add_video(self, video_id: str):
        self.queue.appendleft(video_id)
    
    async def run_next_video(self, inter_public: str, own_public: str) -> str:
        if self.run: 
            if len(self.queue):
                self.started_time = datetime.now()
                
                queue_logger.info(f'Начало таймера. Задержка: {float(self.interval * 60)}')
                await asyncio.sleep(float(self.interval * 60))
                queue_logger.info('Конец таймера.')
            else:
                raise QueueLenException
            
            if self.run:
                if len(self.queue):
                    video_id = self.queue.pop()
                    for i in range(3):
                        try:
                            self.UPLOADER.upload(own_public, inter_public, 
                                                 video_id=video_id)
                        except Exception:
                            continue
                        
                        return video_id
                    else:
                        queue_logger.info('Три попытки для опубликования видео истекли.')
                        raise my_exception.NoValidDataException
                else:
                    raise QueueLenException
            else:
                self.run = True 
    
    def delete_video(self) -> str:
        if len(self.queue):
            return self.queue.pop()
        else:
            raise QueueLenException


class DebugVideoQueue(VideoQueue):
    def run_next_video(self, inter_public: str, own_public: str) -> str:
        if self.run: 
            if len(self.queue): 
                self.started_time = datetime.now()
                
                queue_logger.info(f'Начало таймера. Задержка: {float(self.interval * 60)}')
                time.sleep(float(self.interval * 60))
                queue_logger.info('Конец таймера.')
                
                UserAuthorizer().refresh_anonym_token()
            else:
                raise QueueLenException
            
            if self.run:
                if len(self.queue):
                    video_id = self.queue.pop()
                    
                    self.UPLOADER.upload(own_public, inter_public, 
                                        video_id=video_id)
                    return video_id
                else:
                    raise QueueLenException
            else:
                self.run = True