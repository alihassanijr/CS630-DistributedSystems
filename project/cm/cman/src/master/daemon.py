import logging

from ..configuration import config
from ..commons import lag
from ..mw.socket import ReplySocket
from ..response import Response
from ..node import Node

from .handler import handle_message
from .scheduler import try_assign_job, start_job, fetch_available_nodes
from .job import update_job, get_remaining_jobs

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)



def incoming_routine(node: Node):
    _logger.info("Starting message service")
    sock = ReplySocket(hostname="0.0.0.0", port=config.daemon_port)
    sock.open()
    while True:
        _logger.info("Checking for messages")
        message = sock.receive()
        if message is not None:
            _logger.info(f"Head received message: {message}")
            response = handle_message(node, message)
            _logger.info(f"Head responding with: {response}")
            sock.send(response)
            _logger.info("Sent response.")

    sock.close()


def scheduling_routine(node: Node):
    _logger.info("Starting scheduler")
    while True:
        _logger.debug("Checking scheduler")
        jobs = get_remaining_jobs(node)
        avail_nodes = fetch_available_nodes(node)
        if avail_nodes is not None and len(avail_nodes) > 0 and jobs is not None and len(jobs) > 0:
            for job in jobs:
                status, job = try_assign_job(node, job, avail_nodes)
                if status:
                    for i, n in enumerate(job.nodes_reserved):
                        n = start_job(node, job, n, node_rank=i)
                        assert node.storage.register_node(n), f"Failed to update node {n}... Exiting."
                    assert update_job(node, job), f"Updating job failed: {job}"
        lag(config.scheduler_lag)
