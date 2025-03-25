import pickle

from src.objects.public import Public
from src.my_exceptions import PublicsLenException, NoValidId

class Collector:
    
    def __init__(self, max_publics: int):
        self.publics = dict()
        self.max_publics = max_publics
    
    def add_public(self, public: Public, id: str):
        if self.max_publics != len(self.publics):
            if id in self.publics: raise NoValidId
            
            self.publics[id] = public
        else:
            raise PublicsLenException
    
    def stop_publics(self):
        for public in self.publics.values():
            public.stop = False
            
    def delete_public(self, id: str) -> Public:
        return self.publics.pop(id)
    
    def get_public(self, id: str) -> Public:
        return self.publics[id]
    
    async def start_publics(self):
        for public in self.publics.values():
            await public.start()
    
    def save_state(self):
        with open(f'states/publics.pkl', 'wb') as file:
            pickle.dump(self.publics, file=file)
    
    def load_state(self):
        with open(f'states/publics.pkl', 'rb') as file:
            self.publics = pickle.load(file=file)
        
        for public in self.publics.values():
            public.started = False
            public.stop = False
            public.video_queue.run = True