from typing import List

from fastapi import FastAPI
from kubernetes import client, config
from kubernetes.config.config_exception import ConfigException
import logging
import json

from proxy_server.dto import JobInfo, CreateJobRequest, DeleteJobRequest, JobStatusResponse

# load k8s configuration
try:
    # run in k8s cluster
    config.load_incluster_config()
except ConfigException:
    # run in local host
    logging.warning("Service host/port is not set. use load_kube_config instead")
    config.load_kube_config()

# load k8s client
batch_v1 = client.BatchV1Api()

app = FastAPI()


@app.get("/")
async def health_check():
    return "ok"


@app.get('/jobs')
async def list_jobs(namespace="default") -> List[JobInfo]:
    """ returns the list of jobs
    """
    ret = batch_v1.list_namespaced_job(namespace=namespace)
    return [
        JobInfo(name=item.metadata.name, namespace=item.metadata.namespace,
                active=item.status.active, failed=item.status.failed,
                ready=item.status.ready, succeeded=item.status.succeeded) for item in ret.items
    ]


@app.post("/jobs", status_code=201)
async def create_job(req: CreateJobRequest):
    """ create job
    """
    job_object = create_job_object(req.name, req.value)
    res = batch_v1.create_namespaced_job(req.namespace, job_object)
    return JobStatusResponse(status=str(res.status))


@app.delete("/jobs")
async def delete_job(req: DeleteJobRequest):
    """ delete specific job
    """
    res = batch_v1.delete_namespaced_job(req.name, req.namespace)
    return JobStatusResponse(status=str(res.status))


def create_job_object(job_name: str, value=10):
    # Configure Pod template container
    container = client.V1Container(
        name=job_name,
        image="perl",
        command=["perl", "-Mbignum=bpi", "-wle", f"print bpi({value})"])

    # Create and configure a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": job_name}),
        spec=client.V1PodSpec(restart_policy="Never", containers=[container]))

    # Create the specification of deployment
    spec = client.V1JobSpec(
        template=template,
        backoff_limit=4)

    # Instantiate the job object
    return client.V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=client.V1ObjectMeta(name=job_name),
        spec=spec)
