import logging
from mongoengine import StringField, IntField, FloatField, EnumField
from mongoengine import EmbeddedDocument, Document, EmbeddedDocumentListField
from ...resource import ResourceType
from ...resource import Resource as ResourceClass
from ...node import Node as NodeClass


logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)


class Resource(EmbeddedDocument):
    resource_name     = StringField(required=True)
    resource_type     = EnumField(ResourceType, required=True)
    resource_capacity = FloatField(required=True)


class Node(Document):
    node_id   = StringField(required=True)
    node_type = StringField(required=True)
    resources = EmbeddedDocumentListField(Resource)


def node_to_dict(node):
    if hasattr(node, "node_id") and hasattr(node, "node_type") and hasattr(node, "resources") and type(node.resources) is list:
        resource_list = [
            {
                "resource_name": r.name,
                "resource_type": r.rtype,
                "resource_capacity": r.capacity
            } for r in node.resources if hasattr(r, "name") and hasattr(r, "rtype") and hasattr(r, "capacity")
        ]

        node_dict = {
            "node_id": node.node_id,
            "node_type": node.node_type,
            "resources": resource_list,
        }
        return node_dict
    return None


def node_to_schema(node):
    node_dict = node_to_dict(node)
    if node_dict is not None:
        return Node(**node_dict)
    return None

def schema_to_node(node_schema: Node) -> NodeClass:
    resources = [
        ResourceClass(name=r.resource_name, resource_type=r.resource_type, capacity=r.resource_capacity)
        for r in node_schema.resources
    ]
    return NodeClass(
        node_id=node_schema.node_id,
        node_type=node_schema.node_type,
        resources=resources
    )

