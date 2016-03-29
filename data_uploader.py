from logging import Logger

from data_record import RunRecord


def upload_record(db, data_record:RunRecord, logger:Logger):
    logger.warning('upload_record: implement me')
    print(data_record)
