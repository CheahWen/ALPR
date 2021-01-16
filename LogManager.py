import logging
from datetime import datetime

"""
    log type:
        0: info
        1: error

"""

class LogManager:
    @staticmethod
    def makeConfig():
        logging.basicConfig(filename=f"LogFiles/Log.{datetime.today().strftime('%Y-%m-%d')}.log",
                            filemode='a',
                            format='%(asctime)s %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)


    @staticmethod
    def makeLog(message, type=0):
        # ignore other type to info
        if type == 1:
            logging.error(message)
        else:
            logging.info(message)


