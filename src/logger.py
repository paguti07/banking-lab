import logging
from dotenv import load_dotenv
import os

load_dotenv()

class Logger:
    __instance = None
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    LOG_FILE = os.getenv("LOG_FILE", "banking.log")

    def __new__(cls):
        if cls.__instance is None:           
            cls.__instance = super().__new__(cls)
            cls.__instance.__init_logger()
        return cls.__instance

    def __init_logger(self):
        self.__logger = logging.getLogger("banking-lab")
        self.__logger.setLevel(self.LOG_LEVEL)

        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        self.__logger.addHandler(handler)

        try:
            file_handler = logging.FileHandler(self.LOG_FILE, encoding="utf-8")
            file_handler.setLevel(self.LOG_LEVEL)
            file_handler.setFormatter(formatter)
            self.__logger.addHandler(file_handler)
        except OSError as e:
                print(f"Error setting up file handler: {e}")

    @property
    def get_logger(self):
        return self.__logger
