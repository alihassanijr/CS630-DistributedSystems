import logging
from typing import Any
from ..action import Action
from ..response import Response
from ..message import Message
from ..node import Node
from ..job import Job, JobStatus
from ..user import User
from ..status import Status
from .register import register_node
from .job import create_job_msg, get_alive_jobs_msg, update_job_start_msg, update_job_end_msg
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


def fetch_nodes_handler(current_node: Node, message: Message):
    return fetch_nodes(current_node=current_node)


def fetch_jobs_handler(current_node: Node, message: Message):
    return get_alive_jobs_msg(current_node=current_node)


def assign_job_id_handler(current_node: Node, message: Message):
    if type(message.content) is Job:
        return create_job_msg(current_node=current_node, job=message.content)
    return Message(
        node_id=current_node.node_id,
        action=Action.NoAction,
        response=Response.UnhandledRequest,
        content=f"Expected type Job, got {type(message.content)}")


def report_job_start_handler(current_node: Node, message: Message):
    if type(message.content) is Job:
        incoming_node = current_node.storage.fetch_node(message.node_id)
        if type(incoming_node) is not Node:
            return Message(
                node_id=current_node.node_id,
                action=Action.NoAction,
                response=Response.UnhandledRequest,
                content=f"Unable to find reference to incoming node in storage: {message.node_id}.")
        return update_job_start_msg(current_node=current_node, job=message.content, incoming_node=incoming_node)
    return Message(
        node_id=current_node.node_id,
        action=Action.NoAction,
        response=Response.UnhandledRequest,
        content=f"Expected type Job, got {type(message.content)}")


def report_job_end_handler(current_node: Node, message: Message):
    if type(message.content) is Job:
        incoming_node = current_node.storage.fetch_node(message.node_id)
        if type(incoming_node) is not Node:
            return Message(
                node_id=current_node.node_id,
                action=Action.NoAction,
                response=Response.UnhandledRequest,
                content=f"Unable to find reference to incoming node in storage: {message.node_id}.")
        return update_job_end_msg(current_node=current_node, job=message.content, incoming_node=incoming_node)
    return Message(
        node_id=current_node.node_id,
        action=Action.NoAction,
        response=Response.UnhandledRequest,
        content=f"Expected type Job, got {type(message.content)}")


def kill_job_handler(current_node: Node, message: Message):
    try:
        job = current_node.storage.get_job_by_id(message.content)
        assert job is not None, f"Couldn't fetch job with id {message.content} from storage."
        if job.status in [JobStatus.Completed, JobStatus.Killed]:
            return Message(
                node_id=current_node.node_id,
                action=Action.NoAction,
                response=Response.JobAlreadyDone,
                content=None)
        for node in job.nodes_running:
            node.end_job(current_node, job.job_id)
        return Message(
            node_id=current_node.node_id,
            action=Action.NoAction,
            response=Response.KillSignalSent,
            content=None)
    except:
        pass
    return Message(
        node_id=current_node.node_id,
        action=Action.NoAction,
        response=Response.UnhandledRequest,
        content="Unable to send kill signal.")


def create_user_handler(current_node: Node, message: Message):
    if type(message.content) is User:
        return adduser(current_node=current_node, user=message.content)
    return Message(
        node_id=current_node.node_id,
        action=Action.NoAction,
        response=Response.UnhandledRequest,
        content=f"Expected type User, got {type(message.content)}")


ACTION_TO_HANDLER = {
    Action.GetNodeStatus:  get_status,
    Action.RegisterNode:   node_register_handler,
    Action.FetchNodes:     fetch_nodes_handler,
    Action.FetchJobs:      fetch_jobs_handler,
    Action.CreateUser:     create_user_handler,
    Action.AssignJobId:    assign_job_id_handler,
    Action.ReportJobStart: report_job_start_handler,
    Action.ReportJobEnd:   report_job_end_handler,
    Action.KillJob:        kill_job_handler,
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
