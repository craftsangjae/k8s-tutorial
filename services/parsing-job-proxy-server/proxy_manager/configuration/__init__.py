from typing import TypeVar, Type, Union

from proxy_manager.configuration.common import CombinedSettings
from proxy_manager.configuration.spawner import SpawnerSettings
from proxy_manager.configuration.storage import StorageSettings

ALL_SETTINGS = (StorageSettings, SpawnerSettings)
SettingsType = TypeVar('SettingsType', StorageSettings, SpawnerSettings)


def load_proxy_configurations(*configuration_types: Type[SettingsType]) -> Union[SettingsType, CombinedSettings]:
    """ 환경설정들을 불러옵니다.
    필요한 환경설정 별로 동적으로 불러올 수 있습니다.


    2. load_proxy_configurations(StorageSettings)

    1. K8S Spawner에 대한 환경설정만 불러오고 싶은 경우
    ````python
    from proxy_manager.configuration import StorageSettings, load_proxy_configurations
    settings = load_proxy_configurations(StorageSettings)
    ````

    2. K8S Storage에 대한 환경설정만 불러오고 싶은 경우
    ````python
    from proxy_manager.configuration import SpawnerSettings, load_proxy_configurations
    settings = load_proxy_configurations(SpawnerSettings)
    ````

    3. 모든 환경설정만 불러오고 싶은 경우
    ````python
    from proxy_manager.configuration import load_proxy_configurations
    settings = load_proxy_configurations()
    ````


    :param configuration_types:
    :return:
    """
    if not configuration_types:
        configuration_types = ALL_SETTINGS

    # 단일 설정 타입만 로드하는 경우, 해당 타입을 직접 반환
    if len(configuration_types) == 1:
        return configuration_types[0]()

    return CombinedSettings(*[ct() for ct in configuration_types])
