import logging
import zmq
from .base import ZmqBase, zmq_send, zmq_recv, zmq_recv_nonblocking
from time import sleep

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)


class BaseSocket(ZmqBase):
    def send(self, content):
        try:
            zmq_send(self.sock, content)
            return True
        except:
            return False

    def receive(self):
        try:
            return zmq_recv(self.sock)
        except:
            if hasattr(self, "timeout") and self.timeout is not None:
                self.restart()
            return None

    def receive_nb(self):
        return zmq_recv_nonblocking(self.sock)


class RequestSocket(BaseSocket):
    def __init__(self, timeout, hostname="0.0.0.0", port=None, target_hostname=None, target_port=None):
        self.timeout = timeout
        self.target_hostname = target_hostname
        self.target_port     = target_port
        super().__init__(hostname, port)

    def init_context(self):
        super().init_context()
        self.sock = self.context.socket(zmq.REQ)
        self.sock_type = "REQ"
        _logger.info(f"Initialized {self.sock_type} socket at {self.hostname}:{self.port}")
        self.set_timeout(self.timeout)

    def open(self, target_hostname=None, target_port=None):
        self.target_hostname = target_hostname or self.target_hostname
        self.target_port = target_port or self.target_port
        super().open()
        assert self.target_hostname is not None and self.target_port is not None, f"Expected a target hostname and port, got {self.target_hostname} and {self.target_port}"
        _logger.info(f"Connecting {self.sock_type} socket to tcp://{self.target_hostname}:{self.target_port}")
        self.sock.connect(f"tcp://{self.target_hostname}:{self.target_port}")
        _logger.info(f"Connected {self.sock_type} socket to {self.target_hostname}:{self.target_port}")


class ReplySocket(BaseSocket):
    def init_context(self):
        super().init_context()
        self.sock = self.context.socket(zmq.REP)
        self.sock_type = "REP"
        _logger.info(f"Initialized {self.sock_type} socket at {self.hostname}:{self.port}")
