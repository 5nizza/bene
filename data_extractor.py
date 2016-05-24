import re
import logging

from consts import REAL_RC, UNREAL_RC, TIMEOUT_RC
from structs import RunResult
from utils import readfile


def parse_tool_logs(tool_log) -> (float, float, int):
    """
    :returns: win_region_time_sec, circuit_extr_sec
    """

    win_region_cpu = re.findall('calc_win_region took \(sec\): ([0-9]+)',
                                tool_log)
    assert len(win_region_cpu) == 1, win_region_cpu

    circuit_extr_cpu = re.findall('extract_output_funcs took \(sec\): ([0-9]+)',
                                  tool_log)
    assert len(circuit_extr_cpu) == 1, circuit_extr_cpu

    circuit_size = re.findall('circuit size: ([0-9]+)', tool_log)
    # assert len(circuit_size) == 1, circuit_size   # demiurge prints this message twice for some reason

    return float(win_region_cpu[0]),\
           float(circuit_extr_cpu[0]),\
           int(circuit_size[0])


def extract_data(tool_output_file,
                 tool_log_file,
                 tool_rc) -> RunResult:
    """
    reu.py calls this function filling the parameters.
    This function is tool dependent, thus You need to implement it.
    """
    logging.info('data_extractor.extract_data')

    assert tool_rc in (REAL_RC, UNREAL_RC, TIMEOUT_RC), tool_rc
    is_realizable = {REAL_RC:'REAL',
                     UNREAL_RC:'UNREAL',
                     TIMEOUT_RC:'TIMEOUT'}[tool_rc]

    win_region_cpu, circuit_extr_cpu, circuit_size = parse_tool_logs(readfile(tool_log_file)) \
                                                     if is_realizable else (None, None, None)

    return RunResult(None,
                     win_region_cpu,
                     circuit_extr_cpu,
                     circuit_size,
                     None,
                     is_realizable,
                     readfile(tool_output_file) if is_realizable else None)
