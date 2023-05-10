import logging
from enum import Enum
from typing import Any, Optional
from .action import Action
from .response import Response

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)


class Message:
    def __init__(
            self,
            node_id: str,
            action: Action,
            response: Optional[Response] = None,
            content: Optional[Any] = None,
    ):
        self.node_id  = node_id
        self.action   = action
        self.response = response
        self.content  = content

    def __str__(self):
        return f"Message(" + \
            f"\t node_id={self.node_id}, action={self.action}, response={self.response}, " + \
            f"\t content={self.content})"
