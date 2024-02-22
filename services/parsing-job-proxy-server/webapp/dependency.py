from typing import Annotated

from fastapi import Depends

from proxy_manager.configuration import SpawnerSettings
from proxy_manager.spawner import K8SJobSpawner


def settings_dependency() -> SpawnerSettings:
    """ Spawner에 대한 환경변수 정보
    :return:
    """
    return SpawnerSettings()


def job_spawner_dependency(
        settings: Annotated[SpawnerSettings, Depends(settings_dependency)]
) -> K8SJobSpawner:
    """ K8SJobSpawner에 대한 환경변수 정보

    :param settings:
    :return:
    """
    return K8SJobSpawner(settings.spawner_namespace)
