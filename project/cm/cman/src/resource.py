import logging
import os
from enum import Enum

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)


class ResourceType(Enum):
    Memory = 0
    CPU    = 1
    GPU    = 2


class Resource:
    def __init__(self, name: str, resource_type: ResourceType, capacity: float):
        self.name = name
        self.rtype = resource_type
        self.capacity = capacity

    def __str__(self):
        return f"Resource(name={self.name}, type={self.rtype}, capacity={self.capacity})"
