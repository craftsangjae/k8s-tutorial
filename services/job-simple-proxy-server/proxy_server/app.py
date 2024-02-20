from typing import List, Union

from fastapi import FastAPI, Response
from kubernetes import client, config
from kubernetes.config.config_exception import ConfigException
from kubernetes.client.exceptions import ApiException
import logging

from proxy_server.dto import JobInfo, CreateJobRequest, DeleteJobRequest, JobStatusResponse

# load k8s configuration
try:
    # run in k8s cluster
    config.load_incluster_config()
except ConfigException:
    # run in local host
    logging.warning("Service host/port is not set. use load_kube_config instead")
    try:
        config.load_kube_config()
    except ConfigException:
        logging.warning("unable to test. this app should be launched on K8S Infra.")
        raise

# load k8s client
batch_v1 = client.BatchV1Api()

app = FastAPI()


@app.get("/")
async def health_check():
    return "ok"


@app.get('/jobs')
async def list_jobs(response: Response, namespace="default") -> Union[List[JobInfo], str]:
    """ returns the list of jobs
    """
    try:
        ret = batch_v1.list_namespaced_job(namespace=namespace)
    except ApiException as e:
        response.status_code = 403
        return f"ApiException : {e.reason}"

    return [
        JobInfo(name=item.metadata.name, namespace=item.metadata.namespace,
                active=item.status.active, failed=item.status.failed,
                ready=item.status.ready, succeeded=item.status.succeeded) for item in ret.items
    ]


@app.post("/jobs", status_code=201)
async def create_job(req: CreateJobRequest, response: Response) -> Union[JobStatusResponse, str]:
    """ create job
    """
    job_object = create_job_object(req.name, req.value)
    try:
        res = batch_v1.create_namespaced_job(req.namespace, job_object)
    except ApiException as e:
        response.status_code = 403
        return f"ApiException : {e.reason}"

    return JobStatusResponse(status=str(res.status))


@app.delete("/jobs")
async def delete_job(req: DeleteJobRequest, response: Response) -> Union[JobStatusResponse, str]:
    """ delete specific job
    """
    try:
        res = batch_v1.delete_namespaced_job(req.name, req.namespace)
    except ApiException as e:
        response.status_code = 403
        return f"ApiException : {e.reason}"
    
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
