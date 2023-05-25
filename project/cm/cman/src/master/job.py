import logging
from ..action import Action
from ..response import Response
from ..message import Message
from ..node import Node
from ..job import Job, JobStatus


logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)


def create_job_msg(
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


def get_alive_jobs_msg(
    current_node: Node
):
    try:
        jobs = current_node.storage.get_alive_jobs()
        return Message(
            node_id=current_node.node_id,
            action=Action.NoAction,
            response=Response.FetchSuccessful,
            content=jobs)
    except:
        pass
    return Message(
        node_id=current_node.node_id,
        action=Action.NoAction,
        response=Response.FetchUnsuccessful,
        content=f"Failed to fetch jobs.")


def update_job_start_msg(
    current_node: Node,
    job: Job,
    incoming_node: Node
):
    try:
        job = current_node.storage.get_job(job)
        job.nodes_running.append(incoming_node)
        if len(job.nodes_running) == len(job.nodes_reserved):
            job.status = JobStatus.Running
        result = current_node.storage.update_job(job)
        if result:
            return Message(
                node_id=current_node.node_id,
                action=Action.NoAction,
                response=Response.JobStartRecorded,
                content=job)
    except:
        pass
    return Message(
        node_id=current_node.node_id,
        action=Action.NoAction,
        response=Response.JobStartNotRecorded,
        content=f"Failed to update job to record end event from node.")


def update_job_end_msg(
    current_node: Node,
    job: Job,
    incoming_node: Node
):
    try:
        job = current_node.storage.get_job(job)
        job.nodes_running = [x for x in job.nodes_running if x.node_id != incoming_node.node_id]
        if len(job.nodes_running) == 0:
            job.status = JobStatus.Completed
            job.nodes_reserved = []
        result = current_node.storage.update_job(job)
        if result is not None:
            return Message(
                node_id=current_node.node_id,
                action=Action.NoAction,
                response=Response.JobEndRecorded,
                content=job)
    except:
        pass
    return Message(
        node_id=current_node.node_id,
        action=Action.NoAction,
        response=Response.JobEndNotRecorded,
        content=f"Failed to update job to record end event from node.")
