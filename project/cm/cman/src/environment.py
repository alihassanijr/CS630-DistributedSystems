import logging
import os
# import uuid
import platform

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


def get_storage(master_node):
    from src.master import Storage
    assert "CM_DATABASE_ADDR" in ENV, f"Could not find database address in environment variables (`CM_DATABASE_ADDR`)."
    assert "CM_DATABASE_PORT" in ENV, f"Could not find database portnum in environment variables (`CM_DATABASE_PORT`)."
    assert "CM_DATABASE_NAME" in ENV, f"Could not find database name in environment variables (`CM_DATABASE_NAME`)."
    return Storage(hostname=ENV["CM_DATABASE_ADDR"], port=ENV["CM_DATABASE_PORT"], database_name=ENV["CM_DATABASE_NAME"])


def is_head():
    return get_node_type() == SERVER_TYPE_HEAD


def get_head_addr():
    if not is_head():
        return ENV["CM_MASTER_ADDR"]
    return '0.0.0.0'
