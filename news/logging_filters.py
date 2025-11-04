import logging

class LevelFilter(logging.Filter):
    def __init__(self, name='', max_level=logging.CRITICAL):
        super().__init__(name)
        self.max_level = max_level

    def filter(self, record):
        return record.levelno <= self.max_level