from typing import List, Union

from fastapi import FastAPI, Response
from kubernetes import client, config
from kubernetes.config.config_exception import ConfigException
from kubernetes.client.exceptions import ApiException
import logging

from proxy_server.dto import CronJobInfo, CreateCronJobRequest, DeleteJobRequest, JobStatusResponse

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


@app.get('/cron-jobs')
async def list_cron_jobs(response: Response, namespace="default") -> Union[List[CronJobInfo], str]:
    """ returns the list of cron jobs
    """
    try:
        ret = batch_v1.list_namespaced_cron_job(namespace=namespace)
    except ApiException as e:
        response.status_code = 403
        return f"ApiException : {e.reason}"

    return [
        CronJobInfo(
            name=item.metadata.name, namespace=item.metadata.namespace, schedule=item.spec.schedule,
            created_at=item.metadata.creation_timestamp, last_success_at=item.status.last_schedule_time,
            last_scheduled_at=item.status.last_successful_time
        )
        for item in ret.items
    ]


@app.post("/cron-jobs", status_code=201)
async def create_cron_job(req: CreateCronJobRequest, response: Response) -> Union[JobStatusResponse, str]:
    """ create cron-jobs
    """
    job_object = create_cronjob_object(req.name, req.schedule)

    try:
        res = batch_v1.create_namespaced_cron_job(req.namespace, job_object)
    except ApiException as e:
        response.status_code = 403
        return f"ApiException : {e.reason}"

    return JobStatusResponse(status=str(res.status))


@app.delete("/cron-jobs")
async def delete_job(req: DeleteJobRequest, response: Response) -> Union[JobStatusResponse, str]:
    """ delete specific job
    """
    try:
        res = batch_v1.delete_namespaced_cron_job(req.name, req.namespace)
    except ApiException as e:
        response.status_code = 403
        return f"ApiException : {e.reason}"

    return JobStatusResponse(status=str(res.status))


def create_cronjob_object(job_name: str, schedule: str):
    # Configure Pod template container
    container = client.V1Container(
        name=job_name,
        image="busybox:1.28",
        command=["/bin/sh", "-c", "date; echo Hello from the kubernetes cluster"])

    # Create and configure a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": job_name}),
        spec=client.V1PodSpec(restart_policy="Never", containers=[container]))

    # Create and configure job template spec
    job_template = client.V1JobTemplateSpec(
        metadata=client.V1ObjectMeta(name=job_name),
        spec=client.V1JobSpec(template=template))

    # Create the specification of deployment
    spec = client.V1CronJobSpec(schedule=schedule, job_template=job_template)

    # Instantiate the job object
    return client.V1CronJob(
        api_version="batch/v1",
        kind="CronJob",
        metadata=client.V1ObjectMeta(name=job_name),
        spec=spec)
