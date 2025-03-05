from loguru import logger
from typing import Dict
import os

class LogHandler:
    loggers_data: Dict = {}

    @classmethod
    def register(
            self,
            log_folder: str = None,
            logger_name:str = None,
            rotation: str = "200MB",
            retention: str = "7days"
        ):
        # print("Start register")
        assert logger_name is not None, "You must specify logger_name!"
        assert logger_name not in self.loggers_data.keys(), f"Logger name {logger_name} already existed"
        assert os.path.exists(log_folder), f"Log folder {log_folder} does not exist"
        log_path = os.path.join(log_folder, f"{logger_name}.txt")
        # print("Register processing 1")

        logger.add(log_path,
                   filter=lambda record: record["extra"]["logger_name"] == logger_name,
                   enqueue=False,
                   rotation=rotation,
                   retention=retention)
        # print("Register processing 2")
        
        self.loggers_data[logger_name] = {
            "logger": logger.bind(logger_name=logger_name),
            "log_folder": log_folder,
            "rotation": rotation,
            "retention": retention
        }
        # print("Register log success")

    
    @classmethod
    def get_logger(
            self,
            logger_name: str,
        ) -> logger:
        assert logger_name in self.loggers_data.keys(), f"Logger name {logger_name} does not existed"
        return self.loggers_data[logger_name]["logger"]

def setup_logger(
        log_folder: str = "app/logs/logs_data",
        logger_name: str = "general"
    ):
    if not os.path.exists("app/logs/logs_data"):
        os.makedirs("app/logs/logs_data")
    LogHandler.register(log_folder=log_folder, logger_name=logger_name)

if __name__=="__main__":
    # log_handler = LogHandler()
    LogHandler().register("test", "./logs_data")
    test_logger = LogHandler.get_logger("test")
    test_logger.error("Test")
