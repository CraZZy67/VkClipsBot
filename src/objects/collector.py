import pickle

from src.objects.public import Public


class Collector:
    
    def __init__(self):
        self.publics = dict()
    
    def add_public(self, public: Public, id: str):
        self.publics[id] = public
    
    def delete_public(self, id: str):
        return self.publics.pop(id)
    
    def get_public(self, id: str):
        return self.publics[id]
    
    def save_state(self):
        with open(f'states/publics.pkl', 'wb') as file:
            pickle.dump(self.publics, file=file)
    
    def load_state(self):
        with open(f'states/publics.pkl', 'rb') as file:
            self.publics = pickle.load(file=file)
            