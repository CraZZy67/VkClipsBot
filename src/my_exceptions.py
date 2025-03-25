class QueueLenException(Exception):
    
    def __str__(self):
        return 'Не приемлемая длинна видео очереди для данного действия.'

class AccessDeniedException(Exception):
    
    def __str__(self):
        return 'Не возможно загрузить видео, анонимный токен просрочен.'

class OverOneStartedException(Exception):
    
    def __str__(self):
        return 'Попытка запуска больше одного отложенного видео в паблике.'

class PublicsLenException(Exception):
    
    def __str__(self):
        return 'Достигнуто максимальное количество пабликов.'

class NoValidId(Exception):
    
    def __str__(self):
        return 'Айди уже присутствует в словаре.'