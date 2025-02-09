import logging
import os
from logging.handlers import RotatingFileHandler

class Logger:
    def __init__(self, logger_name='game_scraper_logger', log_file='scraper.log', log_level=logging.INFO):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(log_level)

        # Create a rotating file handler
        handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=5)
        handler.setLevel(log_level)

        # Create a logging format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # Add the handlers to the logger
        self.logger.addHandler(handler)

    def get_logger(self):
        return self.logger