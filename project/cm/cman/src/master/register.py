import logging
from ..action import Action
from ..response import Response
from ..message import Message
from ..node import Node


logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)


def register_node(
    master_node: Node,
    node: Node
):
    try:
        result = master_node.config.register_node(node)
        if result:
            return Message(
                node_id=master_node.node_id,
                action=Action.NoAction,
                response=Response.RegisterationSuccessful,
                content=f"Successfully registered node.")
    except:
        pass
    return Message(
        node_id=master_node.node_id,
        action=Action.NoAction,
        response=Response.RegisterationUnsuccessful,
        content=f"Failed to register node.")
