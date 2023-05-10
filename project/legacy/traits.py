import logging
import os
import uuid

ENV      = os.environ

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)


SERVER_TYPE_HEAD    = "head"
SERVER_TYPE_COMPUTE = "node"

ALLOWED_TYPES = [SERVER_TYPE_HEAD, SERVER_TYPE_COMPUTE]

class Traits:
    def __init__(self):
        assert "CM_SERVER_TYPE" in ENV, f"Failed to fetch server traits, expected `CM_SERVER_TYPE` environment variable."
        self.server_type = ENV["CM_SERVER_TYPE"]
        assert self.server_type in ALLOWED_TYPES, f"Server of type {self.server_type} is not supported! " + \
            f"Supported types: {ALLOWED_TYPES}."
        _logger.info(f"Server of type {self.server_type} starting...")
        assert self.is_head() or "CM_MASTER_ADDR" in ENV, f"Failed to fetch compute node traits, expected `CM_MASTER_ADDR` environment variable."
        if self.is_head():
            self.master_addr = '0.0.0.0'
        else:
            self.master_addr = ENV["CM_MASTER_ADDR"]
        self.node_id = str(uuid.uuid4())
        self.resources = []

    def is_head(self):
        return (self.server_type == SERVER_TYPE_HEAD)

    def is_compute(self):
        return (self.server_type == SERVER_TYPE_COMPUTE)
