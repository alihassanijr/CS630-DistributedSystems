import logging
from ..action import Action
from ..response import Response
from ..message import Message
from ..node import Node


logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)


def fetch_nodes(
    current_node: Node
):
    try:
        result = current_node.storage.get_all_nodes()
        if result is not None:
            result = [node.update(current_node) for node in result]
            _logger.info(f"Fetched node information.")
            return Message(
                node_id=current_node.node_id,
                action=Action.NoAction,
                response=Response.FetchSuccessful,
                content=result)
    except:
        pass
    return Message(
        node_id=current_node.node_id,
        action=Action.NoAction,
        response=Response.FetchUnsuccessful,
        content=f"Failed to fetch node information.")
