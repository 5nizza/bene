#!/usr/bin/python3
import argparse
import os

from utils import execute_shell

SPAWN_JOB_CMD = 'srun'


def main(tool_cmd:str, tool_params:str,
         benchmarks_list:list,
         logs_dir:str,
         db:str,
         exp_name,
         commit,
         time_limit_sec,
         memory_limit_mb,
         hardware):
    os.makedirs(logs_dir, exist_ok=True)
    for input_file in benchmarks_list:
        print('starting a job for ', input_file)
        input_basename = os.path.basename(input_file)
        execute_shell('{spawn_job} '
                      'python3 {REU} '
                      '--tool {tool_cmd} --tool_params {tool_params} '
                      '--input_file {input_file} --output_file {output_file} '
                      '--exec_log {exec_log} --tool_log {tool_log} '
                      '--db {db} '
                      '--exp_name {exp_name} --commit {commit} '
                      '--time_limit_sec {time_limit_sec} --memory_limit_mb {memory_limit_mb} '
                      '--hardware {hardware}'
                      .format(spawn_job=SPAWN_JOB_CMD,
                              REU='reu.py',
                              tool_cmd=tool_cmd,
                              tool_params=tool_params,
                              input_file=input_file,
                              output_file=logs_dir + '/' + input_basename + '.model',
                              exec_log=logs_dir + '/' + input_basename + '.exec.log',
                              tool_log=logs_dir + '/' + input_basename + '.tool.log',
                              db=db,
                              exp_name=exp_name,
                              commit=commit,
                              time_limit_sec=time_limit_sec,
                              memory_limit_mb=memory_limit_mb,
                              hardware=hardware
                              ))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Hi, I am Bene, I run your tool, extract data, and fill DB:\n'
                                                 '  for input_file in <benchmarks_list>:\n'
                                                 '    spawn_job timed_run <tool> <tool_params> input_file -o output_file\n'
                                                 '    data = <extract_data>(<logs_dir>, input_file)\n'
                                                 '    fill(data, <db>).\n'
                                                 'I will use <logs_dir> for output files and logs.',
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--tool', required=True, help='your tool executable')
    parser.add_argument('--tool_params', required=True, help='parameters for your tool')
    parser.add_argument('--benchmarks_list', required=True, type=argparse.FileType(),
                        help='file containing a list of benchmarks (one filepath per line)')
    parser.add_argument('--logs_dir', required=True, type=str,
                        help='directory for log files (will be created if does not exists)')
    parser.add_argument('--db', required=True, help='database credentials (TODO)')
    parser.add_argument('--exp_name', required=True, help='name your experiment')
    parser.add_argument('--commit', required=True, help='version of the tool')
    parser.add_argument('--time_limit_sec', required=False, default=10, type=int, help='(default: %(default)i)')
    parser.add_argument('--memory_limit_mb', required=False, default=10000, type=int, help='(default: %(default)i)')
    parser.add_argument('--hardware', required=True, help='hardware on which you run')
    # TODO: default logs folder created from exp_name + salt?
    # TODO: default commit?

    args = parser.parse_args()

    benchmarks = [b for b in args.benchmarks_list.readlines()
                  if b.strip()]

    print(args)
    exit(main(args.tool, args.tool_params,
              benchmarks,
              args.logs_dir,
              args.db,
              args.exp_name,
              args.commit,
              args.time_limit_sec, args.memory_limit_mb,
              args.hardware))
