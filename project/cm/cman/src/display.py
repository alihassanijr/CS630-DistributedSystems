import logging

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)

import os
import pwd

from rich.console import Console
from rich.table import Table
from rich.align import Align

from .resource import ResourceType


def _print_table(title, headers, values):
    table = Table(show_header=bool(title), header_style="bold", title=title)
    for h in headers:
        table.add_column(h, justify="center")
    for r in values:
        table.add_row(*r)
    return table


def print_table(title, headers, values):
    console = Console()
    console.print(_print_table(title, headers, values))

def print_nodes(nodes):
    headers = ["Node", "Status", "# CPUs", "Memory", "# Free CPUs", "Free Memory"]
    rows = {"head": [], "compute": []}
    for n in nodes:
        n_cpus = 0
        memory = 0
        n_cpus_free = 0
        memory_free = 0
        for r in n.resources:
            if r.rtype == ResourceType.CPU:
                n_cpus += r.capacity
                n_cpus_free += r.free
            elif r.rtype == ResourceType.Memory:
                memory += r.capacity
                memory_free += r.free

        rows["head" if n.is_head() else "compute"].append([
            str(n.node_id),
            str(n.status.name),
            str(n_cpus),
            str(memory),
            str(n_cpus_free),
            str(memory_free)
        ])

    print_table("Head nodes", headers=headers, values=rows["head"])
    print_table("Compute nodes", headers=headers, values=rows["compute"])


def print_jobs(jobs):
    headers = ["ID", "Name", "User", "Status", "Command", "Nodes"]
    rows = []
    for j in jobs:
        rows.append([
            str(j.job_id),
            str(j.job_name),
            str(pwd.getpwuid(j.uid).pw_name),
            str(j.status.name),
            str(j.command)[:20],
            ", ".join([n.node_id for n in j.nodes_reserved]),
        ])

    print_table("Jobs", headers=headers, values=rows)
