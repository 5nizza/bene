import os
import re
from logging import Logger

from tool_run_params import ToolRunParams
from run_stats import RunStats
from utils import get_tmp_file_name, execute_shell, readfile
from config import RUN_SOLVER_EXEC


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
    status = re.findall('Child status: (\d+)', exec_log_str)
    assert len(status) == 1, status
    return int(status[0])


def main(time_limit_sec:int,
         tool_run:ToolRunParams,
         logger:Logger) -> (RunStats, int):

    stats_file_name = get_tmp_file_name()
    exec_log_file = get_tmp_file_name()

    rc, out, err = \
        execute_shell('{runsolver} -o {tool_log} -v {stats_file} -w {exec_log} -C {time_limit} '
                      '{tool_cmd}'
                      .format(runsolver=RUN_SOLVER_EXEC,
                              tool_log=tool_run.log_file,
                              stats_file=stats_file_name,
                              exec_log=exec_log_file,
                              time_limit=str(time_limit_sec),
                              tool_cmd=tool_run.to_cmd_str()))

    logger.info(readfile(exec_log_file))

    assert rc == 0, 'timed run failed: rc={rc}, \nout={out}, \nerr={err}'\
            .format(rc=str(rc), out=out, err=err)

    stats = parse_stats(readfile(stats_file_name))
    tool_rc = get_tool_rc(readfile(exec_log_file))

    os.remove(stats_file_name)
    os.remove(exec_log_file)

    return stats, tool_rc

