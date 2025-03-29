import logging
from logging import Logger

# ---------
handler = logging.FileHandler("logs.log", encoding="utf-8")
stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d) [%(filename)s]')

handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

def add_hadlers(logger: Logger):
    logger.addHandler(stream_handler)
    logger.addHandler(handler)
# ---------

# ---------
auth_logger = logging.getLogger('authorizer')
add_hadlers(logger=auth_logger)

inter_logger = logging.getLogger('interceptor')
add_hadlers(logger=inter_logger)

down_logger = logging.getLogger('download')
add_hadlers(logger=down_logger)

upload_logger = logging.getLogger('upload')
add_hadlers(logger=upload_logger)

bot_logger = logging.getLogger('bot')
add_hadlers(logger=bot_logger)

queue_logger = logging.getLogger('queue')
add_hadlers(logger=queue_logger)

pub_logger = logging.getLogger('ppub')
add_hadlers(logger=pub_logger)
# ---------

# ---------    
auth_logger.setLevel(logging.INFO)
inter_logger.setLevel(logging.INFO)
down_logger.setLevel(logging.INFO)
upload_logger.setLevel(logging.INFO)
bot_logger.setLevel(logging.INFO)
queue_logger.setLevel(logging.INFO)
pub_logger.setLevel(logging.INFO)
# ---------

# logging.disable()