import logging
from typing import Any
from ..action import Action
from ..response import Response
from ..message import Message
from ..status import Status
from ..node import Node
from ..mw.socket import RequestSocket


logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)


def handle_message(current_node: Node, message: Any):
    if type(message) is Message:
        pass
    else:
        return Message(
            node_id=current_node.node_id,
            action=Action.NoAction,
            response=Response.UnhandledRequest,
            content=f"Unexpected message type: {type(message)}.")

    if message.action == Action.GetNodeStatus:
        return get_status(current_node=current_node, message=message)

    _logger.info(f"Message from node {message.node_id} not handled; unexpected action: {message.action}.")
    return Message(
        node_id=current_node.node_id,
        action=Action.NoAction,
        response=Response.UnhandledRequest,
        content=f"Unexpected action: {message.action}.")


def get_status(current_node: Node, message: Message):
    return Message(
        node_id=current_node.node_id,
        action=Action.NoAction,
        response=Response.StatusFetchSuccessful,
        content=current_node.self_update().status)

