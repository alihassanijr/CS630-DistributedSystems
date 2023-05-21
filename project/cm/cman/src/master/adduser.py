import subprocess
import logging
from ..action import Action
from ..response import Response
from ..message import Message
from ..node import Node
from ..user import User


logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)

def create_user(uid: int, username: str, fullname: str):
    cmd = f"adduser -u {uid} -c {fullname} {username} --disabled--password"
    proc = subprocess.run(cmd, shell=True, capture_output=True, timeout=5)
    return proc.returncode == 0


def adduser(
    current_node: Node,
    user: User
):
    create_user(uid=user.uid, username=user.username, fullname=user.fullname)
    _logger.info(f"User {user.username} ({user.uid}) created.")
    return Message(
        node_id=current_node.node_id,
        action=Action.NoAction,
        response=Response.UserCreationSuccessful,
        content=f"Successfully created user.")
