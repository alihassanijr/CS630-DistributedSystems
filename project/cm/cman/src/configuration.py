import logging
import os
import yaml

ENV      = os.environ

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
_logger = logging.getLogger(__name__)

from .base import CMObject

class Configuration(CMObject):
    def __init__(self):
        self.scheduler_lag           = 1000 # milliseconds
        self.status_lag              = 5000 # milliseconds

        self.register_retries        = 10
        self.register_retry_wait     = 5    # seconds

        self.daemon_port             = 5001

        self.num_cpus_per_child      = 2
        self.memory_per_child        = 512

        self.num_cpus_per_head       = 2
        self.memory_per_head         = 512

        self.request_timeout         = 100

        self.default_n_nodes         = 1
        self.default_n_procs         = 1
        self.default_n_cpus_per_node = 1
        self.default_mem_per_node    = 100
        self.default_time_limit      = 0

    def load(self, conf):
        for k, v in conf.items():
            if k in self.__dict__:
                self.__dict__[k] = v
        return self

    def __str__(self):
        repr_str = f"Configuration("
        for k, v in self.__dict__.items():
            repr_str += f"{k}={v}, "
        repr_str += ")"
        return repr_str


def load_configuration():
    assert "CM_PATH" in ENV, f"Could not find `CM_PATH` in environment variables."
    config_path = f"{ENV['CM_PATH']}/etc/cm-config.yml"
    with open(config_path, 'r') as f:
        config_dict = yaml.safe_load(f)
    config = Configuration().load(config_dict)
    return config

config = load_configuration()
