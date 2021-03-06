import logging

from typing import Iterable

from adhoc_fields import adhoc_fields
from field_desc import FieldDesc
from structs import ExpDesc, TimedRunParams, ToolRunParams, RunResult
from peewee import *

from config import DB_HOST, DB_USER, DB_PASSWD, DB_DBNAME
from utils import readfile


# taken from:
# http://peewee.readthedocs.org/en/latest/peewee/example.html#example-app

database = MySQLDatabase(host=DB_HOST,
                         user=DB_USER,
                         passwd=DB_PASSWD,
                         database=DB_DBNAME)

# database = SqliteDatabase('tests.db')


class BaseModel(Model):  # BaseModel is only used to specify the database
    class Meta:
        database = database


class RunRecord(BaseModel):
    """ Note: see the end of this module -- this class is updated with fields from adhoc_fields """
    total_time_sec = FloatField(null=True)
    circuit_size = IntegerField(null=True)
    memory_mb = FloatField(null=True)
    is_realizable = CharField()
    model = TextField(null=True)

    input_file = CharField()
    logs = TextField(null=True)
    tool_params = CharField()

    exp = CharField()
    commit = CharField(null=True)
    hardware = CharField(null=True)
    datetime = DateTimeField(null=True)
    note = CharField(null=True)

    time_limit_sec = FloatField(null=True)
    memory_limit_mb = FloatField(null=True)

    def __init__(self,
                 exp_desc:ExpDesc,
                 timed_run_params:TimedRunParams, tool_run_params:ToolRunParams,
                 run_result:RunResult,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.total_time_sec = run_result.total_time_sec
        self.circuit_size = run_result.circuit_size
        self.memory_mb = run_result.memory_mb
        self.is_realizable = run_result.is_realizable
        self.model = run_result.model

        self.input_file = tool_run_params.input_file
        self.logs = readfile(tool_run_params.log_file) if tool_run_params.log_file else ''
        self.tool_params = tool_run_params.params

        self.exp = exp_desc.exp_name
        self.commit = exp_desc.commit
        self.hardware = exp_desc.hardware
        self.datetime = exp_desc.datetime
        self.note = exp_desc.note

        self.time_limit_sec = timed_run_params.time_limit_sec
        self.memory_limit_mb = timed_run_params.memory_limit_mb


def __add_static_fields_RunRecord(adhoc_fields_:Iterable[FieldDesc]):
    for f_desc in adhoc_fields_:
        f_desc.db_field.add_to_class(RunRecord, f_desc.name)


def __add_object_fields_RunRecord(rr:RunRecord, adhoc_data:dict):
    """ :arg adhoc_data: dict{field_name -> field python value}"""
    for name, value in adhoc_data.items():
        setattr(rr, name, value)


def upload_run(exp_desc:ExpDesc,
               timed_run_params:TimedRunParams,
               tool_run_params:ToolRunParams,
               run_result:RunResult,
               adhoc_data:dict):
    logging.info('data_uploader.upload_record')
    logging.debug('run_result=' + str(run_result))
    RunRecord._meta.db_table = exp_desc.exp_name
    with database.transaction():
        rr = RunRecord(exp_desc, timed_run_params, tool_run_params, run_result)
        __add_object_fields_RunRecord(rr, adhoc_data)
        rr.save()


def create_table(table_name):
    """ Fails if table 'table_name' already exists. """
    logging.info('create_table: ' + table_name)
    RunRecord._meta.db_table = table_name   # TODO: not clear: should you restore the old name?
    database.connect()
    database.create_table(RunRecord)
    database.close()


def table_exists(table_name):
    old_name = RunRecord._meta.db_table
    RunRecord._meta.db_table = table_name
    result = RunRecord.table_exists()
    RunRecord._meta.db_table = old_name
    return result


__add_static_fields_RunRecord(adhoc_fields)
