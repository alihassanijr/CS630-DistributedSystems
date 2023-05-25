import logging
from enum import Enum

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)


class Action(Enum):
    NoAction        = 0
    RegisterNode    = 1
    FetchNode       = 2
    FetchNodes      = 3
    CreateUser      = 4
    RemoveUser      = 5
    ModifyUser      = 6
    FetchUser       = 7
    GetNodeStatus   = 8
    AssignJobId     = 9
    HostJob         = 10
    StartJob        = 11
    FetchJobs       = 12
    ReportJobStart  = 13
    ReportJobEnd    = 14
    FreeResources   = 15


ACTION_MAP = {
    "user": {
        "create": Action.CreateUser,
        "remove": Action.RemoveUser,
        "modify": Action.ModifyUser,
        "show":   Action.FetchUser,
    },
    "node": {
        "show":   Action.FetchNode,
    }
}


def get_action(entity, action):
    if entity in ACTION_MAP and action in ACTION_MAP[entity]:
        return ACTION_MAP[entity][action]
    elif entity in ACTION_MAP:
        raise NotImplementedError(f"Action {action} not implemented for {entity}.")
    raise NotImplementedError(f"Invalid entity {entity}.")
