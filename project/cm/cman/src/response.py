import logging
from enum import Enum

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)


class Response(Enum):
    UnhandledRequest            = 0

    RegisterationSuccessful     = 1
    RegisterationUnsuccessful   = 2

    FetchSuccessful             = 3
    FetchUnsuccessful           = 4

    UserCreationSuccessful      = 5
    UserCreationUnsuccessful    = 6

    StatusFetchSuccessful       = 7
    StatusFetchUnsuccessful     = 8

    AssignJobIdSuccessful       = 9
    AssignJobIdUnsuccessful     = 10

    JobHostingSuccessful        = 11
    JobHostingUnsuccessful      = 12

    JobStartSuccessful          = 13
    JobStartUnsuccessful        = 14
