from enum import Enum


class ModelStatus(Enum):
    RUNNING = "running"
    FAIL = "failed"
    SUCCESS = "success"
