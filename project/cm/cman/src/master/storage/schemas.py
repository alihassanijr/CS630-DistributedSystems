import logging
from mongoengine import StringField, IntField, FloatField, EnumField
from mongoengine import EmbeddedDocument, EmbeddedDocumentField, Document, EmbeddedDocumentListField
from mongoengine import ReferenceField, SequenceField, ListField
from ...resource import ResourceType
from ...resource import Resource as ResourceClass
from ...resource import ResourceRequirement as ResourceRequirementClass
from ...node import Node as NodeClass
from ...job import Job as JobClass
from ...job import JobStatus


logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)


class Resource(EmbeddedDocument):
    resource_name     = StringField(required=True)
    resource_type     = EnumField(ResourceType, required=True)
    resource_capacity = FloatField(required=True)


class ResourceRequirement(EmbeddedDocument):
    n_nodes = IntField(required=True)
    n_cpus_per_node = IntField(required=True)
    mem_per_node = IntField(required=True)


class Node(Document):
    node_id   = StringField(required=True)
    node_type = StringField(required=True)
    resources = EmbeddedDocumentListField(Resource)


class Job(Document):
    job_id         = SequenceField(required=True)
    job_name       = StringField()
    uid            = IntField(required=True)
    command        = StringField(required=True)
    time_limit     = IntField()
    nodes_reserved = ListField(ReferenceField(Node))
    resource_req   = EmbeddedDocumentField(ResourceRequirement, required=True)
    status         = EnumField(JobStatus, required=True)


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


def job_to_dict(job):
    if hasattr(job, "job_name") and hasattr(job, "uid") and hasattr(job, "command") and hasattr(job, "status") and \
            hasattr(job, "resource_req") and hasattr(job.resource_req, "n_nodes") \
            and hasattr(job.resource_req, "n_cpus_per_node") and hasattr(job.resource_req, "mem_per_node"):
        resource_req = {
            "n_nodes": job.resource_req.n_nodes,
            "n_cpus_per_node": job.resource_req.n_cpus_per_node,
            "mem_per_node": job.resource_req.mem_per_node,
            }
        job_dict = {
            "job_name": job.job_name,
            "uid": job.uid,
            "command": job.command,
            "resource_req": resource_req,
            "status": job.status,
        }
        if hasattr(job, "job_id") and job.job_id is not None:
            job_dict["job_id"] = job.job_id
        if hasattr(job, "time_limit"):
            job_dict["time_limit"] = job.time_limit
        if hasattr(job, "nodes_reserved") and job.job_id is not None:
            job_dict["nodes_reserved"] = job.nodes_reserved
        return job_dict
    return None


def node_to_schema(node):
    node_dict = node_to_dict(node)
    if node_dict is not None:
        return Node(**node_dict)
    return None


def job_to_schema(job):
    job_dict = job_to_dict(job)
    if job_dict is not None:
        return Job(**job_dict)
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


def schema_to_job(job_schema: Job) -> JobClass:
    return JobClass(
        job_id=job_schema.job_id,
        job_name=job_schema.job_name,
        uid=job_schema.uid,
        command=job_schema.command,
        resource_req=ResourceRequirementClass(
            n_nodes=job_schema.resource_req.n_nodes,
            n_cpus_per_node=job_schema.resource_req.n_cpus_per_node,
            mem_per_node=job_schema.resource_req.mem_per_node
        ),
        time_limit=job_schema.time_limit,
        nodes_reserved=job_schema.nodes_reserved
    )

