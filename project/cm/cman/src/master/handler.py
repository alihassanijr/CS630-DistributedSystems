import logging
from typing import Any
from ..action import Action
from ..response import Response
from ..message import Message
from ..node import Node
from ..user import User
from ..status import Status
from .register import register_node
from .fetch import fetch_nodes
from .adduser import adduser


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

    elif message.action == Action.RegisterNode:
        return node_register_handler(current_node=current_node, message=message)

    elif message.action == Action.FetchNodes:
        return fetch_all_handler(current_node=current_node, message=message)

    elif message.action == Action.CreateUser:
        return create_user_handler(current_node=current_node, message=message)

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


def node_register_handler(current_node: Node, message: Message):
    if type(message.content) is Node:
        return register_node(current_node=current_node, node=message.content)
    return Message(
        node_id=current_node.node_id,
        action=Action.NoAction,
        response=Response.UnhandledRequest,
        content=f"Expected type Node when registering node, got {type(message.content)}")


def fetch_all_handler(current_node: Node, message: Message):
    return fetch_nodes(current_node=current_node)


def create_user_handler(current_node: Node, message: Message):
    if type(message.content) is User:
        return adduser(current_node=current_node, user=message.content)
    return Message(
        node_id=current_node.node_id,
        action=Action.NoAction,
        response=Response.UnhandledRequest,
        content=f"Expected type User, got {type(message.content)}")

