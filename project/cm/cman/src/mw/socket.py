import logging
import zmq
from .base import ZmqBase, zmq_send, zmq_recv
from time import sleep

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)


class BaseSocket(ZmqBase):
    def send(self, content):
        return zmq_send(self.sock, content)

    def receive(self):
        return zmq_recv(self.sock)


class RequestSocket(BaseSocket):
    def __init__(self, hostname, port):
        super().__init__(hostname, port)
        self.sock = self.context.socket(zmq.REQ)
        self.sock_type = "REQ"
        _logger.info(f"Initialized {self.sock_type} socket at {self.hostname}:{self.port}")

    def open(self, target_hostname, target_port):
        super().open()
        self.sock.connect(f"tcp://{target_hostname}:{target_port}")
        _logger.info(f"Connected {self.sock_type} socket to {target_hostname}:{target_port}")


class ReplySocket(BaseSocket):
    def __init__(self, hostname, port):
        super().__init__(hostname, port)
        self.sock = self.context.socket(zmq.REP)
        self.sock_type = "REP"
        _logger.info(f"Initialized {self.sock_type} socket at {self.hostname}:{self.port}")
