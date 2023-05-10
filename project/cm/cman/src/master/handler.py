import logging
from typing import Any
from ..action import Action
from ..response import Response
from ..message import Message
from ..node import Node
from .register import register_node


logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)


def handle_message(master_node: Node, message: Any):
    if type(message) is Message:
        pass
    else:
        return Message(
            node_id=master_node.node_id,
            action=Action.NoAction,
            response=Response.UnhandledRequest,
            content=f"Unexpected message type: {type(message)}.")

    if message.action == Action.RegisterNode:
        return node_register_handler(master_node=master_node, message=message)

    _logger.info(f"Message from node {message.node_id} not handled; unexpected action: {message.action}.")
    return Message(
        node_id=master_node.node_id,
        action=Action.NoAction,
        response=Response.UnhandledRequest,
        content=f"Unexpected action: {message.action}.")


def node_register_handler(master_node: Node, message: Message):
    if type(message.content) is Node:
        return register_node(master_node=master_node, node=message.content)
    return Message(
        node_id=master_node.node_id,
        action=Action.NoAction,
        response=Response.UnhandledRequest,
        content=f"Expected type Node when registering node, got {type(message.content)}")

