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
auth_logger = logging.getLogger('authorizers')
add_hadlers(logger=auth_logger)
# ---------

# ---------    
auth_logger.setLevel(logging.DEBUG)
# ---------
