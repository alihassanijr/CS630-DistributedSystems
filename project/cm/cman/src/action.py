import logging
from enum import Enum
from typing import Any

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)


class Action(Enum):
    NoAction        = 0
    RegisterNode    = 1

