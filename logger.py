import logging


class Logger:
    def __init__(self):
        logging.basicConfig(filename='log.log', level=logging.DEBUG)




logging.basicConfig(filename='example.log',level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')