import logging
import os
from enum import Enum
from typing import Optional

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)


class ResourceType(Enum):
    Memory = 0
    CPU    = 1
    GPU    = 2


class Resource:
    def __init__(self, name: str, resource_type: ResourceType, capacity: float, users: Optional[list] = None):
        self.name = name
        self.rtype = resource_type
        self.capacity = capacity
        self.users = users or []

    def __str__(self):
        return f"Resource(name={self.name}, type={self.rtype}, capacity={self.capacity}, free={self.free})"

    @property
    def free(self):
        total_usage = 0
        for _, usage in self.users:
            total_usage += usage
        assert total_usage <= self.capacity, f"This resource was over-allocated: {self.name} of type {self.rtype}."
        return self.capacity - total_usage

    def can_allocate(self, amnt):
        if amnt > self.free:
            return False
        return True

    def allocate(self, user_id, amnt):
        if self.can_allocate(amnt):
            self.users.append((user_id, amnt))
            return True
        return False


class ResourceRequirement:
    def __init__(self, n_nodes, n_cpus_per_node, mem_per_node):
        self.n_nodes = n_nodes
        self.n_cpus_per_node = n_cpus_per_node
        self.mem_per_node = mem_per_node

    def __str__(self):
        return f"ResourceRequirement(" + \
            f"n_nodes={self.n_nodes}, " + \
            f"n_cpus_per_node={self.n_cpus_per_node}, " + \
            f"mem_per_node={self.mem_per_node}, " + \
            f"total_cpus={self.n_cpus_per_node * self.n_nodes}, " + \
            f"total_mem={self.mem_per_node * self.n_nodes}" + \
            f")"
