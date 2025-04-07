from datetime import datetime, timedelta
from asyncio import sleep

from src.bot.global_classes import collector
from src.objects.public import Public
from src.objects.authorizer import UserAuthorizer


def create_str_public_list() -> str:
    string = 'ID | PUBLIC ID | STATUS | TIME LEFT (h:m:s)\n\n'
    sep = '—————————————'
    
    for k, v in collector.publics.items():
        if v.stop:
            status = 'stoping'
        elif v.started:
            status = 'started'
        else:
            status = 'stoped'
            string += f'{k} - {v.public_id} {sep} {status} N\\A\n\n'
            continue
        
        time_left = get_time_left(v.video_queue.started_time, v.video_queue.interval)
        status = status if time_left[0] != '-' else 'error'
        time_left = time_left if time_left[0] != '-' else 'N/A'
        
        string += f'{k} - {v.public_id} {sep} {status} {time_left}\n\n'
    return string

def get_time_left(started_time: datetime, interval: str) -> str:
    target_time = started_time + timedelta(minutes=int(interval))
    time_left = str(target_time - datetime.now())
    
    return time_left[:time_left.find('.')]

def create_public_info(public: Public) -> str:
    sep = '—————————————'
    string = 'ИНФОРМАЦИЯ О ПАБЛИКЕ\n\n'
    
    if public.stop:
        status = 'stoping'
    elif public.started:
        status = 'started'
    else:
        status = 'stoped'
    
    string += f'Паблик id: {public.public_id}\n'
    string += sep + '\n'
    string += f'Отслеживаемый паблик: {public.inter_public}\n'
    string += sep + '\n'
    
    if status == 'stoped':
        string += 'Оствашееся время: N\\A\n'
    else:
        time_left = get_time_left(public.video_queue.started_time,
                              public.video_queue.interval)
        string += f'Оствашееся время: {time_left}\n'
    
    string += sep + '\n'
    string += f'Статус: {status}'
    
    return string

def create_queue_info(public: Public) -> str:
    sep = '—————————————'
    string = 'ИНФОРМАЦИЯ О ВИДЕО ОЧЕРЕДИ\n\n'
    
    string += f'Интервал: {public.video_queue.interval} мин\n'
    string += sep + '\n'
    string += 'Очередь: '
    
    if len(public.video_queue.queue):
        for i, v in enumerate(public.video_queue.queue):
            string += f'{i} - {str(v)[-3:]}; '
        string += '\n'
    else:
        string += 'empty\n'
            
    string += sep + '\n'
    status = 'Will be started' if public.video_queue.run else 'Will be stoped'
    string += f'Cтатус: {status}'
    return string

async def intercept_expiry(interval: float):
    UserAuthorizer().refresh_anonym_token()
     
    while True:
        await sleep(interval)
        UserAuthorizer().refresh_anonym_token()
        