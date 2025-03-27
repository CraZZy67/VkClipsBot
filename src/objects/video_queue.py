from collections import deque
import asyncio
from datetime import datetime
import time

from src.objects.uploader import VideoUploader
from src.my_exceptions import QueueLenException
from src.settings import Settings
from src.objects.authorizer import UserAuthorizer


class VideoQueue:
    UPLOADER = VideoUploader()
    settings = Settings()
    
    def __init__(self, interval: int):
        self.interval = interval
        
        self.queue = deque(maxlen=self.settings.MAX_LEN_QUEUE)
        self.run = True
    
    def add_video(self, video_id: str):
        self.queue.appendleft(video_id)
    
    async def run_next_video(self, inter_public: str, own_public: str) -> str:
        if self.run: 
            if len(self.queue):
                self.started_time = datetime.now()
                
                print('B')
                await asyncio.sleep(float(self.interval * 60))
                print('A')
                
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
                
                time.sleep(float(self.interval * 60))
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