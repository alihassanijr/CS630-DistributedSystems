import logging
import os
from time import sleep

from .base import CMObject
from .environment import *
from .action import Action
from .message import Message
from .resource import ResourceType, Resource
from .response import Response
from .status import Status, Reason
from .configuration import config
from .commons import send_message_to_head, send_message_to_node
from .queue import Queue

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)

def get_resources(is_head):
    if is_head:
        cpus = [
            Resource(name=f"cpu{i}", resource_type=ResourceType.CPU, capacity=1) for i in range(config.num_cpus_per_head)
        ]
        memory = [Resource(f"memory", resource_type=ResourceType.Memory, capacity=config.memory_per_head)]
        gpus = []
    else:
        cpus = [
            Resource(name=f"cpu{i}", resource_type=ResourceType.CPU, capacity=1) for i in range(config.num_cpus_per_child)
        ]
        memory = [Resource(f"memory", resource_type=ResourceType.Memory, capacity=config.memory_per_child)]
        # TODO: add GPU support
        gpus = []
    return cpus + memory + gpus

def can_host_job(node, job):
    cpu_cores_free = 0
    mem_free = 0
    for r in node.resources:
        if r.rtype == ResourceType.CPU:
            cpu_cores_free += r.free
        elif r.rtype == ResourceType.Memory:
            mem_free += r.free
    if cpu_cores_free >= job.resource_req.n_cpus_per_node and \
            mem_free >= job.resource_req.mem_per_node:
        return True
    return False

def host_job(node, job):
    allocated_cpus = 0
    allocated_mem = 0
    for r in node.resources:
        if r.rtype == ResourceType.CPU and allocated_cpus < job.resource_req.n_cpus_per_node:
            amnt = min(r.free, job.resource_req.n_cpus_per_node)
            if r.allocate(job.job_id, amnt):
                allocated_cpus += amnt
        elif r.rtype == ResourceType.Memory and allocated_mem < job.resource_req.mem_per_node:
            amnt = min(r.free, job.resource_req.mem_per_node)
            if r.allocate(job.job_id, amnt):
                allocated_mem += amnt

        if allocated_cpus == job.resource_req.n_cpus_per_node and allocated_mem == job.resource_req.mem_per_node:
            break
        elif allocated_cpus > job.resource_req.n_cpus_per_node or \
                allocated_mem > job.resource_req.mem_per_node:
            raise RuntimeError(f"Allocated more resources than necessary. This should not happen.")

    if allocated_cpus == job.resource_req.n_cpus_per_node or \
            allocated_mem == job.resource_req.mem_per_node:
        return True, node
    return False, node

def kick_job(node, job_id):
    for r in node.resources:
        r.kick(job_id)
    return True

class Node(CMObject):
    def __init__(self, node_id, node_type, resources):
        self.node_id   = node_id
        self.node_type = node_type
        self.resources = resources
        self.status = Status.Down
        self.status_reason = None

    def is_head(self):
        return (self.node_type == SERVER_TYPE_HEAD)

    def is_compute(self):
        return (self.node_type == SERVER_TYPE_COMPUTE)

    def __str__(self):
        return f"Node(id={self.node_id}, type={self.node_type},\n\tresources={[str(r) for r in self.resources]},\n\t" + \
            f"status={self.status}, status_reason={self.status_reason})"

    def can_host_job(self, job):
        return can_host_job(self, job)

    def running_jobs(self):
        for r in self.resources:
            if r.free < r.capacity:
                return True
        return False

    def self_update(self):
        if self.is_head():
            self.status = Status.Up
        else:
            self.status = Status.InUse if self.running_jobs() else Status.Idle
        self.status_reason = Reason.NoReason
        return self

    def merge(self, new_node):
        assert self.node_id == new_node.node_id and \
            self.node_type == new_node.node_type, f"Mismatch between node settings on head node and response from node itself."
        self.resources = new_node.resources
        return self

    def reserve_resources(self, requesting_node, job):
        if requesting_node.node_id == self.node_id:
            if self.can_host_job(job):
                status, self = host_job(self, job)
                if status:
                    return self
        else:
            status, self = request_host_job(requesting_node, self, job)
            if status:
                return self
        return None

    def start_job(self, requesting_node, job, node_rank):
        if requesting_node.node_id == self.node_id:
            self.status = Status.InUse
            _logger.info(f"Started job: {job}")
            assert hasattr(self, "queue"), f"Node object not initialized correctly, could not find queue!"
            self.queue = self.queue.load()
            self.queue.add(job, node_rank=node_rank)
            return self
        else:
            status, self = request_start_job(requesting_node, self, job, node_rank)
            if status:
                return self
        return None

    def end_job(self, requesting_node, job_id):
        if requesting_node.node_id == self.node_id:
            assert hasattr(self, "queue"), f"Node object not initialized correctly, could not find queue!"
            self.queue = self.queue.load()
            self.queue.safe_kill_job(job_id)
            self.queue.flush()
            kick_job(self, job_id)
            _logger.info(f"Freed resources from job: {job_id}")
            return self
        else:
            assert request_end_job(requesting_node, self, job_id), f"Failed to kill job {job_id}."
        return None

    def update(self, requesting_node):
        try:
            if requesting_node.node_id == self.node_id:
                self.self_update()
                return self
            else:
                self.status, self.status_reason, out_node = request_node_status(requesting_node, self)
                if type(out_node) is Node:
                    return self.merge(out_node)
        except:
            pass
        self.status, self.status_reason = Status.Down, Reason.StatusFetchExecutionFailed
        return self


