from logging import Logger
from data_record import Run
from peewee import *

from config import DB_HOST, DB_USER, DB_PASSWD, DB_DBNAME


# taken from:
# http://peewee.readthedocs.org/en/latest/peewee/example.html#example-app

database = MySQLDatabase(host=DB_HOST,
                         user=DB_USER,
                         passwd=DB_PASSWD,
                         database=DB_DBNAME)


class BaseModel(Model):  # BaseModel is only used to specify the database
    class Meta:
        database = database


class ExperimentRecord(BaseModel):
    name = CharField()
    date = DateTimeField()
    tool_cmd = CharField()
    tool_params = CharField()
    commit = CharField()
    time_limit_sec = IntegerField()
    memory_limit_mb = IntegerField()
    hardware = CharField()
    note = CharField()
    tag = CharField()


class RunRecord(BaseModel):
    exp = ForeignKeyField(ExperimentRecord, related_name='runs')
    filename = CharField()
    total_time_sec = IntegerField()
    time_win_region_sec = IntegerField()
    time_extraction_sec = IntegerField()
    circuit_size = IntegerField()
    memory_mb = IntegerField()
    is_realizable = BooleanField()
    model = TextField()
    logs = TextField()
    note = CharField()
    tag = CharField()

    def __init__(self, run:Run, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exp = run.exp
        self.filename = run.filename
        self.total_time_sec = run.total_time_sec
        self.time_extraction_sec = run.time_extraction_sec
        self.circuit_size = run.circuit_size
        self.memory_mb = run.memory_mb
        self.is_realizable = run.is_realizable
        self.model = run.model
        self.logs = run.logs
        self.tag = run.tag


def upload_run(db, run:Run, logger:Logger):
    logger.info('data_uploader.upload_record')
    with database.transaction():
        rr = RunRecord(run)
        rr.save()


def create_tables():
    database.connect()
    print('connected')
    database.create_tables([ExperimentRecord, RunRecord], True)  # True: check if they exist
    database.close()

create_tables()
