import sys
import logs.config_server_log
import logs.config_client_log
import logging

if sys.argv[0].find('server') != -1:
    logger = logging.getLogger('server')
else:
    logger = logging.getLogger('client')


def log(function):
    def log_saver(*args, **kwargs):
        logger.debug(
            f'The function {function.__name__} has been called with arguments {args} , {kwargs}. Call was executed from  {function.__module__}')
        ret = function(*args, **kwargs)
        return ret

    return log_saver
