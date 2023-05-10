from mongoengine import StringField, IntField
from mongoengine import EmbeddedDocument, Document, EmbeddedDocumentListField


class Resource(EmbeddedDocument):
    resource_name = StringField(required=True)
    resource_type = StringField(required=True)
    resource_capacity = IntField(required=True)


class Node(Document):
    node_id   = StringField(required=True)
    node_type = StringField(required=True)
    resources = EmbeddedDocumentListField(Resource)

def node_to_schema(node):
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
        return Node(**node_dict)
    return None
