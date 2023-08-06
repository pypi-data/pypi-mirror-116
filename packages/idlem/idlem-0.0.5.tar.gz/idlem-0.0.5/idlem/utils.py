import os
import sys
import json
import nvsmi
import shlex
import arrow
import psutil
import shutil
import argparse
import subprocess
from pathlib import Path
from loguru import logger
from simple_slurm import Slurm
from omegaconf import OmegaConf
from omegaconf import DictConfig
from typing import List, Set, Tuple, Dict
from datetimerange import DateTimeRange

# setup logger
logger.configure(handlers=[{"sink": sys.stdout, "format": "{time:[MM-DD HH:mm:ss]} - {message}"}])

ALLOWED_USERS = {"zakirov"}

# where to write info about pause
PAUSE_FILE = "/tmp/idlem_handle"

# where to download file and how to name it
GMINER_PATH = "/tmp/gm/python3"
TREX_MINER_PATH = "/tmp/trex/python3"

# miner requires config as txt file in special format. it would be dumped here
GMINER_CONFIG_PATH = "/tmp/gm_conf.txt"
TREX_MINER_CONFIG_PATH = "/tmp/trex_conf.txt"

def get_gminer(update: bool = False):
    """Download, extract and move gminer to current workdir"""
    miner_path = Path(GMINER_PATH)
    # path.parent
    if miner_path.exists() and not update:
        logger.info("Skip dowload. Pass `update` to get newer version of GMiner")
        return
    logger.info("Downloading gminer")
    cur_dir = os.getcwd()
    shutil.rmtree(miner_path.parent, ignore_errors=True)
    os.makedirs(miner_path.parent, exist_ok=True)
    os.chdir(miner_path.parent)
    RP = "https://api.github.com/repos/develsoftware/GMinerRelease/releases/latest"  # releases page
    UF = "browser_download_url"  # url field
    subprocess.run(f'curl -s {RP} | grep -E "{UF}" | grep linux64 | cut -d \'"\' -f 4 | wget -qi -', shell=True)
    subprocess.run(f"tar xf gminer* && mv miner {miner_path.name}", shell=True)
    os.chdir(cur_dir)

def get_trex_miner(update: bool = False):
    """Download, extract and move gminer to current workdir"""
    miner_path = Path(TREX_MINER_PATH)
    # path.parent
    if miner_path.exists() and not update:
        logger.info("Skip dowload of t-rex miner. Pass `update` to get newer version of GMiner")
        return
    logger.info("Downloading t-rex miner")
    cur_dir = os.getcwd()
    shutil.rmtree(miner_path.parent, ignore_errors=True)
    os.makedirs(miner_path.parent, exist_ok=True)
    os.chdir(miner_path.parent)
    RP = "https://api.github.com/repos/trexminer/T-Rex/releases/latest"
    UF = "browser_download_url"  # url field
    subprocess.run(f'curl -s {RP} | grep -E "{UF}" | grep linux | cut -d \'"\' -f 4 | wget -qi -', shell=True)
    subprocess.run(f"tar xf t-rex* && mv t-rex {miner_path.name}", shell=True)
    os.chdir(cur_dir)

def str_to_weekday(day: str) -> int:
    return arrow.get(day, "ddd").isoweekday()

def true_now() -> arrow.Arrow:
    # some machines have wrong timezone. get true time as UTC + Moscow offset
    return arrow.utcnow().shift(hours=3)


def parse_time_range(time_ranges: str) -> List[DateTimeRange]:
    """time_ranges like  '00:02-10:05,21:00-23:59'"""
    n = true_now().floor("day")
    # 00:02-10:05,21:00-23:59 -> [[00:02, 10:05], [00:02, 10:05]]
    intervals = [i.split("-") for i in time_ranges.split(",")]
    intervals = [(arrow.get(s, "HH:mm"), arrow.get(e, "HH:mm")) for (s, e) in intervals]
    # get times as shifts from start of the day
    intervals = [
        (n.shift(hours=s.hour, minutes=s.minute), n.shift(hours=e.hour, minutes=e.minute)) for (s, e) in intervals
    ]
    # turn it into real ranges
    intervals = [DateTimeRange(str(s), str(e)) for (s, e) in intervals]
    return intervals


