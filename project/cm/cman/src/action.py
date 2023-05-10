import logging
from enum import Enum

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)


class Action(Enum):
    NoAction        = 0
    RegisterNode    = 1
    FetchNodes      = 2

