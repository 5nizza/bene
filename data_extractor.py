import re
import logging

from consts import REAL_RC, UNREAL_RC, TIMEOUT_RC
from structs import RunResult
from utils import readfile


def extract_data(tool_output_file,
                 tool_log_file,
                 tool_rc) -> RunResult:
    """
    reu.py calls this function filling the parameters.
    This function is tool dependent, thus You need to implement it.
    """
    logging.info('data_extractor.extract_data')

    assert tool_rc in (REAL_RC, UNREAL_RC), tool_rc

    tool_log_str = readfile(tool_log_file)

    return RunResult(None,
                     int(re.findall('calc_win_region took \(sec\): ([0-9]+)', tool_log_str)[0]),
                     int(re.findall('extract_output_funcs took \(sec\): ([0-9]+)', tool_log_str)[0])
                         if tool_rc == REAL_RC else None,
                     int(re.findall('circuit size: ([0-9]+)', tool_log_str)[0])
                         if tool_rc == REAL_RC else None,
                     None,
                     {REAL_RC:'REAL', UNREAL_RC:'UNREAL'}[tool_rc],
                     readfile(tool_output_file) if tool_rc == REAL_RC and tool_output_file else None,
                     int(re.findall('calc_trans_rel took \(sec\): ([0-9]+)', tool_log_str)[0]),
                     # re.findall('order_after_trans_rel: (.+$)', tool_log_str, flags=re.M)[0],
                     None,
                     # re.findall('order_after_win_region: (.+$)', tool_log_str, flags=re.M)[0],
                     None,
                     None)
                     # re.findall('order_after_circuit_extraction: (.+$)', tool_log_str, flags=re.M)[0]
                     #     if tool_rc == REAL_RC else None)
