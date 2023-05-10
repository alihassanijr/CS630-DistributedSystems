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


class ZmqBase:
    def __init__(self, hostname, port):
        self.hostname  = hostname or 'localhost'
        self.port      = port
        self.context   = zmq.Context()
        self.sock      = None
        self.sock_type = "None"
        _logger.info(f"Initialized Zero-MQ context.")

    def open(self):
        if self.sock is None:
            raise NotImplementedError(f"Base class does not implement open.")
        self.sock.bind(f"tcp://{self.hostname}:{self.port}")
        _logger.info(f"Bound {self.sock_type} socket to {self.hostname}:{self.port}")

    def close(self):
        if self.sock:
            self.sock.close()
            del self.sock
        self.context.term()
        del self.context

    def __del__(self):
        self.close()

