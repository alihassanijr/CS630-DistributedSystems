import logging
from ..action import Action
from ..response import Response
from ..message import Message
from ..node import Node
from ..job import Job


logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)


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


def update_job(
    current_node: Node,
    job: Job
):
    try:
        result = current_node.storage.update_job(job)
        if result:
            _logger.info(f"Job {result.job_id} updated.")
            return True
    except:
        pass
    return False


def get_jobs(
    current_node: Node
):
    try:
        return current_node.storage.get_jobs()
    except:
        pass
    return None


def get_remaining_jobs(
    current_node: Node
):
    try:
        return current_node.storage.get_remaining_jobs()
    except:
        pass
    return None
