import logging
from enum import Enum

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)


class Status(Enum):
    Down  = 0

    # Compute node only
    Idle  = 1
    InUse = 2

    # Head node only
    Up    = 3


class Reason(Enum):
    NoReason                    = 0

    Unreachable                 = 1
    FailedToRespond             = 2
    InvalidResponse             = 3
    RespondedDown               = 4
    StatusFetchExecutionFailed  = 5
    FetchFailedAtNode           = 6
    Unknown                     = 7
