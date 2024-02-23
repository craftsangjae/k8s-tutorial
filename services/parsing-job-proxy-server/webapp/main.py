from typing import Annotated

from fastapi import FastAPI, Depends, Request
from starlette.responses import JSONResponse

from proxy_manager.exceptions import ProxyManagerException
from proxy_manager.spawner.spawner import K8SJobSpawner
from webapp.dependency import job_spawner_dependency
from webapp.dto import ExistResponse, OkResponse, JobCreationRequest

app = FastAPI(title="proxy-manager-API")


@app.get("/health")
async def read_health():
    """ health check API
    """
    return OkResponse(ok=True)


@app.get('/jobs/{job_name}')
async def read_job(
        job_name: str,
        spawner: Annotated[K8SJobSpawner, Depends(job_spawner_dependency)]
):
    """ Job에 대한 정보 조회
    """
    job = spawner.read(job_name)
    return job


@app.post('/jobs')
async def create_job(
        req: JobCreationRequest,
        spawner: Annotated[K8SJobSpawner, Depends(job_spawner_dependency)]
):
    """ Job 생성 요청
    :return:
    """
    spawner.create(req.job_name, req.image, req.args, req.configmap_names)
    return OkResponse(ok=True)


@app.delete('/jobs/{job_name}')
async def delete_job(
        job_name: str,
        spawner: Annotated[K8SJobSpawner, Depends(job_spawner_dependency)]
):
    """ Job 삭제 요청
    :return:
    """
    spawner.delete(job_name)
    return OkResponse(ok=True)


@app.get('/jobs/{job_name}/exists')
async def exist_job(
        job_name: str,
        spawner: Annotated[K8SJobSpawner, Depends(job_spawner_dependency)]
) -> ExistResponse:
    """ Job 존재여부 응답 받기
    :return:
    """
    exist = spawner.exist(job_name)
    return ExistResponse(exist=exist)


@app.exception_handler(ProxyManagerException)
async def proxy_manager_handler(request: Request, exc: ProxyManagerException):
    """ ProxyManagerException 핸들링 로직
    :param request:
    :param exc:
    :return:
    """

    return JSONResponse(
        status_code=403,
        content={
            "message": exc.message
        }
    )
