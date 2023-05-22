import logging
from ..action import Action
from ..response import Response
from ..message import Message
from ..node import Node
from ..job import Job


logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)


def register_node(
    current_node: Node,
    node: Node
):
    try:
        result = current_node.storage.register_node(node)
        if result:
            _logger.info(f"Node {node.node_id} of type {node.node_type} registered.")
            return Message(
                node_id=current_node.node_id,
                action=Action.NoAction,
                response=Response.RegisterationSuccessful,
                content=f"Successfully registered node.")
    except:
        pass
    return Message(
        node_id=current_node.node_id,
        action=Action.NoAction,
        response=Response.RegisterationUnsuccessful,
        content=f"Failed to register node.")


def create_job(
    current_node: Node,
    job: Job
):
    try:
        result = current_node.storage.create_job(job)
        if result:
            _logger.info(f"Job {result.job_id} created.")
            return Message(
                node_id=current_node.node_id,
                action=Action.NoAction,
                response=Response.AssignJobIdSuccessful,
                content=result)
    except:
        pass
    return Message(
        node_id=current_node.node_id,
        action=Action.NoAction,
        response=Response.AssignJobIdUnsuccessful,
        content=f"Failed to create job.")