def get_node():
    node = Node(node_id=get_node_id(), node_type=get_node_type(), resources=None)
    node.resources = get_resources(is_head=node.is_head())
    _logger.info(f"Node of type {node.node_type} starting...")
    node.master_addr = get_head_addr()
    return node


def setup_compute_daemon(node):
    if node.is_head():
        return False
    node.queue = Queue(node_id=node.node_id)
    return True


def setup_head_daemon(node):
    if not node.is_head():
        return False
    node.storage = get_storage(node)
    return True


def register_node(node):
    _logger.info("Registering node")
    if node.is_head():
        assert node.storage.register_node(node), f"Failed to self-register; terminating..."
    else:
        registered = False
        for _ in range(config.register_retries):
            _logger.info("Registering node")
            response, succ = send_message_to_head(generate_register_message(node))
            if succ and response is not None:
                if hasattr(response, "response"):
                    if response.response == Response.RegisterationSuccessful:
                        _logger.info(f"Registered with head node successfully. Proceeding.")
                        registered = True
                        break
                    else:
                        _logger.info(f"Node registration failed. Retrying...")
                else:
                    _logger.info(f"Node registration failed (head node sent invalid response). Retrying...")

            else:
                _logger.info(f"Node registration failed (request was not delivered). Retrying...")
            sleep(config.register_retry_wait)

        if not registered:
            raise RuntimeError(f"Failed to register with head node after {config.register_retries} attempts. Quitting.")


def request_node_status(requesting_node, node):
    response, succ = send_message_to_node(node, generate_status_message(requesting_node, node))
    if response is not None and succ:
        if not hasattr(response, "response") or not hasattr(response, "content"):
            return Status.Down, Reason.InvalidResponse, node
        elif response.response == Response.StatusFetchSuccessful and type(response.content) is Node:
            _logger.debug(f"Fetched node status successfully.")
            return response.content.status, None, response.content
        return Status.Down, Reason.FetchFailedAtNode, node

    elif response is None and succ:
        return Status.Down, Reason.InvalidResponse, node
    return Status.Down, Reason.Unreachable, node


def request_host_job(requesting_node, node, job):
    response, succ = send_message_to_node(node, generate_host_message(requesting_node, job))
    if response is not None and succ:
        if hasattr(response, "response") and hasattr(response, "content") and \
                response.response == Response.JobHostingSuccessful and type(response.content) is Node:
            _logger.info(f"Node hosted job successfully.")
            return True, response.content
    return False, node


def request_start_job(requesting_node, node, job, node_rank):
    response, succ = send_message_to_node(node, generate_start_job_message(requesting_node, job, node_rank))
    if response is not None and succ:
        if hasattr(response, "response") and hasattr(response, "content") and \
                response.response == Response.JobStartSuccessful and type(response.content) is Node:
            _logger.info(f"Node started job successfully.")
            return True, response.content
    return False, node


def request_end_job(requesting_node, node, job_id):
    msg = Message(
        node_id=requesting_node.node_id,
        action=Action.FreeResources,
        response=None,
        content=job_id)
    message, success = send_message_to_node(node, msg)
    if success and message is not None and message.response == Response.ResourcesFreed:
        return True
    return False


def generate_register_message(node):
    return Message(
        node_id=node.node_id,
        action=Action.RegisterNode,
        response=None,
        content=node)


def generate_status_message(requesting_node, node):
    return Message(
        node_id=requesting_node.node_id,
        action=Action.GetNodeStatus,
        response=None,
        content=node)


def generate_host_message(requesting_node, job):
    return Message(
        node_id=requesting_node.node_id,
        action=Action.HostJob,
        response=None,
        content=job)


def generate_start_job_message(requesting_node, job, node_rank):
    return Message(
        node_id=requesting_node.node_id,
        action=Action.StartJob,
        response=None,
        content=(job, node_rank))
