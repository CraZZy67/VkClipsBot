from collections import deque
from asyncio import sleep
import time


from src.objects.uploader import Uploader
from src.my_exceptions import QueueLenException


class DebugVideoQueue:
    UPLOADER = Uploader()
    
    def __init__(self, inter_public: str, own_public: str, interval: int):
        self.inter_public = inter_public
        self.own_public = own_public
        self.interval = interval
        
        self.queue = deque(maxlen=5)
        self.run = True
    
    def add_video(self, video_id: str):
        self.queue.appendleft(video_id)
    
    async def run_next_video(self):
        if self.run: 
            if len(self.queue): 
                await sleep(float(self.interval * 60))
            else:
                raise QueueLenException
            
        if self.run:
            if len(self.queue):
                video_id = self.queue.pop()
                
                self.UPLOADER.upload(self.own_public, 
                                    self.inter_public, video_id=video_id)
            else:
                raise QueueLenException
        else:
            self.run = True 
    
    def delete_video(self):
        if len(self.queue):
            self.queue.pop()
        else:
            raise QueueLenException


class DebugVideoQueue(DebugVideoQueue):
    def run_next_video(self):
        if self.run: 
            if len(self.queue): 
                time.sleep(float(self.interval * 60))
            else:
                raise QueueLenException
            
        if self.run:
            if len(self.queue):
                video_id = self.queue.pop()
                
                self.UPLOADER.upload(self.own_public, 
                                    self.inter_public, video_id=video_id)
            else:
                raise QueueLenException
        else:
            self.run = True