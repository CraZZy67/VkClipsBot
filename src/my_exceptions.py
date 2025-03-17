class QueueLenException(Exception):
    
    def __str__(self):
        return 'Не возможно выгрузить следующие видео, очередь пуста.'