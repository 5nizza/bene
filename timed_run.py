import os
import re
import logging

from consts import TIMEOUT_RC
from structs import TimedRunParams
from structs import ToolRunParams
from utils import get_tmp_file_name, execute_shell, readfile
from config import RUN_SOLVER_EXEC


class RunStats:
    def __init__(self, cpu_time_sec:float=None,
                 wall_time_sec:float=None,
                 virt_mem_mb:int=None):
        self.cpu_time_sec = cpu_time_sec
        self.wall_time_sec = wall_time_sec
        self.virt_mem_mb = virt_mem_mb


def get_float(param_name, text):
    numbers = re.findall(param_name + '=([0-9]+\.?[0-9]*)',
                         text)
    assert len(numbers) == 1, numbers
    return float(numbers[0])


def parse_stats(stats_str) -> RunStats:
    stats = RunStats(cpu_time_sec=get_float('CPUTIME', stats_str),
                     wall_time_sec=get_float('WCTIME', stats_str),
                     virt_mem_mb=int(get_float('MAXVM', stats_str) / 1000))
    return stats


def get_tool_rc(exec_log_str) -> int:
    if 'Maximum wall clock time exceeded' in exec_log_str:
        return TIMEOUT_RC

    status = re.findall('Child status: (\d+)', exec_log_str)
    assert len(status) == 1, status  # TODO: replace ALL asserts in the async part by logging into the DB
    return int(status[0])


def main(timed_run_params:TimedRunParams, tool_run:ToolRunParams) -> (RunStats, int):
    # TODO: add memory limit

    logging.info('timed_run.main')

    stats_file_name = get_tmp_file_name()
    exec_log_file = get_tmp_file_name()

    rc, out, err = \
        execute_shell('{runsolver} -o {tool_log} -v {stats_file} -w {exec_log} -W {time_limit} '
                      '{tool_cmd}'
                      .format(runsolver=RUN_SOLVER_EXEC,
                              tool_log=tool_run.log_file,
                              stats_file=stats_file_name,
                              exec_log=exec_log_file,
                              time_limit=str(timed_run_params.time_limit_sec),
                              tool_cmd=tool_run.to_cmd_str()))

    logging.info(readfile(exec_log_file))

    # TODO: this should also be logged in the DB
    assert rc == 0, 'timed run failed: rc={rc}, \nout={out}, \nerr={err}'\
            .format(rc=str(rc), out=out, err=err)

    tool_rc = get_tool_rc(readfile(exec_log_file))
    stats = parse_stats(readfile(stats_file_name))

    os.remove(stats_file_name)
    os.remove(exec_log_file)

    return stats, tool_rc
