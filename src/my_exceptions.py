class QueueLenException(Exception):
    
    def __str__(self):
        return 'Не приемлемая длинна видео очереди для данного действия.'

class AccessDeniedException(Exception):
    def __init__(self, public_id: str = None):
        self.public_id = public_id
    
    def __str__(self):
        return 'Не возможно загрузить видео, анонимный токен просрочен.'

class OverOneStartedException(Exception):
    
    def __str__(self):
        return 'Попытка запуска больше одного отложенного видео в паблике.'

class PublicsLenException(Exception):
    
    def __str__(self):
        return 'Достигнуто максимальное количество пабликов.'

class NoValidIdException(Exception):
    
    def __str__(self):
        return 'Айди уже присутствует в словаре.'

class NoFoundVideoException(Exception):
    def __init__(self, public_id: str = None):
        self.public_id = public_id
    
    def __str__(self):
        return 'Указаное видео не было найдено.'

class NoValidOwnPublicException(Exception):
    def __init__(self, public_id: str = None):
        self.public_id = public_id
    
    def __str__(self):
        return 'Указаный личный паблик не был валиден.'

class NoValidVideoPathException(Exception):
    def __init__(self, public_id: str = None):
        self.public_id = public_id
    
    def __str__(self):
        return 'Введенные данные для пути к видео не верны.'

class NoValidInterPublicException(Exception):
    def __init__(self, public_id: str = None):
        self.public_id = public_id
    
    def __str__(self):
        return 'Указанный паблик для отслеживания не был валиден.'

class NoValidDataException(Exception):
    
    def __str__(self):
        return 'Введенные данные не валидны.'
