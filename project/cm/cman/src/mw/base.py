import logging
import zmq
from time import sleep

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)


def zmq_send(socket, content):
    socket.send_pyobj(content)
    # if type(content) is bytes:
    #     return socket.send(content)
    # elif type(content) is str:
    #     return socket.send_string(content)
    # elif type(content) is dict:
    #     return socket.send_json(content)
    # elif type(content) is dict:
    #     return socket.send_json(content)
    # raise NotImplementedError(f"I don't know how to transmit object of type {type(content)}")

def zmq_recv(socket):
    return socket.recv_pyobj()

def zmq_recv_nonblocking(socket):
    try:
        return socket.recv_pyobj(flags=zmq.NOBLOCK)
    except zmq.Again as e:
        return None


class ZmqBase:
    def __init__(self, hostname, port, verbose=False):
        self.hostname  = hostname or 'localhost'
        self.port      = port
        self.sock      = None
        self.sock_type = "None"
        self.verbose = verbose
        self.init_context()

    def init_context(self):
        self.context   = zmq.Context()
        if self.verbose:
            _logger.info(f"Initialized Zero-MQ context.")

    def set_timeout(self, timeout):
        if self.sock is None:
            raise NotImplementedError(f"Base class does not implement set_timeout.")
        self.sock.setsockopt(zmq.LINGER,   0)
        self.sock.setsockopt(zmq.AFFINITY, 1)
        self.sock.setsockopt(zmq.RCVTIMEO, timeout)

    def open(self):
        if self.sock is None:
            raise NotImplementedError(f"Base class does not implement open.")
        if self.port is not None:
            self.sock.bind(f"tcp://{self.hostname}:{self.port}")
        else:
            self.port = self.sock.bind_to_random_port(f"tcp://{self.hostname}")
        if self.verbose:
            _logger.info(f"Bound {self.sock_type} socket to {self.hostname}:{self.port}")

    def restart(self):
        self.close()
        self.init_context()
        self.open()

    def close(self):
        if hasattr(self, "sock") and self.sock:
            self.sock.close()
            del self.sock
        if hasattr(self, "context") and self.context:
            self.context.term()
            del self.context

    def __del__(self):
        self.close()

