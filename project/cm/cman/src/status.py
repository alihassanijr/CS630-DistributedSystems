import logging
from enum import Enum

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)


class Status(Enum):
    Down  = 0
    Idle  = 1
    InUse = 2


class DownReason(Enum):
    Unreachable = 0
    FailedToRespond = 1
    InvalidResponse = 2
    RespondedDown = 3
    StatusFetchExecutionFailed = 4
    FetchFailedAtNode = 5
    Unknown = 6
