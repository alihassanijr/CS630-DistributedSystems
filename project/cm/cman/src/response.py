import logging
from enum import Enum
from typing import Any

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)


class Response(Enum):
    UnhandledRequest = 0

    RegisterationSuccessful = 1
    RegisterationUnsuccessful = 2

    FetchSuccessful = 3
    FetchUnsuccessful = 4

