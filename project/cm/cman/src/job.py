import logging
from enum import Enum

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)


class Job:
    def __init__(self, job_id, job_name, uid, command, resource_req=None, time_limit=-1, nodes_reserved=None):
        self.job_id         = job_id
        self.job_name       = job_name
        self.uid            = uid
        self.command        = command
        self.resource_req   = resource_req
        self.time_limit     = time_limit
        self.nodes_reserved = nodes_reserved

    def merge(self, new_job):
        for attr in ["job_id", "job_name", "uid", "command", "resource_req", "time_limit", "nodes_reserved"]:
            if hasattr(new_job, attr) and hasattr(self, attr):
                setattr(self, attr, getattr(new_job, attr) or getattr(self, attr))
            elif hasattr(new_job, attr):
                setattr(self, attr, getattr(new_job, attr))
            elif hasattr(self, attr):
                setattr(self, attr, getattr(new_job, attr))
        return self

    def __str__(self):
        return f"Job(" + \
            f"job_id={self.job_id}, " + \
            f"job_name={self.job_name}, " + \
            f"uid={self.uid}, " + \
            f"command={self.command}, " + \
            f"time_limit={self.time_limit}, " + \
            f"nodes_reserved={self.nodes_reserved}, " + \
            f"resource_req={self.resource_req}, " + \
            f")"
