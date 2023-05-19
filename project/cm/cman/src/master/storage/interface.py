from mongoengine import connect
import uuid

from .schemas import node_to_schema, schema_to_node, Node
from ...node import Node as NodeClass


class Storage:
    def __init__(self, hostname, port, database_name):
        self.hostname  = hostname
        self.port      = port
        self.database_name  = database_name
        connect(host=f"mongodb://{self.hostname}:{self.port}/{self.database_name}")

    def register_node(self, node: NodeClass) -> bool:
        try:
            node_inst = node_to_schema(node)
            if node_inst:
                node_inst.save()
                return True
        except:
            pass
        return False

    def get_all_nodes(self):
        try:
            return [schema_to_node(n) for n in Node.objects]
        except:
            return None
