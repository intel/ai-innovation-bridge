import os
import sys

from loguru import logger
from logging import StreamHandler, FileHandler

class Logger:
    _instance = None
    
    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = logger
            cls._instance.add(StreamHandler(sys.stdout), format="{time} {level} {message}", level="INFO")
            if not os.path.exists("logs"):
                os.makedirs("logs")
            cls._instance.add(FileHandler("logs/app.log"), format="{time} {level} {message}", level="DEBUG")
        return cls._instance

log = Logger.instance()

if __name__ == "__main__":
    log.info("Hello, World!")
    log.debug("Hello, World!")