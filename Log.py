# Created by Zachary Andrews
# Github: ZachAndrews98

import glob
import logging
import logging.handlers

LOG_FILENAME = './logs/log.out'
MAX_BYTES = 50000*10^8

logger = logging.getLogger('MyLogger')
logger.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes= MAX_BYTES, backupCount=5)
logger.addHandler(handler)

def log_info(info):
    info = info.replace('\n', ' ')
    logger.info(' INFO- '+info)

def log_debug(debug):
    debug = debug.replace('\n', ' ')
    logger.debug('DEBUG- '+debug)
