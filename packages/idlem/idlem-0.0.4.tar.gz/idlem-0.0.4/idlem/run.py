"""
This file is intended to run on machines were no safety precautions are needed
It doesn't hide itself and allows easy pause/un-pause for miner
"""
from logging import log
import os
import hydra
import platform
import subprocess
from time import sleep
from loguru import logger
from omegaconf import OmegaConf

import idlem.utils as ut
from idlem.arg_parser import BaseConfig

def start_miner(debug: bool=False):
    subprocess.Popen([ut.TREX_MINER_PATH, '-c', ut.TREX_MINER_CONFIG_PATH], stdout=None if debug else subprocess.DEVNULL)

@hydra.main(config_path="./configs/", config_name="config_pip.yaml")
def main(cfg: BaseConfig) -> None:
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

    # wrap in try-except to handle Keyboard Interrupt and kill mining
    try:
        while True:
            # put sleep to the top to avoid adding it in every branch
            sleep(cfg.sleep_time)

            if ut.is_on_pause():
                logger.info("On pause")
                ut.stop_trex_miner() # will check existence inside
                continue
                
            # start if not already running
            if not ut.get_trex_processes():
                logger.info("Starting miner")
                start_miner(debug=cfg.debug)
            
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt. Stopping")
    finally:
        ut.stop_trex_miner()


if __name__ == "__main__":
    main()
