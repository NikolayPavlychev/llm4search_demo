import os
import psutil
from typing import List

from classy_fastapi import Routable, post

from fastapi import BackgroundTasks, HTTPException

from src.cores.common.web.api_paths import API_PATH
from src.cores.common.workers.singleton_worker import SingletonWorker
from src.cores.common.workers.worker_result import WorkerMessageType
from src.service_modules.igla_pipeline_service.services.igla_processor import IglaProcessor

class IglaPipelineController(Routable):

    def __init__(self, processor: IglaProcessor, singleton_worker: SingletonWorker) -> None:
        super().__init__()
        self.__processor = processor
        self.__singleton_worker = singleton_worker

    PIPELINE_API_PATH = f"{API_PATH}/igla-pipeline"

    @post(f"{PIPELINE_API_PATH}/crawl", description="run igla pipeline",
          summary="Crawl igla docs and vectorize to a elasticsearch",
          status_code=202)
    async def crawl(self, source_codes: List[str], tasks: BackgroundTasks):
        res = await self.__singleton_worker.start("igla_pipeline", tasks, self.__processor.process, source_codes)
        if (res.message_type == WorkerMessageType.STARTED):
            return res.message
        elif (res.message_type == WorkerMessageType.ALREADY_RUNNING):
            raise HTTPException(status_code=406, detail=res.message)
        else:
            raise HTTPException(status_code=500, detail=res.message)
        
    @post(f"{PIPELINE_API_PATH}/quit", description="shutdown app")
    def iquit(self):
        parent_pid = os.getpid()
        parent = psutil.Process(parent_pid)
        for child in parent.children(recursive=True):
            child.kill()
        parent.kill()
