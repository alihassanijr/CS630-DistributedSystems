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


def try_assign_job(current_node: Node, job: Job):
    from time import sleep
    _logger.info(f"Trying to schedule job {job}")
    # TODO: write scheduler
    sleep(0.1)
    return False, job
