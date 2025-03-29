from asyncio import create_task
import pickle

import src.my_exceptions as my_exceptions
from src.objects.public import Public
from src.settings import Settings


class Collector:
    settings = Settings()
    STATE_PATH = f'{settings.STATES_PATH}{settings.PUBLICS_STATE_NAME}.pkl'
    
    def __init__(self, max_publics: int):
        self.publics = dict()
        self.max_publics = max_publics
    
    def add_public(self, public: Public, id: str):
        if self.max_publics != len(self.publics):
            if id in self.publics: raise my_exceptions.NoValidIdException
            self.publics[id] = public
        else:
            raise my_exceptions.PublicsLenException
    
    def stop_publics(self):
        for public in self.publics.values():
            public.stop = True
            
    def delete_public(self, id: str) -> Public:
        return self.publics.pop(id)
    
    def get_public(self, id: str) -> Public:
        return self.publics[id]
    
    async def start_publics(self):
        for public in self.publics.values():
            try:
                create_task(public.start())
            except my_exceptions.OverOneStartedException:
                continue
    
    def save_state(self):
        with open(self.STATE_PATH, 'wb') as file:
            pickle.dump(self.publics, file=file)
    
    def load_state(self):
        with open(self.STATE_PATH, 'rb') as file:
            self.publics = pickle.load(file=file)
        
        for public in self.publics.values():
            public.started = False
            public.stop = False
            public.video_queue.started_time = None
            public.video_queue.run = True