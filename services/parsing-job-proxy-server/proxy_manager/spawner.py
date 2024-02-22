import logging
from typing import List

from kubernetes import client, config
from kubernetes.client import V1Job, ApiException
from kubernetes.config import ConfigException

from proxy_manager.exceptions import FailedJobRequestException, MissingConfigException, NotExistJobException, \
    AlreadyExistedJobException

logger = logging.getLogger(__name__)


class K8SJobSpawner:
    """ K8SJob에 대한 컨테이너를 생성/삭제/조회하는 로직

    * jupyterhub에서 노트북 instance을 생성하는 로직을 Spawner라고 부르는 데에서 착안
    """

    def __init__(self, namespace: str = 'default'):
        """
        :param namespace: 생성할 쿠버네티스 클러스터의 namespace
        """
        self.namespace = namespace
        self._load_configuration()
        self.batch_client = client.BatchV1Api()

    def create(self, job_name: str, image: str, commands: List[str]):
        """ job 생성하기

        :param job_name: 생성할 job의 이름
        :param image: 생성할 job의 이미지
        :param commands: 생성할 job에게 넘길 commands 파라미터 리스트
        :return:
        """
        if self.exist(job_name):
            raise AlreadyExistedJobException(f"{self.namespace}에 이미 {job_name}이 존재합니다.")

        job_object = self._create_job_object(job_name, image, commands)
        try:
            res = self.batch_client.create_namespaced_job(self.namespace, job_object)
        except ApiException as e:
            raise FailedJobRequestException(f"K8SJobController.create 실패했습니다. reason:{e.reason}")
        return res

    def delete(self, job_name: str):
        """ job 삭제하기

        :param job_name: 삭제할 job의 이름
        :return:
        """
        if not self.exist(job_name):
            raise NotExistJobException(f"{self.namespace}에 {job_name}이 존재하지 않습니다.")

        try:
            res = self.batch_client.delete_namespaced_job(job_name, self.namespace)
        except ApiException as e:
            raise FailedJobRequestException(f"K8SJobController.delete 실패했습니다. reason:{e.reason}")
        return res

    def exist(self, job_name: str) -> bool:
        """ job이 존재하는지 여부

        :param job_name:
        :return:
        """
        try:
            res = self.batch_client.list_namespaced_job(self.namespace, label_selector=f"app={job_name}")
            return len(res.items) > 0
        except ApiException as e:
            raise FailedJobRequestException(f"K8SJobController.exist 실패했습니다. reason:{e.reason}")

    @classmethod
    def _load_configuration(cls):
        try:
            # run in k8s cluster
            config.load_incluster_config()
        except ConfigException:
            # run in local host
            logger.warning("Service host/port is not set. use load_kube_config instead")
            try:
                config.load_kube_config()
            except ConfigException:
                logger.warning("unable to test. this app should be launched on K8S Infra.")
                raise MissingConfigException("K8S에 대한 설정이 존재하지 않습니다.")

    @classmethod
    def _create_job_object(
            cls,
            job_name: str,
            image: str,
            commands: List[str]
    ) -> V1Job:
        container = client.V1Container(
            name=job_name,
            image=image,
            command=commands
        )

        # Create and configure a spec section
        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={"app": job_name}),
            spec=client.V1PodSpec(restart_policy="Never", containers=[container]))

        # Create the specification of deployment
        spec = client.V1JobSpec(
            template=template,
            backoff_limit=4
        )

        # Instantiate the job object
        return client.V1Job(
            api_version="batch/v1",
            kind="Job",
            metadata=client.V1ObjectMeta(name=job_name),
            spec=spec)
