import logging

from settings import *


logger = logging.getLogger('server')


class Port:
    def __set__(self, instance, value):
        if not 1023 < value < 65536:
            message = f'Wrong port number {value}. Correct value for a port number is in range from 1024 to 65535.' \
                f'Will be used a default port number {DEFAULT_PORT}.'
            logger.critical(message)
            print(message)
            value = DEFAULT_PORT
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        # owner - <class '__main__.Server'>
        # name - port
        self.name = name

