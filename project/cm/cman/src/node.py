import logging
import os
import uuid
import platform
from time import sleep

from .mw.socket import RequestSocket, ReplySocket
from .action import Action
from .message import Message
from .resource import ResourceType, Resource
from .response import Response
from .status import Status, Reason
from .configuration import config

ENV = os.environ

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)

SERVER_TYPE_HEAD    = "head"
SERVER_TYPE_COMPUTE = "node"

ALLOWED_TYPES = [SERVER_TYPE_HEAD, SERVER_TYPE_COMPUTE]


#def generate_node_id():
#    return str(uuid.uuid4())

def get_node_id():
    return platform.node()

def get_node_type():
    assert "CM_SERVER_TYPE" in ENV, f"Failed to fetch server traits, expected `CM_SERVER_TYPE` environment variable."
    node_type = ENV["CM_SERVER_TYPE"]
    assert node_type in ALLOWED_TYPES, f"Node of type {node_type} is not supported! " + \
        f"Supported types: {ALLOWED_TYPES}."
    return node_type

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

def running_jobs():
    return False

def get_storage(master_node):
    from src.master import Storage
    assert "CM_DATABASE_ADDR" in ENV, f"Could not find database address in environment variables (`CM_DATABASE_ADDR`)."
    assert "CM_DATABASE_PORT" in ENV, f"Could not find database portnum in environment variables (`CM_DATABASE_PORT`)."
    assert "CM_DATABASE_NAME" in ENV, f"Could not find database name in environment variables (`CM_DATABASE_NAME`)."
    return Storage(hostname=ENV["CM_DATABASE_ADDR"], port=ENV["CM_DATABASE_PORT"], database_name=ENV["CM_DATABASE_NAME"])

class Node:
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

    def self_update(self):
        if self.is_head():
            self.status = Status.Up
        else:
            self.status = Status.InUse if running_jobs() else Status.Idle
        self.status_reason = Reason.NoReason
        return self

    def update(self, requesting_node=None):
        try:
            if requesting_node.node_id == self.node_id:
                self.self_update()
            else:
                self.status, self.status_reason = get_node_status(self)
        except:
            self.status, self.status_reason = Status.Down, Reason.StatusFetchExecutionFailed
        return self

def get_node():
    node = Node(node_id=get_node_id(), node_type=get_node_type(), resources=None)
    node.resources = get_resources(is_head=node.is_head())
    _logger.info(f"Node of type {node.node_type} starting...")
    if node.is_head():
        node.master_addr = '0.0.0.0'
    else:
        node.master_addr = ENV["CM_MASTER_ADDR"]
    return node

def is_head():
    return get_node_type() == SERVER_TYPE_HEAD

def get_head_addr():
    if not is_head():
        return ENV["CM_MASTER_ADDR"]
    return '0.0.0.0'


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
        head_sock = RequestSocket(timeout=config.request_timeout, hostname="0.0.0.0", port=config.rep_port)
        head_sock.open(node.master_addr, config.req_port)
        registered = False
        for _ in range(config.register_retries):
            _logger.info("Registering node")
            if head_sock.send(generate_register_message(node)):
                _logger.info("Waiting for response")
                message = head_sock.receive()
                _logger.info(f"Child received message: {message}")
                if message is not None and message.response == Response.RegisterationSuccessful:
                    _logger.info(f"Registered with head node successfully. Proceeding.")
                    registered = True
                    break
                else:
                    _logger.info(f"Node registration failed. Retrying...")
                    sleep(config.register_retry_wait)
            else:
                _logger.info(f"Node registration failed (request was not delivered). Retrying...")
                sleep(config.register_retry_wait)

        if not registered:
            raise RuntimeError(f"Failed to register with head node after {config.register_retries} attempts. Quitting.")
        head_sock.close()

def get_node_status(node):
    sock = RequestSocket(timeout=config.request_timeout)
    sock.open(node.node_id, config.req_port)
    _logger.info(f"Pinging node {node.node_id}")
    if sock.send(generate_status_message(node)):
        _logger.info("Waiting for response")
        message = sock.receive()
        _logger.info(f"Received : {message}")
        if message is None:
            sock.close()
            return Status.Down, Reason.FailedToRespond
        if not hasattr(message, "response"):
            sock.close()
            return Status.Down, Reason.InvalidResponse

        if message.response == Response.StatusFetchSuccessful:
            _logger.info(f"Fetched node status successfully.")
            sock.close()
            return message.content, None
        else:
            _logger.info(f"Fetching node status was not successful.")
            sock.close()
            return Status.Down, Reason.FetchFailedAtNode

        sock.close()
        return Status.Down, Reason.InvalidResponse
    else:
        _logger.info("Failed to send request to node.")
        return Status.Down, Reason.Unreachable

def generate_register_message(node):
    return Message(
        node_id=node.node_id,
        action=Action.RegisterNode,
        response=None,
        content=node)

def generate_status_message(node):
    return Message(
        node_id=node.node_id,
        action=Action.GetNodeStatus,
        response=None,
        content=node)
