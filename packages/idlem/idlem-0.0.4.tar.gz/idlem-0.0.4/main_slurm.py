"""script to be run on Zhores cluster"""
from logging import log
import os
import sys
import nvsmi
import hydra
import platform
import threading
import subprocess
from time import sleep
from typing import List
from loguru import logger
from omegaconf import OmegaConf

import idlem.utils as ut
from idlem.arg_parser import ConfigSlurm

# setup logger
logger.configure(handlers=[{"sink": sys.stdout, "format": "{time:[MM-DD HH:mm:ss]} - {message}"}])


@hydra.main(config_path="./configs/", config_name="config_slurm.yaml")
def main(cfg: ConfigSlurm):
    logger.info(OmegaConf.to_yaml(cfg, resolve=True))
    # hydra changes dir. need to undo this
    os.chdir(hydra.utils.get_original_cwd())

    cfg.miner.server.user += f".{platform.node()}"  # set unique name for each node

    while True:
        num_running = ut.slurm_num_running()
        on_schedule = ut.is_in_time_range(cfg.scheduler.data)
        log_str = f"Current mining jobs: {num_running}/{cfg.max_schedule_jobs if on_schedule else cfg.max_idle_jobs}. "
        logger.info(log_str + f"On schedule: {'True' if on_schedule else 'False'}")

        if on_schedule:
            if num_running < cfg.max_schedule_jobs:
                logger.info("spawning more miners")
                ut.slurm_submit_mining_jobs(num_jobs=cfg.max_schedule_jobs - num_running)

        if not on_schedule:
            if num_running > cfg.max_idle_jobs:
                logger.info("Too many miners not on schedule. Killing")
                ut.slurm_kill_all()
                sleep(10)  # give jobs enough time to die
                num_running = ut.slurm_num_running()

            if num_running < cfg.max_idle_jobs:
                logger.info("Spawning more miners")
                ut.slurm_submit_mining_jobs(num_jobs=cfg.max_idle_jobs - num_running)

        sleep(cfg.sleep_time)


if __name__ == "__main__":
    main()
