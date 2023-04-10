import _thread
import logging
import socket

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)


class Socket:
    def __init__(self, hostname=None, sock=None):
        if sock:
            self.sock = sock
            self.hostname = None
        else:
            assert hostname is not None, f"Expected hostname, got {hostname}."
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.hostname = hostname
            _logger.info(f"Initialized streaming socket with hostname: {self.hostname}")
        self.port = None
        self.num_connections = None

    def bind(self, port):
        assert (
            self.hostname is not None
        ), f"Cannot re-bind an existing socket to port {port}."
        self.port = port
        self.sock.bind((self.hostname, port))
        _logger.info(f"Binding streaming socket to {self.hostname}:{self.port}")

    def connect(self, hostname, port):
        _logger.info(
            f"Connecting streaming socket at {self.hostname}:{self.port} to"
            f" {hostname}:{port}"
        )
        self.sock.connect((hostname, port))

    def listen(self, num_connections):
        assert self.hostname is not None, f"Cannot call listen on an existing socket."
        self.num_connections = num_connections
        self.sock.listen(num_connections)
        _logger.info(
            f"Socket listening at {self.hostname}:{self.port} with"
            f" {num_connections} max connections."
        )

    def send(self, content):
        bytes_sent = 0
        while bytes_sent < len(content):
            buff = bytes(content[bytes_sent:], encoding="utf-8")
            bytes_sent += self.sock.send(buff)

    def receive(self, max_len=1024):
        chunks = []
        bytes_recd = 0
        while True:
            chunk = self.sock.recv(max_len)
            if chunk == b"":
                raise RuntimeError("socket connection broken")
            if not chunk:
                break
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
            if len(chunk) < max_len:
                break
        msg = b"".join(chunks)
        return msg

    def close(self):
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
