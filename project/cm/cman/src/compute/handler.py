import logging
from typing import Any
from ..action import Action
from ..response import Response
from ..message import Message
from ..node import Node
from ..mw.socket import RequestSocket


logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)


def handle_message(master_node: Node, message: Any, head_sock: RequestSocket):
    if type(message) is Message:
        pass
    else:
        return Message(
            node_id=master_node.node_id,
            action=Action.NoAction,
            response=Response.UnhandledRequest,
            content=f"Unexpected message type: {type(message)}.")

    _logger.info(f"Message from node {message.node_id} not handled; unexpected action: {message.action}.")
    return Message(
        node_id=master_node.node_id,
        action=Action.NoAction,
        response=Response.UnhandledRequest,
        content=f"Unexpected action: {message.action}.")

