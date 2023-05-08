import logging
from kink import di
from syslog import LOG_DAEMON
import logging.handlers
from logging.handlers import SysLogHandler


def get_logger(source:str):
	logger = logging.getLogger(source)
	logger.setLevel(logging.DEBUG)
	handler = logging.handlers.SysLogHandler(facility=SysLogHandler.LOG_DAEMON, address = di['LOGGING_ADRESS'])
	handler.setFormatter(di['LOGGING_FORMAT'])
	logger.addHandler(handler)
	return logger

