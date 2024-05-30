from multiprocessing import Process
import psutil
import time
import uvicorn
from fastapi import FastAPI
from classy_fastapi import Routable

from src.cores.common.web.controllers.system_controller import SystemController


class WebApi:
    def __init__(self, host: str, port: int, config_file: str, log_format: str) -> None:
        self.__app = FastAPI()
        self.__host = host
        self.__port = port
        self.__log_format = log_format
        self.__config_file = config_file

    def add_controller(self, controller: Routable):
        self.__app.include_router(controller.router)

    # https://github.com/tiangolo/fastapi/issues/1508
    def run(self):
        self.__app.include_router(SystemController(config_file=self.__config_file).router)
        log_config = uvicorn.config.LOGGING_CONFIG
        log_config["formatters"]["access"]["fmt"] = self.__log_format
        log_config["formatters"]["default"]["fmt"] = self.__log_format
        uvicorn.run(self.__app, host=self.__host, port=self.__port, log_config=log_config)
        
    def shutdown_server(self, proc: Process):

        pid = proc.pid
        parent = psutil.Process(pid)
        for child in parent.children(recursive=True):
            child.kill()
        
        proc.terminate()
