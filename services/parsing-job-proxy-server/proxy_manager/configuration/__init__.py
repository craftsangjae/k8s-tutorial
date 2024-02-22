from typing import TypeVar

from proxy_manager.configuration.spawner import SpawnerSettings
from proxy_manager.configuration.storage import StorageSettings

ALL_SETTINGS = (StorageSettings, SpawnerSettings)
SettingsType = TypeVar('SettingsType', StorageSettings, SpawnerSettings)
