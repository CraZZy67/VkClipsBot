from datetime import datetime, timedelta

from src.bot.global_classes import collector


def create_str_public_list():
    string = 'ID | PUBLIC ID | STATUS | TIME LEFT (h:m:s)\n\n'
    sep = '———————————————'
    
    for k, v in collector.publics.items():
        if v.stop:
            status = 'stoping'
        elif v.started:
            status = 'started'
        else:
            status = 'stoped'
            string += f'{k} - {v.public_id} {sep} {status}\n\n'
            continue
        
        target_time = v.video_queue.started_time + timedelta(minutes=int(v.video_queue.interval))
        time_left = str(target_time - datetime.now())
        time_left = time_left[:time_left.find('.')]
            
        string += f'{k} - {v.public_id} {sep} {status} {time_left}\n\n'
        
    return string
        