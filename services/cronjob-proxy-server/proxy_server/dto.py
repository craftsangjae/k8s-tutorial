from dataclasses import dataclass
from datetime import datetime


@dataclass
class CronJobInfo:
    name: str
    namespace: str
    schedule: str  # The schedule in Cron format

    created_at: datetime  # CreationTimestamp is a timestamp representing the server time when this object was created
    last_scheduled_at: datetime  # Information when was the last time the job was successfully scheduled
    last_success_at: datetime  # Information when was the last time the job successfully completed


@dataclass
class CreateCronJobRequest:
    schedule: str
    name: str
    namespace: str = "default"


@dataclass
class DeleteJobRequest:
    name: str
    namespace: str = "default"


@dataclass
class JobStatusResponse:
    status: str
