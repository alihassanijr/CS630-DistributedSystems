import _thread
import logging

from .socket import Socket

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)


STATUS_OK = "HTTP/1.0 200 OK\n\n"
STATUS_FORBIDDEN = "HTTP/1.0 403 Forbidden\n\n"
STATUS_NOT_FOUND = "HTTP/1.0 404 Not Found\n\n"
STATUS_NOT_IMPLEMENTED = "HTTP/1.0 401 Not Implemented\n\n"


class Server:
    def __init__(self, port, hostname="", num_connections=4):
        self.socket = Socket(hostname=hostname)
        self.hostname = hostname
        self.port = port
        self.num_connections = num_connections

    def start(self):
        self.socket.bind(self.port)
        self.socket.listen(self.num_connections)
        while True:
            (clientsocket, address) = self.socket.sock.accept()
            _logger.info(
                f"[{self.hostname}:{self.port}] Request accepted from {address}"
            )
            _thread.start_new_thread(self.handle, (Socket(sock=clientsocket),))

    def handle(self, clientsocket):
        msg = clientsocket.receive()
        _logger.info(f"[{self.hostname}:{self.port}] Content received: {msg}")
        clientsocket.send(STATUS_OK)
        clientsocket.send("OK\n")
        clientsocket.close()
