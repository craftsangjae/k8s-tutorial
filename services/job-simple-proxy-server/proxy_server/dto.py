from dataclasses import dataclass
from typing import Dict


@dataclass
class JobInfo:
    name: str
    namespace: str

    active: int  # The number of pending and running pods.
    failed: int  # The number of pods which reached phase Failed.
    ready: int  # The number of pods which have a Ready condition.
    succeeded: int  # The number of pods which reached phase Succeeded.


@dataclass
class CreateJobRequest:
    name: str
    namespace: str = "default"
    value: int = 10


@dataclass
class DeleteJobRequest:
    name: str
    namespace: str = "default"


@dataclass
class JobStatusResponse:
    status: str
