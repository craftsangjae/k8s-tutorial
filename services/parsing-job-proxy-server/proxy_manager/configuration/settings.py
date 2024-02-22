from typing import Type, Union, TypeVar

from pydantic import Field

from proxy_manager.configuration.common import CombinedSettings
from proxy_manager.configuration.spawner import SpawnerSettings
from proxy_manager.configuration.storage import StorageSettings

ALL_SETTINGS = (StorageSettings, SpawnerSettings)
T = TypeVar('T', **ALL_SETTINGS)


def load_proxy_configurations(*configuration_types: Type[T]) -> Union[T, 'CombinedSettings']:
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

    # 여러 설정 타입들을 병합하는 경우, 동적으로 클래스를 생성하고 인스턴스를 반환
    for setting_cls in configuration_types:
        for field_name, field_type in setting_cls.__annotations__.items():
            default_value = getattr(setting_cls, field_name, ...)
            field_info = setting_cls.__fields__[field_name].field_info
            setattr(CombinedSettings, field_name, Field(default=default_value, **field_info))

    # 이 경우, CombinedSettings는 명시적인 타입이 없기 때문에 'CombinedSettings'라는 문자열로 타입 힌트를 제공
    return CombinedSettings()
