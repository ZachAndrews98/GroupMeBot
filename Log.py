# Created by Zachary Andrews
# Github: ZachAndrews98

import logging
import logging.handlers

LOG_FILENAME = './logs/log.out'
ERROR_FILENAME = './logs/error.out'
MAX_BYTES = 50000*10^8
# creates general log
logger = logging.getLogger('General')
logger.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=MAX_BYTES, backupCount=5)
logger.addHandler(handler)
# creates error log
error_logger = logging.getLogger('Error')
error_logger.setLevel(logging.ERROR)
error_handler = logging.handlers.RotatingFileHandler(ERROR_FILENAME, maxBytes=MAX_BYTES, backupCount=5)
error_logger.addHandler(error_handler)

def log_info(info):
    info = info.replace('\n', ' ')
    logger.info(' INFO- '+info)

def log_debug(debug):
    debug = debug.replace('\n', ' ')
    logger.debug('DEBUG- '+debug)

def log_error(Exception):
    logger.debug('DEBUG- ERROR OCCURRED, CHECK ERROR LOG')
    error_logger.error('\t\t\t\t\t\t\t\t==Error==',exc_info=True)
