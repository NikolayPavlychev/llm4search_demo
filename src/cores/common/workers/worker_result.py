from dataclasses import dataclass
from enum import Enum


class WorkerMessageType(Enum):
    ALREADY_RUNNING = "already_running"
    STARTED = "started"


@dataclass
class WorkerResult:
    success: bool
    message_type: WorkerMessageType
    message: str
