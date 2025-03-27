from asyncio import create_task
import pickle

from src.objects.public import Public
from src.my_exceptions import PublicsLenException, NoValidIdException, OverOneStartedException
from src.settings import Settings


class Collector:
    settings = Settings()
    STATE_PATH = f'{settings.STATES_PATH}{settings.PUBLICS_STATE_NAME}.pkl'
    
    def __init__(self, max_publics: int):
        self.publics = dict()
        self.max_publics = max_publics
    
    def add_public(self, public: Public, id: str):
        if self.max_publics != len(self.publics):
            if id in self.publics: raise NoValidIdException
            
            self.publics[id] = public
        else:
            raise PublicsLenException
    
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
            except OverOneStartedException:
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
            public.video_queue.run = True