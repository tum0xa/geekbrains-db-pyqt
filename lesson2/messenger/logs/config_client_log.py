import sys
import os
import logging

from settings import LOGGING_LEVEL


client_formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')


path = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(path, 'client.log')


steam = logging.StreamHandler(sys.stderr)
steam.setFormatter(client_formatter)
steam.setLevel(logging.ERROR)
log_file = logging.FileHandler(path, encoding='utf8')
log_file.setFormatter(client_formatter)


logger = logging.getLogger('client')
logger.addHandler(steam)
logger.addHandler(log_file)
logger.setLevel(LOGGING_LEVEL)


