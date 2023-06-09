import logging
from typing import Any
from ..action import Action
from ..response import Response
from ..message import Message
from ..status import Status
from ..node import Node
from ..job import Job


logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)


def get_status(current_node: Node, message: Message):
    return Message(
        node_id=current_node.node_id,
        action=Action.NoAction,
        response=Response.StatusFetchSuccessful,
        content=current_node.self_update())


def host_job(current_node: Node, message: Message):
    if type(message.content) is Job:
        return Message(
            node_id=current_node.node_id,
            action=Action.NoAction,
            response=Response.JobHostingSuccessful,
            content=current_node.reserve_resources(current_node, message.content))
    return Message(
        node_id=current_node.node_id,
        action=Action.NoAction,
        response=Response.JobHostingUnsuccessful,
        content=None)


def start_job(current_node: Node, message: Message):
    if type(message.content) is tuple and len(message.content) == 2 and \
            type(message.content[0]) is Job and type(message.content[1]) is int:
        job, node_rank = message.content
        return Message(
            node_id=current_node.node_id,
            action=Action.NoAction,
            response=Response.JobStartSuccessful,
            content=current_node.start_job(current_node, job, node_rank=node_rank))
    return Message(
        node_id=current_node.node_id,
        action=Action.NoAction,
        response=Response.JobStartUnsuccessful,
        content=None)


def free_resources(current_node: Node, message: Message):
    try:
        result = current_node.end_job(current_node, message.content)
        if result:
            return Message(
                node_id=current_node.node_id,
                action=Action.NoAction,
                response=Response.ResourcesFreed,
                content=None)
    except:
        pass
    return Message(
        node_id=current_node.node_id,
        action=Action.NoAction,
        response=Response.ResourcesNotFreed,
        content=None)


ACTION_TO_HANDLER = {
    Action.GetNodeStatus: get_status,
    Action.HostJob:       host_job,
    Action.StartJob:      start_job,
    Action.FreeResources: free_resources,
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

