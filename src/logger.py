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
# ---------

# ---------    
auth_logger.setLevel(logging.DEBUG)
inter_logger.setLevel(logging.DEBUG)
down_logger.setLevel(logging.DEBUG)
upload_logger.setLevel(logging.DEBUG)
# ---------

# logging.disable()