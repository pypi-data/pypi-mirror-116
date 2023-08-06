"""
This file is intended to run on machines were no safety precautions are needed
It doesn't hide itself and allows easy pause/un-pause for miner
"""
from logging import log
import os
import shlex
import hydra
import platform
import subprocess
from time import sleep
from loguru import logger
from omegaconf import OmegaConf

import idlem.utils as ut
from idlem.arg_parser import BaseConfig


def start_miner(miner_path: str) -> int:
    """Start miner and return it's pid. This function launces a separate child process and runs miner inside it.
    This complication is needed to bypass GMiner anti-hacking system. Simplier approaches don't work"""
    command_line = f"""
    python3 -c "import subprocess; p = subprocess.Popen(['{miner_path}', '--config', '{ut.MINER_CONFIG_PATH}'], stdout=subprocess.DEVNULL); print(p.pid)"
    """
    command_args = shlex.split(command_line)
    process = subprocess.Popen(command_args, stdout=subprocess.PIPE)
    pid = int(process.stdout.read().decode("utf-8"))
    logger.info(f"Process pid: {pid}")
    return pid


def kill_miner(miner_pid: int) -> None:
    if miner_pid is not None:
        logger.info(f"Killing miner. PID: {miner_pid}")
        os.kill(miner_pid, 15)  # 15 - SIGTERM
    return None  # explicitly return None


@hydra.main(config_path="./configs/", config_name="config_pip.yaml")
def main(cfg: BaseConfig) -> None:
    # set unique name for each node
    cfg.miner.server.user += f".{platform.node()}"
    # log current config
    logger.info(OmegaConf.to_yaml(cfg, resolve=True))

    # maybe download miner
    miner_path = ut.get_gminer()

    # hydra changes dir. need to undo this
    os.chdir(hydra.utils.get_original_cwd())

    # dump config to tmp. later this file would be mounted to docker
    ut.dump_gminer_config(cfg.miner, ut.MINER_CONFIG_PATH)

    miner_pid = None
    # wrap in try-except to handle Keyboard Interrupt and kill mining
    try:
        while True:
            # put sleep to the top to avoid adding it in every branch
            sleep(cfg.sleep_time)

            if ut.is_on_pause():
                logger.info("On pause")
                miner_pid = kill_miner(miner_pid)
                continue

            if miner_pid is None:
                logger.info("Starting miner")
                miner_pid = start_miner(miner_path)
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt. Stopping")
    finally:
        kill_miner(miner_pid)


if __name__ == "__main__":
    main()
