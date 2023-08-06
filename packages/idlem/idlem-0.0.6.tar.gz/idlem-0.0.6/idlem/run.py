"""
This file is intended to run on machines were no safety precautions are needed
It doesn't hide itself and allows easy pause/un-pause for miner
"""
import os
import hydra
import platform
import subprocess
from time import sleep
from loguru import logger
from omegaconf import OmegaConf

import idlem.utils as ut
from idlem.arg_parser import Config


class Miner:
    def __init__(self, cfg: Config):
        self.miner_process = None
        self.start_free_gpus_set = {}
        self.cfg = cfg

    def step(self):

        extra_users = ut.get_external_users(self.cfg.allowed_users)
        if extra_users:
            logger.info(f"Someone external logged in: {extra_users}.")
            self.stop()
            sleep(self.cfg.long_sleep_time)
            return

        on_pause = ut.is_on_pause()
        if on_pause:
            logger.info("On pause")
            self.stop()
            return

        new_free_gpus = set(ut.free_gpus_list()).difference(self.start_free_gpus_set)
        have_new_free_gpus = len(new_free_gpus) > 0

        if have_new_free_gpus:
            if self.start_free_gpus_set:
                logger.info("Shutting down existing miner to restart")
                self.stop()
            self.start()
            return

        if not self.start_free_gpus_set:
            logger.info("No free GPUs. Waiting.")

    def start(self):
        self.start_free_gpus_set = set(ut.free_gpus_list())
        logger.info(f"Started mining. Using GPUs: {self.start_free_gpus_set}")
        stdout = None if self.cfg.debug else subprocess.DEVNULL
        self.miner_process = subprocess.Popen([ut.TREX_MINER_PATH, "-c", ut.TREX_MINER_CONFIG_PATH], stdout=stdout)
        sleep(self.cfg.sleep_time)  # extra time for startup

    def stop(self):
        if not self.working:
            return
        logger.info(f"Stopped mining on gpus: {self.start_free_gpus_set}")
        self.start_free_gpus_set = {}
        self.miner_process.terminate()
        self.miner_process = None
        sleep(self.cfg.sleep_time)  # make sure all processes stop

    @property
    def working(self):
        return self.miner_process is not None


@hydra.main(config_path="./configs/", config_name="config_pip.yaml")
def main(cfg: Config) -> None:
    # set unique name for each node
    cfg.miner.pools[0].user += f".{platform.node()}"
    # log current config
    logger.info(OmegaConf.to_yaml(cfg, resolve=True))

    # maybe download miner
    ut.get_trex_miner(update=cfg.update_miner)

    # hydra changes dir. need to undo this
    os.chdir(hydra.utils.get_original_cwd())

    # dump config to tmp. later this file would be mounted to docker
    ut.dump_trex_config(cfg.miner)

    miner = Miner(cfg)
    # wrap in try-except to handle Keyboard Interrupt and kill mining
    try:
        while True:
            miner.step()
            sleep(cfg.sleep_time)
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt. Stopping")
    finally:
        ut.stop_trex_miner()


if __name__ == "__main__":
    main()
