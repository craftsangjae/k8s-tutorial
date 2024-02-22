from pydantic import Field

from proxy_manager.configuration.common import CommonSettings


class SpawnerSettings(CommonSettings):
    ##################
    # spawner 관련된 설정
    ##################
    spawner_namespace: str = Field(description="k8s spawner에서 job을 생성할 namespace")
