import sys
from time import sleep
from omegaconf import OmegaConf
from freezegun import freeze_time
from datetimerange import DateTimeRange


sys.path.append("src")
import utils


def test_str_to_weekday():
    assert utils.str_to_weekday("Mon") == 1
    assert utils.str_to_weekday("Sun") == 7


FROZEN_DATE = "2021-07-01"


@freeze_time(FROZEN_DATE)
def test_parse_time_range():
    # test parsing single range
    time_ranges = "00:00-23:59"
    parsed = utils.parse_time_range(time_ranges)
    expected_parsed = [DateTimeRange(f"{FROZEN_DATE} 00:00:00+0", f"{FROZEN_DATE} 23:59:00+0")]
    assert parsed == expected_parsed

    # test parsing multiple ranges
    time_ranges = "00:02-10:05,21:02-23:59"
    parsed = utils.parse_time_range(time_ranges)
    expected_parsed = [
        DateTimeRange(f"{FROZEN_DATE} 00:02:00+0", f"{FROZEN_DATE} 10:05:00+0"),
        DateTimeRange(f"{FROZEN_DATE} 21:02:00+0", f"{FROZEN_DATE} 23:59:00+0"),
    ]
    assert parsed == expected_parsed


@freeze_time("2021-07-01T23:59:59", tick=True, tz_offset=-3)
def test_is_in_timerange():
    scheduler = [["Thu", "00:00-23:59"], ["Fri", "00:00-23:59"]]
    assert utils.true_now().isoweekday() == utils.str_to_weekday("Thu")
    assert not utils.is_in_time_range(scheduler)

    sleep(1)  # wait for day change
    assert utils.true_now().isoweekday() == utils.str_to_weekday("Fri")
    assert utils.is_in_time_range(scheduler)


def test_dump_config():
    """check that dumping works and produces expected format for configs"""
    cfg = OmegaConf.create({"common": {"algo": "eth", "interval": 60}, "server": {"host": "some.host", "port": 42}})
    TEST_CFG_PATH = "/tmp/test_conf.txt"
    utils.dump_gminer_config(cfg, TEST_CFG_PATH)
    loaded_cfg = open(TEST_CFG_PATH).read().strip()
    expected_cfg = "[common]\nalgo=eth\ninterval=60\n[server]\nhost=some.host\nport=42"
    assert loaded_cfg == expected_cfg
