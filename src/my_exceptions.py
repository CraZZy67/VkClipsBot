class QueueLenException(Exception):
    
    def __str__(self):
        return 'Не приемлемая длинна видео очереди для данного действия.'

class NotFoundVideoException(Exception):
    
    def __str__(self):
        return 'Не возможно найти видео запрошенное пользователем.'

class AccessDeniedException(Exception):
    
    def __str__(self):
        return 'Не возможно загрузить видео, анонимный токен просрочен.'

class OverOneStartedException(Exception):
    
    def __str__(self):
        return 'Попытка запуска больше одного отложенного видео в паблике.'