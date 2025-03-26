from datetime import datetime, timedelta

from src.bot.global_classes import collector


def create_str_public_list():
    string = 'ID | PUBLIC ID | STATUS | TIME LEFT\n\n'
    sep = '———————————————'
    
    for k, v in collector.publics.items():
        if v.stop:
            status = 'stoping'
            
            target_time = v.video_queue.started_time + timedelta(minutes=v.video_queue.interval)
            time_left = target_time - datetime.now().strftime('%d.%m.%Y %H:%M:%S')
            
            string += f'{k} - {v.public_id} {sep} {status} {time_left}\n\n'
        elif v.started:
            status = 'started'

            target_time = v.video_queue.started_time + timedelta(minutes=v.video_queue.interval)
            time_left = target_time - datetime.now().strftime('%d.%m.%Y %H:%M:%S')    
            
            string += f'{k} - {v.public_id} {sep} {status} {time_left}\n\n'
        else:
            status = 'stoped'
            string += f'{k} - {v.public_id} {sep} {status}\n\n'
        
    return string
        