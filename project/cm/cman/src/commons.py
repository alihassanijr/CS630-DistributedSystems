import logging
from time import sleep
import os

from .environment import get_head_addr
from .mw.socket import RequestSocket
from .message import Message
from .configuration import config

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)


def send_message(address, message, verbose=False, timeout=config.request_timeout):
    sock = RequestSocket(timeout=timeout, verbose=verbose)
    sock.open(address, config.daemon_port)
    if verbose:
        _logger.info(f"Pinging {address} with message: {message}")
    if sock.send(message):
        if verbose:
            _logger.info("Waiting for response")
        response = sock.receive()
        if verbose:
            _logger.info(f"Received : {response}")
        sock.close()
        return response, True
    if verbose:
        _logger.info("Failed to send request to node.")
    return None, False

def send_message_to_head(message, verbose=False, timeout=config.request_timeout):
    return send_message(get_head_addr(), message, verbose=verbose)

def send_message_to_node(node, message, verbose=False, timeout=config.request_timeout):
    return send_message(node.node_id, message, verbose=verbose)

def lag(ms):
    sleep(ms / 1000)

def get_uid():
    return os.getuid()

def get_workdir():
    return os.getcwd()