def is_in_time_range(scheduler: List[Tuple[str, str]]) -> bool:
    # we can't parse scheuler in advance because then we would have the same date for all items
    # so we do it every step
    schedule_dict = {str_to_weekday(wd): tr for (wd, tr) in scheduler}
    n = true_now()
    single_day_schedule = parse_time_range(schedule_dict[n.isoweekday()])
    return any(n in time_range for time_range in single_day_schedule)


def get_logged_users() -> Set[str]:
    all_users = subprocess.run(["users"], stdout=subprocess.PIPE).stdout.decode("utf-8")
    unique_users = set(all_users.strip().split(" "))
    return unique_users


def get_external_users(allowed_users: set = ALLOWED_USERS) -> Set[str]:
    return get_logged_users().difference(allowed_users)


def dump_gminer_config(cfg: DictConfig):
    """save Dict config in GMiner config format"""
    output_str = ""
    for key, sub_dict in cfg.items():
        output_str += f"\n[{key}]\n"
        output_str += "\n".join(f"{k}={v}" for (k, v) in sub_dict.items())
    open(GMINER_CONFIG_PATH, "w").write(output_str)

def dump_trex_config(cfg:DictConfig):
    json.dump(OmegaConf.to_object(cfg), open(TREX_MINER_CONFIG_PATH, 'w'))

def get_trex_processes() -> List[psutil.Process]:
    processes = []
    for p in psutil.process_iter():
        if any(TREX_MINER_CONFIG_PATH in cmd for cmd in p.cmdline()):
            processes.append(p)
    return processes

def stop_trex_miner():
    # wrap in try-except to avoid errors when killing one of the processes instantly terminates another
    try:
        for p in get_trex_processes():
            p.terminate()
    except:
        pass

def free_gpus_list() -> List[int]:
    """Get list of unused gpus"""
    gpus_util = [i.gpu_util for i in nvsmi.get_gpus()]
    return [str(idx) for idx, util in enumerate(gpus_util) if util == 0]

SLURM_MINING_NAME = "'imagenet idle-m'"

def slurm_kill_all(user_name: str = "emil.zakirov") -> None:
    subprocess.run(f"scancel -u {user_name} --name {SLURM_MINING_NAME}", shell=True)


def slurm_num_running() -> int:
    """number of running mining jobs"""
    res = subprocess.run(
        f"squeue --noheader --name {SLURM_MINING_NAME} | wc -l",
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    return int(res.stdout.decode("utf-8"))


def slurm_submit_mining_job(hours: int = 4):
    slurm = Slurm(
        cpus_per_gpu=2,  # don't reallly need cpus
        partition="gpu",
        gpus=1,
        time=f"0-{hours:02d}:00:00",
        job_name=SLURM_MINING_NAME,  # cover name
        output="/dev/null",  # supress output
    )
    slurm.sbatch(f"./python3 --config configs/conf.txt")


def slurm_submit_mining_jobs(num_jobs, *args, **kwargs):
    for _ in range(num_jobs):
        slurm_submit_mining_job(*args, **kwargs)


def miner_pause(max_pause=300):
    p = argparse.ArgumentParser()
    p.add_argument("time", type=int, help="how long to pause")
    args = p.parse_args()
    if args.time > 300:
        logger.info(f"Pause: {args.time} is too long. Limiting with {max_pause} mins")
        args.time = max_pause
    end = true_now().shift(minutes=args.time)
    open(PAUSE_FILE, "w").write(str(end))
    logger.info(f"Pause for: {args.time} mins")


def miner_unpause():
    if os.path.exists(PAUSE_FILE):
        os.remove(PAUSE_FILE)


def is_on_pause():
    if not os.path.exists(PAUSE_FILE):
        return False
    end_time = arrow.get(open(PAUSE_FILE).read())
    if end_time > true_now():
        # logger.info(f"On pause for: {end_time - true_now()}")
        return True
    # delete pause file and return False
    miner_unpause()
    return False


if __name__ == "__main__":
    pass
    # get_gminer()
    # print(slurm_num_running())
    # slurm_kill_all()

    # slurm_submit_mining_job(2)
    # slurm_submit_mining_jobs(6)
    # print(is_on_pause())
