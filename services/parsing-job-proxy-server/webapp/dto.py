from typing import List, Optional

from pydantic import BaseModel
from pydantic import Field


class JobCreationRequest(BaseModel):
    job_name: str = Field(description="생성할 job name", examples=["sample-job1"])

    image: str = Field(description="생성할 docker image", examples=["busybox:1.28"])

    args: Optional[List[str]] = Field(default=None,
                                      description="docker container에 passing할 arguments 정보",
                                      examples=[["/bin/sh", "-c", "date; echo Hello from the kubernetes cluster"]])

    configmap_names: Optional[List[str]] = Field(default=None,
                                                 description="docker container에 적용할 환경변수(configmap) 목록들",
                                                 examples=[["storage-config", "spawner-config"]])


class OkResponse(BaseModel):
    ok: bool


class ExistResponse(BaseModel):
    exist: bool
