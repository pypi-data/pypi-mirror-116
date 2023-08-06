from typing import List, Any
from dataclasses import dataclass, field
from omegaconf import MISSING

from hydra.core.config_store import ConfigStore


@dataclass
class BaseConfig:
    # Hydra will populate this field based on the defaults list
    miner: Any = MISSING
    sleep_time: int = 300
    debug: bool = False
    # flag to update version of GMiner
    update_miner: bool = False


@dataclass
class Config(BaseConfig):
    scheduler: Any = MISSING
    # Whitelist users. Would start mining even if they are logged in. If any other user logs in, will kill miner
    allowed_users: List[str] = field(default_factory=lambda: ["zakirov"])


@dataclass
class ConfigSlurm(BaseConfig):
    scheduler: Any = MISSING
    max_schedule_jobs: int = 2
    max_idle_jobs: int = 2


cs = ConfigStore.instance()
cs.store(name="strict_config_base", node=BaseConfig)
cs.store(name="strict_config", node=Config)
cs.store(name="strict_config_slurm", node=ConfigSlurm)
