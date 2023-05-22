import logging
from time import sleep

from .mw.socket import RequestSocket
from .message import Message
from .node import get_head_addr
from .configuration import config

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)


def send_message(address, message):
    sock = RequestSocket(timeout=config.request_timeout)
    sock.open(address, config.req_port)
    _logger.info(f"Pinging {address}")
    if sock.send(message):
        _logger.info("Waiting for response")
        response = sock.receive()
        _logger.info(f"Received : {response}")
        sock.close()
        return response, True
    _logger.info("Failed to send request to node.")
    return None, False

def send_message_to_head(message):
    return send_message(get_head_addr(), message)

def send_message_to_node(node, message):
    return send_message(node.node_id, message)
