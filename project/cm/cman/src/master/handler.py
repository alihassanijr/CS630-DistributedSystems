import logging
from typing import Any
from ..action import Action
from ..response import Response
from ..message import Message
from ..node import Node
from ..job import Job
from ..user import User
from ..status import Status
from .register import register_node
from .job import create_job
from .fetch import fetch_nodes
from .adduser import adduser


logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)


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


def assign_job_id_handler(current_node: Node, message: Message):
    if type(message.content) is Job:
        return create_job(current_node=current_node, job=message.content)
    return Message(
        node_id=current_node.node_id,
        action=Action.NoAction,
        response=Response.UnhandledRequest,
        content=f"Expected type Job, got {type(message.content)}")


def create_user_handler(current_node: Node, message: Message):
    if type(message.content) is User:
        return adduser(current_node=current_node, user=message.content)
    return Message(
        node_id=current_node.node_id,
        action=Action.NoAction,
        response=Response.UnhandledRequest,
        content=f"Expected type User, got {type(message.content)}")


ACTION_TO_HANDLER = {
    Action.GetNodeStatus: get_status,
    Action.RegisterNode:  node_register_handler,
    Action.FetchNodes:    fetch_all_handler,
    Action.CreateUser:    create_user_handler,
    Action.AssignJobId:   assign_job_id_handler,
}


def handle_message(current_node: Node, message: Any):
    if type(message) is Message:
        pass
    else:
        return Message(
            node_id=current_node.node_id,
            action=Action.NoAction,
            response=Response.UnhandledRequest,
            content=f"Unexpected message type: {type(message)}.")

    if message.action in ACTION_TO_HANDLER:
        return ACTION_TO_HANDLER[message.action](current_node=current_node, message=message)

    _logger.info(f"Message from node {message.node_id} not handled; unexpected action: {message.action}.")
    return Message(
        node_id=current_node.node_id,
        action=Action.NoAction,
        response=Response.UnhandledRequest,
        content=f"Unexpected action: {message.action}.")
