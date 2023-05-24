import logging
from typing import Any
from ..action import Action
from ..response import Response
from ..message import Message
from ..node import Node
from ..job import Job
from ..user import User
from ..status import Status


logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)


def fetch_available_nodes(current_node: Node):
    try:
        all_nodes = current_node.storage.get_all_nodes()
        avail_nodes = []
        if all_nodes is not None:
            for i, n in enumerate(all_nodes):
                if n.is_compute():
                    n = n.update(current_node)
                if n.status != Status.Down:
                    avail_nodes.append(n)
            return avail_nodes
    except:
        pass
    return None


def try_assign_job(current_node: Node, job: Job, avail_nodes: list):
    from time import sleep
    if job.resource_req.n_nodes > len(avail_nodes):
        # Not enough nodes
        _logger.debug(f"Not enough nodes to schedule job {job}")
        return False, job

    compat_nodes = []
    for n in avail_nodes:
        if n.can_host_job(job):
            compat_nodes.append(n)

    if len(compat_nodes) < job.resource_req.n_nodes:
        _logger.debug(f"Not enough resources to schedule job {job}")
        return False, job

    reserved_nodes = []
    for n in compat_nodes:
        if len(reserved_nodes) == job.resource_req.n_nodes:
            break
        result = n.reserve_resources(current_node, job)
        if result is None or type(result) is not Node:
            _logger.info(f"Failed to schedule job on node {n.node_id}: {result}")
            return False, job
        reserved_nodes.append(result)
    return True, job.update_nodes(reserved_nodes).start()


def start_job(current_node: Node, job: Job, target_node: Node):
    result = target_node.start_job(current_node, job)
    if result is None or type(result) is not Node:
        raise RuntimeError(f"Nodes promised resources, but failed to deliver.")
    return result
