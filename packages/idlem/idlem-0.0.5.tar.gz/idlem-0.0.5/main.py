import os
import sys
import hydra
import platform
import threading
import subprocess
from time import sleep
from typing import List, Tuple
from loguru import logger
from omegaconf import OmegaConf

import idlem.utils as ut
from idlem.arg_parser import Config

DOCKER_NAME = "test"

# setup logger
logger.configure(handlers=[{"sink": sys.stdout, "format": "{time:[MM-DD HH:mm:ss]} - {message}"}])


class MinerThread(threading.Thread):
    def __init__(self, start_command: str):
        super().__init__()
        self.start_command = start_command

    def run(self):
        subprocess.run(self.start_command, shell=True, stdout=subprocess.DEVNULL)

    def stop(self):
        subprocess.run(f"docker kill {DOCKER_NAME}", shell=True, stdout=subprocess.DEVNULL)


class Miner:
    """High-level wrapper which handles restaring the theads"""

    def __init__(
        self,
        scheduler: List[Tuple[str, str]],
        allowed_users: List[str],
    ):
        self.scheduler = scheduler
        self.miner_thread = None
        self.start_free_gpus_set = {}
        self.allowed_users = allowed_users

        # get params str with `devices` being filled later. `python3` here is renamed miner!
        self.params_str = (
            f"""docker run --name {DOCKER_NAME} --rm -it """
            + """--gpus '\"device={devices}\"' """
            + f"""-v {os.getcwd()}:/usr/bin/logs/ -v {ut.MINER_CONFIG_PATH}:/usr/bin/config.txt gm ./python3 --config ./config.txt"""
        )

    def step(self):
        on_schedule = ut.is_in_time_range(self.scheduler)
        extra_users = ut.get_external_users(self.allowed_users)
        if extra_users:
            logger.info(f"Someone logged in: {extra_users}. Stoping.")

        # stop when someone logs in or because of scheduler
        need_stop = not on_schedule or extra_users

        new_free_gpus = set(ut.free_gpus_list()).difference(self.start_free_gpus_set)
        have_new_free_gpus = len(new_free_gpus) > 0
        # restart when can run and miner is off (or it's on, but we can grab more GPUs)
        if not need_stop and (have_new_free_gpus or not self.working):
            self.restart()

        if need_stop:
            self.stop()

        sleep(10)

    def start(self):
        self.start_free_gpus_set = set(ut.free_gpus_list())
        logger.info(f"Started mining. Using GPUs: {self.start_free_gpus_set}")
        self.miner_thread = MinerThread(self.params_str.format(devices=self.free_gpus_str))
        self.miner_thread.start()
        sleep(10)  # extra time for startup

    def stop(self):
        if not self.working:
            return
        logger.info(f"Stopped mining on gpus: {self.start_free_gpus_set}")
        self.start_free_gpus_set = {}
        self.miner_thread = self.miner_thread.stop()
        self.miner_thread = None
        sleep(10)  # make sure all processes stop

    def restart(self):
        self.stop()
        self.start()

    @property
    def num_free_gpus(self) -> int:
        return len(ut.free_gpus_list())

    @property
    def free_gpus_str(self) -> str:
        free_gpus_list = ut.free_gpus_list()
        return ",".join(free_gpus_list) if free_gpus_list else None

    @property
    def on_schedule(self):
        return ut.is_in_time_range(self.schedule_dict)

    @property
    def working(self):
        return self.miner_thread is not None


@hydra.main(config_path="./configs/", config_name="config.yaml")
def main(cfg: Config) -> None:
    logger.info(OmegaConf.to_yaml(cfg, resolve=True))

    cfg.miner.server.user += f".{platform.node()}"  # set unique name for each node
    # dump config to tmp. later this file would be mounted to docker
    ut.dump_gminer_config(cfg.miner, ut.MINER_CONFIG_PATH)

    miner = Miner(cfg.scheduler.data, cfg.allowed_users)
    while True:
        miner.step()


if __name__ == "__main__":
    main()
