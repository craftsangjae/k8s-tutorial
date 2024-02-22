from dataclasses import dataclass
from typing import Dict


@dataclass
class K8SJobInfo:
    name: str
    namespace: str
    creation_timestamp: str
    labels: Dict[str, str]
