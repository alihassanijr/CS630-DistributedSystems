import logging
import zmq
from .base import ZmqBase
from time import sleep

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)


class Publisher(ZmqBase):
    def __init__(self, hostname, port):
        super().__init__(hostname, port)
        self.sock      = self.context.socket(zmq.PUB)
        self.sock_type = "PUB"
        _logger.info(f"Initialized {self.sock_type} socket at {self.hostname}:{self.port}")

    def open(self):
        super().open()
        sleep(1)

    def publish(self, topic, content):
        self.sock.send_string(f"{topic} {content}")

    def publish_object(self, topic, obj):
        self.sock.send_string(topic, flags=zmq.SNDMORE)
        self.sock.send_json(obj)


class Subscriber(ZmqBase):
    def __init__(self, hostname, port):
        super().__init__(hostname, port)
        self.sock = self.context.socket(zmq.SUB)
        self.sock_type = "SUB"
        _logger.info(f"Initialized {self.sock_type} socket at {self.hostname}:{self.port}")

    def subscribe(self, topic):
        self.sock.subscribe(topic)

    def receive(self):
        message = self.sock.recv_string()
        message_split = message.split(" ")
        topic = message_split[0]
        message = message[len(topic)+1:]
        return topic, message

    def receive_object(self):
        topic = self.sock.recv_string()
        obj   = self.sock.recv_json()
        return topic, obj
