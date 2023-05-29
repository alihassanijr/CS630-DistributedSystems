import logging

from ..configuration import config
from ..commons import lag, send_message_to_head, send_message_to_node
from ..mw.socket import ReplySocket
from ..message import Message
from ..action import Action
from ..response import Response
from ..node import Node

from .handler import handle_message

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)


def report_job_start(node, job):
    msg = Message(
        node_id=node.node_id,
        action=Action.ReportJobStart,
        response=None,
        content=job)
    message, success = send_message_to_head(msg)
    if success and message is not None and message.response == Response.JobStartRecorded:
        return True
    return False


def report_job_end(node, job):
    msg = Message(
        node_id=node.node_id,
        action=Action.ReportJobEnd,
        response=None,
        content=job)
    message, success = send_message_to_head(msg)
    if success and message is not None and message.response == Response.JobEndRecorded:
        return True
    return False


def free_resources(node, job):
    msg = Message(
        node_id=node.node_id,
        action=Action.FreeResources,
        response=None,
        content=job.job_id)
    message, success = send_message_to_node(node, msg)
    if success and message is not None and message.response == Response.ResourcesFreed:
        return True
    return False


def incoming_routine(node: Node):
    _logger.info("Starting message service")
    sock = ReplySocket(hostname="0.0.0.0", port=config.daemon_port)
    sock.open()
    while True:
        _logger.debug("Waiting for message")
        message = sock.receive()
        _logger.debug(f"Received message: {message}")
        response = handle_message(node, message)
        _logger.debug(f"Handled message: {response}")
        sock.send(response)
        _logger.debug("Sent response.")

    sock.close()


def scheduling_routine(node: Node):
    _logger.info("Starting scheduler process on compute node")
    while True:
        _logger.debug("Checking scheduler")
        node.queue = node.queue.load()
        start_failures, started_jobs = node.queue.run_queued_jobs()
        if len(start_failures) > 0:
            _logger.info(f"Failed to start the following jobs: {start_failures}.")
        for j in started_jobs:
            assert report_job_start(node, j), f"Failed to report job {j.job_id} as started to head node!"
        lag(config.scheduler_lag)


def status_routine(node: Node):
    _logger.info("Starting status process on compute node")
    while True:
        _logger.debug("Checking status")
        node.queue = node.queue.load()
        procs = node.queue.check_running_jobs()
        for job_id, proc_list in procs.items():
            _logger.info(f"Job {job_id} : {proc_list}")
        overtime_jobs = node.queue.get_overtime_jobs()
        if len(overtime_jobs) > 0:
            _logger.info(f"Overtime jobs: {overtime_jobs}.")
        result = node.queue.kill_overtime_jobs()
        if not result:
            _logger.warning(f"Failed to kill overtime jobs!")
        completed_jobs = node.queue.clear_completed_jobs()
        for j in completed_jobs:
            assert report_job_end(node, j), f"Failed to report job {j.job_id} as complete to head node!"
            assert free_resources(node, j), f"Failed to report job {j.job_id} as complete to self!"
        lag(config.status_lag)
