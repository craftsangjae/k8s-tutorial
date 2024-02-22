from typing import List

from pydantic import BaseModel
from pydantic import Field


class JobCreationRequest(BaseModel):
    job_name: str = Field(description="생성할 job name", examples=["sample-job1"])

    image: str = Field(description="생성할 docker image", examples=["busybox:1.28"])

    command: List[str] = Field(default_factory=list,
                               description="docker container에 passing할 command 정보",
                               examples=[["/bin/sh", "-c", "date; echo Hello from the kubernetes cluster"]])


class OkResponse(BaseModel):
    ok: bool


class ExistResponse(BaseModel):
    exist: bool
