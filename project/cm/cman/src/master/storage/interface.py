import logging
from mongoengine import connect
import uuid

from .schemas import node_to_schema, schema_to_node, node_to_dict, Node
from .schemas import job_to_schema, schema_to_job, job_to_dict, Job
from ...node import Node as NodeClass
from ...job import Job as JobClass
from ...job import JobStatus


logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)


class Storage:
    def __init__(self, hostname, port, database_name):
        self.hostname  = hostname
        self.port      = port
        self.database_name  = database_name
        connect(host=f"mongodb://{self.hostname}:{self.port}/{self.database_name}")

    def register_node(self, node: NodeClass) -> bool:
        try:
            existing_node = Node.objects(node_id__exact=node.node_id)
            if existing_node is not None and hasattr(existing_node, "first"):
                existing_node = existing_node.first()
                if existing_node is not None and hasattr(existing_node, "update"):
                    _logger.info(f"Re-registering existing node {node.node_id}...")
                    existing_node.update(**node_to_dict(node))
                    return True
            node_inst = node_to_schema(node)
            if node_inst:
                _logger.info(f"Registering node {node.node_id}...")
                node_inst.save()
            return True
        except:
            return False

    def get_all_nodes(self):
        try:
            return [schema_to_node(n) for n in Node.objects]
        except:
            return None

    def create_job(self, job: JobClass) -> bool:
        job_inst = job_to_schema(job)
        if job_inst:
            _logger.info(f"Creating job record...")
            job_inst.save()
        return schema_to_job(job_inst)

    def update_job(self, job: JobClass) -> bool:
        existing_job = Job.objects(job_id__exact=job.job_id)
        if existing_job is not None and hasattr(existing_job, "first"):
            existing_job = existing_job.first()
            if existing_job is not None and hasattr(existing_job, "update"):
                existing_job.update(**job_to_dict(job, for_mongo=True))
                return schema_to_job(existing_job)
        return None

    def get_jobs(self):
        try:
            return [schema_to_job(j) for j in Job.objects.select_related()]
        except:
            return None

    def get_remaining_jobs(self):
        try:
            return [schema_to_job(j) for j in Job.objects(status__exact=JobStatus.Pending).select_related()]
        except:
            return None

    def get_alive_jobs(self):
        try:
            return [schema_to_job(j) for j in Job.objects(status__nin=[JobStatus.Killed, JobStatus.Completed]).select_related()]
        except:
            return None
