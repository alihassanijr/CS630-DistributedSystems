import logging
import os
import subprocess
import time
import pickle

import psutil

from .configuration import config
from .base import CMObject
from .job import Job, JobProcess, JobStatus

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)


PSUTIL_RUNNING = [
    psutil.STATUS_RUNNING,
    psutil.STATUS_SLEEPING,
    psutil.STATUS_DISK_SLEEP,
    psutil.STATUS_WAKING,
    psutil.STATUS_IDLE,
    psutil.STATUS_LOCKED,
    psutil.STATUS_WAITING,
    psutil.STATUS_PARKED,
]


PSUTIL_COMPLETED = [
    psutil.STATUS_STOPPED,
    psutil.STATUS_TRACING_STOP,
    psutil.STATUS_ZOMBIE,
]


PSUTIL_KILLED = [
    psutil.STATUS_DEAD,
]


def timestamp():
    return time.time()


def time_diff_h(t1, t2):
    return (t1 - t2) / (60 * 60)


def start_process(node_id, proc_index, uid, cwd, env, cmd):
    log_dir = f"{cwd}/cmlogs/{node_id}"
    os.makedirs(log_dir, exist_ok=True)
    out_path = f"{log_dir}/{proc_index}.out.txt"
    err_path = f"{log_dir}/{proc_index}.err.txt"
    out_file = open(out_path, "w")
    err_file = open(err_path, "w")
    p = subprocess.Popen(
        [cmd],
        env=env,
        cwd=cwd,
        user=uid,
        shell=True,
        stdout=out_file,
        stderr=err_file,
    )
    return p.pid


class Queue(CMObject):
    def __init__(self, node_id):
        self.node_id = node_id
        self.jobs = {}
        self.pids = {}
        self.start_times = {}
        self.assign_context_path()
        self.flush()

    def assign_context_path(self):
        ts  = int(time.time() * 1000)
        _context_dir = f"/tmp/cm/queues/{self.node_id}_{ts}"
        self._context_path = f"{_context_dir}/queue.obj"
        os.makedirs(_context_dir, exist_ok=True)
        return True

    def __str__(self):
        return f"Queue(jobs={self.jobs})"

    def add(self, job: Job):
        self = self.load()
        assert job.job_id not in self.jobs and job.job_id not in self.pids, f"Job {job.job_id} is already running in this queue."
        self.jobs[job.job_id] = job
        self.pids[job.job_id] = []
        self.flush()
        return self

    def flush(self):
        with open(self._context_path, 'wb') as fh:
            pickle.dump({"jobs": self.jobs, "pids": self.pids, "start_times": self.start_times}, fh)
        return self

    def load(self):
        with open(self._context_path, 'rb') as fh:
            inst = pickle.load(fh)
            self.jobs = inst["jobs"]
            self.pids = inst["pids"]
            self.start_times = inst["start_times"]
        return self

    def start(self, job: Job):
        return self.start_by_id(job.job_id)

    def start_by_id(self, job_id: int):
        self = self.load()
        if job_id in self.pids and job_id in self.jobs and len(self.pids[job_id]) == 0 and job_id not in self.start_times:
            self.start_times[job_id] = []
            n_procs = self.jobs[job_id].resource_req.n_per_node
            cmd = self.jobs[job_id].command
            cwd = self.jobs[job_id].working_dir
            env = self.jobs[job_id].env
            uid = self.jobs[job_id].uid
            for i in range(n_procs):
                pid = start_process(self.node_id, i, uid, cwd, env, cmd)
                self.pids[job_id].append(pid)
                self.start_times[job_id].append(timestamp())
            self.flush()
            return True
        return False

    def get_unstarted_jobs(self):
        self = self.load()
        job_ids = []
        for job_id in self.jobs.keys():
            if job_id not in self.pids or len(self.pids[job_id]) == 0:
                job_ids.append(job_id)
        return job_ids

    def run_queued_jobs(self):
        failures = []
        for i in self.get_unstarted_jobs():
            stat = self.start_by_id(i)
            if not stat:
                failures.append(i)
        return failures

    def get_running_jobs(self):
        self = self.load()
        job_ids = []
        for job_id in self.jobs.keys():
            if job_id in self.pids and len(self.pids[job_id]) > 0:
                job_ids.append(job_id)
        return job_ids

    def get_overtime_jobs(self):
        self = self.load()
        job_ids = []
        for job_id in self.jobs.keys():
            if job_id in self.pids and len(self.pids[job_id]) > 0:
                assert job_id in self.start_times, f"Unhandled error: job {job_id} has PIDs, but not start times."
                assert len(self.start_times[job_id]) == len(self.pids[job_id]), f"Unhandled error: job {job_id} has PIDs, but not start times."
                if self.jobs[job_id].time_limit is None:
                    continue
                for pid, start_time in zip(self.pids[job_id], self.start_times[job_id]):
                    if time_diff_h(timestamp(), start_time) > self.jobs[job_id].time_limit:
                        job_ids.append(job_id)
                        continue
        return job_ids

    def check_running_jobs(self):
        status_dict = {}
        for i in self.get_running_jobs():
            status_list = []
            for pid in self.pids[i]:
                status = JobStatus.Unknown
                try:
                    if pid is not None and type(pid) is int and psutil.pid_exists(pid):
                        proc = psutil.Process(pid=pid).as_dict()
                        if proc["status"] in PSUTIL_RUNNING:
                            status = JobStatus.Running
                        elif proc["status"] in PSUTIL_KILLED:
                            status = JobStatus.Killed
                        elif proc["status"] in PSUTIL_COMPLETED:
                            status = JobStatus.Completed
                except:
                    pass
                status_list.append(JobProcess(pid=pid, status=status))
            status_dict[i] = status_list
        return status_dict


