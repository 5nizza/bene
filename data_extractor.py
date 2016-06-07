import logging
import re

from consts import REAL_RC, UNREAL_RC
from structs import RunResult


def extract_data(tool_output_model_str: str or None,
                 tool_log_str:str,
                 tool_rc) -> RunResult:
    """
    reu.py calls this function filling the parameters.
    This function is tool dependent, thus You need to implement it.
    """
    logging.info('data_extractor.extract_data')

    assert tool_rc in (REAL_RC, UNREAL_RC), tool_rc

    return RunResult(None,
                     int(re.findall('circuit size: ([0-9]+)', tool_log_str)[0])
                         if tool_rc == REAL_RC else None,
                     None,
                     {REAL_RC:'REAL', UNREAL_RC:'UNREAL'}[tool_rc],
                     tool_output_model_str)
