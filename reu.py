import argparse
import sys
import traceback
from logging import Logger

import datetime

import timed_run
from ansistrm import setup_logging
from data_extractor import extract_data
from data_record import Experiment
from data_uploader import upload_run
from tool_run_params import ToolRunParams


def main(exp_record:Experiment, tool_launch_data:ToolRunParams, db,
         tag, note,
         logger:Logger):
    run_stats, tool_rc = timed_run.main(exp_record.time_limit_sec, tool_launch_data, logger)
    run_record = extract_data(run_stats, tool_launch_data, tool_rc, logger)
    run_record.exp = exp_record
    run_record.note = note
    run_record.tag = tag
    upload_run(db, run_record, logger)


def set_exc_hook(logger:Logger):
    # uncaught exceptions get logged
    saved = sys.excepthook

    def log_exception(ty, value, tb):
        logger.fatal(''.join(traceback.format_exception(ty, value, tb)))
        saved(ty, value, traceback)

    sys.excepthook = log_exception


if __name__ == "__main__":
    # TODO: test with srun, create DB uploader

    # TODO: bad design for tool params? (provide template?)

    parser = argparse.ArgumentParser(description='REU: Run the tool - Extract the data - Upload to the DB.\n'
                                                 "Note on the DB: if a table named 'exp_name' already exists,\n"
                                                 "then I create table 'exp_name_i' with lowest natural number i\n"
                                                 "such that 'exp_name_i' is not in the DB.",
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--tool',        required=True, help='your tool executable')
    parser.add_argument('--tool_params', required=False, help='parameters for your tool (excl. input and output files)')
    parser.add_argument('--input_file',  required=True, help='input file to the tool')
    parser.add_argument('--output_file', required=True, help='output file for the tool')
    parser.add_argument('--exec_log',    required=True, help='file name to store my execution logs')
    parser.add_argument('--tool_log',    required=True, help="file name to store your tool' logs")
    parser.add_argument('--db',          required=True, help='authorisation args for the db')  # TODO
    parser.add_argument('--exp_name',    required=True, help="name the experiment run")
    parser.add_argument('--commit',      required=True, help='tool version')
    parser.add_argument('--time_limit_sec',  required=True, type=int)
    parser.add_argument('--memory_limit_mb', required=True, type=int)
    parser.add_argument('--hardware',    required=True)
    args = parser.parse_args()

    logger = setup_logging(filename=args.exec_log)

    logger.info(args)

    set_exc_hook(logger)

    exp = Experiment(args.exp_name,
                     datetime.datetime.now(),
                     args.tool,
                     args.tool_params,
                     args.commit,
                     args.time_limit_sec,
                     args.memory_limit_mb,
                     args.hardware,
                     None,
                     None)

    tool_launch_data = ToolRunParams(args.tool, args.tool_params, args.input_file, args.output_file, args.tool_log)

    exit(main(exp, tool_launch_data, args.db, None, None, logger))
