#!/usr/bin/python3
import argparse

from utils import execute_shell, readfile

REU_CMD = ''   # Run the tool - Extract the data - Upload to the DB
SPAWN_JOB_CMD = 'srun'


def main(tool_cmd:str, tool_params:str, benchmarks_list:list, logs_dir:str, db:str):
    for input_file in benchmarks_list:
        execute_shell('{spawn_job} {REU} {tool_cmd} {tool_params} {input_file} {logs_dir} {db}'
                      .format(REU=REU_CMD,
                              spawn_job=SPAWN_JOB_CMD,
                              tool_cmd=tool_cmd,
                              tool_params=tool_params,
                              input_file=input_file,
                              logs_dir=logs_dir,
                              db=db))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Hi, I am Bene, I run your tool, extract data, and fill DB:\n'
                                                 'for input_file in <benchmarks_list>:\n'
                                                 '  spawn_job timed_run <tool> <tool_params> input_file -o output_file\n'
                                                 '  data = <extract_data>(<logs_dir>, input_file)\n'
                                                 '  fill(data, <db>).\n'
                                                 'I will use <logs_dir> for output files and logs.',
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--tool', required=True, help='your tool executable')
    parser.add_argument('--tool_params', required=True, help='parameters for your tool')
    parser.add_argument('--benchmarks_list', required=True, type=argparse.FileType(),
                        help='file containing a list of benchmarks (one filepath per line)')
    parser.add_argument('--logs_dir', required=True, type=argparse.FileType(), help='directory for log files')
    parser.add_argument('--db', required=True, type=argparse.FileType(), help='database file')

    args = parser.parse_args()

    benchmarks = [b for b in args.benchmarks_list.readlines()
                  if b.strip()]

    print(args)
    exit(main(args.tool,
              args.tool_params,
              benchmarks,
              args.logs_dir,
              args.db))
