from __future__ import print_function
import sys
from logging import StreamHandler, getLogger
import coloredlogs


def get_module_logger(module):
    logger = getLogger(module)
    logger.addHandler(StreamHandler(sys.stderr))
    logger.propagate = False
    coloredlogs.DEFAULT_LOG_FORMAT = '[%(asctime)s %(levelname)s] %(message)s'
    coloredlogs.install(level='INFO', logger=logger)
    return logger
