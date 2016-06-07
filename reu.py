import argparse
import sys
import traceback
import logging
import datetime
import timed_run

from ansistrm import setup_logging
from consts import REAL_RC, TIMEOUT_STR, TIMEOUT_RC, FAIL_STR
from consts import UNREAL_RC
from data_extractor import extract_data
from structs import ToolRunParams, ExpDesc, TimedRunParams, RunResult
from data_uploader import upload_run


def main(exp:ExpDesc, timed_run_params:TimedRunParams, tool_run_params:ToolRunParams):
    run_stats, tool_rc = timed_run.main(timed_run_params, tool_run_params)

    if tool_rc in (REAL_RC, UNREAL_RC):
        run_result = extract_data(tool_run_params.output_file,
                                  tool_run_params.log_file,
                                  tool_rc)
    elif tool_rc == TIMEOUT_RC:
        run_result = RunResult(None, None, None, TIMEOUT_STR, None)
    else:
        run_result = RunResult(None, None, None, FAIL_STR, None)

    run_result.total_time_sec = run_stats.wall_time_sec
    run_result.memory_mb = run_stats.virt_mem_mb
    upload_run(exp, timed_run_params, tool_run_params, run_result)


def set_exc_hook():
    """ uncaught exceptions get logged """
    saved = sys.excepthook

    def log_exception(ty, value, tb):
        logging.fatal(''.join(traceback.format_exception(ty, value, tb)))
        saved(ty, value, traceback)

    sys.excepthook = log_exception


if __name__ == "__main__":
    # TODO: bad design for tool params? (provide template?)

    parser = argparse.ArgumentParser(description='REU: Run the tool - Extract the data - Upload to the DB.\n'
                                                 "Note on the DB: if a table named 'exp_name' already exists,\n"
                                                 "then I create table 'exp_name_i' with lowest natural number i\n"
                                                 "such that 'exp_name_i' is not in the DB.",
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--tool',        required=True, help='your tool executable')
    parser.add_argument('--tool_params', required=False, help='parameters for your tool (excl. input and output files)')
    parser.add_argument('--input_file',  required=True, help='input file to the tool')
    parser.add_argument('--output_file', required=False, default=None, help='output file for the tool')
    parser.add_argument('--exec_log',    required=True, help='file name to store my execution logs')
    parser.add_argument('--tool_log',    required=True, help="file name to store your tool' logs")
    parser.add_argument('--exp_name',    required=True, help="name the experiment run")
    parser.add_argument('--commit',      required=True, help='tool version')
    parser.add_argument('--time_limit_sec',  required=True, type=int)
    parser.add_argument('--memory_limit_mb', required=True, type=int)
    parser.add_argument('--hardware',    required=True)
    args = parser.parse_args()

    setup_logging(filename=args.exec_log)

    logging.info(args)

    set_exc_hook()

    exp_desc = ExpDesc(args.exp_name, datetime.datetime.now(), args.commit, args.hardware, None)

    timed_run_params = TimedRunParams(args.time_limit_sec, args.memory_limit_mb)

    tool_run_params = ToolRunParams(args.tool, args.tool_params,
                                    args.input_file, args.output_file,
                                    args.tool_log)

    exit(main(exp_desc, timed_run_params, tool_run_params))
