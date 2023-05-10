from mongoengine import connect
import uuid

from .schemas import node_to_schema
from ...node import Node as Node


class Configuration:
    def __init__(self, hostname, port, instance):
        self.hostname  = hostname
        self.port      = port
        self.instance  = instance
        connect(host=f"mongodb://{self.hostname}:{self.port}/{self.instance}")

    def register_node(self, node: Node):
        try:
            node_inst = node_to_schema(node)
            if node_inst:
                node_inst.save()
                return True
        except:
            pass
        return False
