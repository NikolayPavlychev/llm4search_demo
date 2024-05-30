from asyncio import Semaphore
from typing import Any
from fastapi import BackgroundTasks
import logging

from src.cores.common.workers.worker_result import WorkerResult, WorkerMessageType


class SingletonWorker:
    def __init__(self):
        self.__sem = Semaphore(1)

    async def start(self, name: str, tasks: BackgroundTasks, worker_func: Any, *args) -> WorkerResult:
        async def start_with_lock(*args):
            await self.__sem.acquire()
            try:
                logging.info(f"starting worker {name}")
                await worker_func(*args)
                logging.info(f"finished worker {name}")
            except Exception as e:
                logging.error(e, exc_info=True)
            finally:
                self.__sem.release()

        if (self.__sem.locked() == False):
            tasks.add_task(start_with_lock, *args)
            logging.info(f"started task {len(tasks.tasks)}")
            return WorkerResult(True, WorkerMessageType.STARTED, f"started")
        else:
            logging.info(f"already running task {len(tasks.tasks)}")
            return WorkerResult(False, WorkerMessageType.ALREADY_RUNNING, f"already running")
