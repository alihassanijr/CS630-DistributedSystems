import logging

from ..configuration import config
from ..commons import lag
from ..mw.socket import ReplySocket
from ..response import Response
from ..node import Node

from .handler import handle_message

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)



def incoming_routine(node: Node):
    _logger.info("Starting message service")
    sock = ReplySocket(hostname="0.0.0.0", port=config.req_port)
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
        start_failures = node.queue.run_queued_jobs()
        if len(start_failures) > 0:
            _logger.info(f"Failed to start the following jobs: {start_failures}.")
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
        lag(config.status_lag)
