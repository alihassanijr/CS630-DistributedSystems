import logging
import zmq
from time import sleep

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)


class PubSubBase:
    """
    Base class for Zero-MQ publisher and subscribe.
    """
    def __init__(self, hostname, port):
        self.hostname = hostname or 'localhost'
        self.port     = port
        self.context  = zmq.Context()
        self.sock     = None
        _logger.info(f"Initialized Zero-MQ context.")

    def open(self):
        raise NotImplementedError(f"Base class does not implement open.")

    def close(self):
        if self.sock:
            self.sock.close()
            del self.sock
        self.context.term()
        del self.context

    def __del__(self):
        self.close()


class Publisher(PubSubBase):
    def __init__(self, hostname, port):
        super().__init__(hostname, port)
        self.sock     = self.context.socket(zmq.PUB)
        _logger.info(f"Initialized PUB socket at {self.hostname}:{self.port}")

    def open(self):
        self.sock.bind(f"tcp://{self.hostname}:{self.port}")
        sleep(1)
        _logger.info(f"Bound PUB socket to {self.hostname}:{self.port}")

    def publish(self, topic, content):
        self.sock.send_string(f"{topic} {content}")

    def publish_object(self, topic, obj):
        self.sock.send_string(topic, flags=zmq.SNDMORE)
        self.sock.send_json(obj)


class Subscriber(PubSubBase):
    def __init__(self, hostname, port):
        super().__init__(hostname, port)
        self.sock = self.context.socket(zmq.SUB)
        _logger.info(f"Initialized SUB socket at {self.hostname}:{self.port}")

    def open(self):
        self.sock.connect(f"tcp://{self.hostname}:{self.port}")
        _logger.info(f"Connected SUB socket to {self.hostname}:{self.port}")

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
