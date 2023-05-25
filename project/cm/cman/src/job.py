import logging
from enum import Enum

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)

from .base import CMObject


class JobStatus(Enum):
    Created   = 0
    Pending   = 1
    Started   = 2
    Running   = 3
    Completed = 4
    Killed    = 5
    Unknown   = 6


class Job(CMObject):
    def __init__(self,
                 job_id,
                 job_name,
                 uid,
                 command,
                 working_dir,
                 env,
                 resource_req=None,
                 time_limit=-1,
                 nodes_reserved=None,
                 status=JobStatus.Pending
        ):
        self.job_id         = job_id
        self.job_name       = job_name
        self.uid            = uid
        self.command        = command
        self.env            = env
        self.working_dir    = working_dir
        self.resource_req   = resource_req
        self.time_limit     = None if time_limit is None or time_limit < 1 else time_limit
        self.nodes_reserved = nodes_reserved
        self.status         = status

    def merge(self, new_job):
        for attr in ["job_id", "job_name", "uid", "command", "resource_req", "time_limit", "nodes_reserved", "status"]:
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
            f"working_dir={self.working_dir}, " + \
            f"command={self.command}, " + \
            f"time_limit={self.time_limit}, " + \
            f"nodes_reserved={self.nodes_reserved}, " + \
            f"resource_req={self.resource_req}, " + \
            f"status={self.status}, " + \
            f")"

    def update_nodes(self, nodes):
        if self.nodes_reserved is None or len(self.nodes_reserved) < 1:
            self.nodes_reserved = nodes
            return self
        node_ids = {n.node_id: i for i, n in enumerate(self.nodes_reserved)}
        for n in nodes:
            if n.node_id in node_ids:
                self.nodes_reserved[node_ids[n.node_id]] = n
        return self

    def start(self):
        self.status = JobStatus.Started
        return self


class JobProcess(CMObject):
    def __init__(self, pid, status):
        self.pid = pid
        self.status = status

    def __str__(self):
        return f"Process(" + \
            f"pid={self.pid}, " + \
            f"status={self.status}" + \
            f")"
