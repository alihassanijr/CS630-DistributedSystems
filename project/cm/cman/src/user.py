import logging

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)


class User:
    def __init__(self, uid: int, username: str, fullname: str):
        self.uid = uid
        self.username = username
        self.fullname = fullname

    def __str__(self):
        return f"User(uid={self.uid}, username={self.username}, fullname={self.fullname})"

