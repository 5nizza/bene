import os
import re
from logging import Logger

from data_record import RunRecord
from run_stats import RunStats
from tool_run_params import ToolRunParams
from utils import readfile


REAL_RC = 10


def parse_demiurge_logs(tool_log) -> (float, float):
    """
    :returns: win_region_time_sec, circuit_extr_sec
    """

    win_region_cpu = re.findall('Winning region computation time: ([0-9]+[\.]?[0-9]*) sec CPU time',
                                tool_log)
    assert len(win_region_cpu) == 1, win_region_cpu

    circuit_extr_cpu = re.findall('Relation determinization time: ([0-9]+[\.]?[0-9]*) sec CPU time',
                                  tool_log)
    assert len(circuit_extr_cpu) == 1, circuit_extr_cpu

    circuit_size = re.findall('Final circuit size: +([0-9]+)', tool_log)
    # assert len(circuit_size) == 1, circuit_size   # demiurge prints this message twice for some reason

    return float(win_region_cpu[0]),\
           float(circuit_extr_cpu[0]),\
           int(circuit_size[0])


def extract_data(run_stats:RunStats,
                 tool_launch_data:ToolRunParams,
                 tool_rc,
                 logger:Logger) -> RunRecord:
    """
    reu.py calls this function filling the parameters.
    This function is tool dependent, thus You need to implement it.
    """
    is_realizable = tool_rc == REAL_RC
    win_region_cpu, circuit_extr_cpu, circuit_size = parse_demiurge_logs(readfile(tool_launch_data.log_file)) \
                                                     if is_realizable else (None, None, None)

    return RunRecord(None,
                     tool_launch_data.input_file,
                     run_stats.cpu_time_sec,
                     win_region_cpu,
                     circuit_extr_cpu,
                     circuit_size,
                     run_stats.virt_mem_mb,
                     is_realizable,
                     readfile(tool_launch_data.output_file) if is_realizable else None,
                     readfile(tool_launch_data.log_file) if os.path.exists(tool_launch_data.log_file) else None,
                     None,
                     None)
