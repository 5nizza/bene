#!/usr/bin/env python3

import argparse
import os
import stat

CONFIG_PY_NAME = 'config.py'

CONFIG_PY_TEXT = """
RUN_SOLVER_EXEC = '/home/ayrat/projects/runsolver/src/runsolver'
DB_HOST = 'host'
DB_USER = 'user'
DB_PASSWD = 'user password'
DB_DBNAME = 'database name'
"""


def _get_root_dir():
    return os.path.dirname(os.path.abspath(__file__))


def _user_confirmed(question):
    answer = input(question + ' [y/n] ').strip()
    assert answer in 'yYnN', answer
    return answer in 'yY'


def main():
    config_py = os.path.join(_get_root_dir(), CONFIG_PY_NAME)
    existing = os.path.exists(CONFIG_PY_NAME)
    if not existing or \
            _user_confirmed('{files} already exist(s).\n'.format(files=existing) +
                            'Replace?'):
        with open(config_py, 'w') as file:
            file.write(CONFIG_PY_TEXT)
        print('Created {file}.\n'
              'Now edit them with your paths.'.
              format(file=CONFIG_PY_NAME))

        return True

    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=
                                     'Generate local configuration file')

    args = parser.parse_args()
    res = main()
    print(['not done', 'done'][res])
    exit(res)
