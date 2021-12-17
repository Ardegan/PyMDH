from sqlalchemy import Column, Integer, TIMESTAMP, func, JSON
from communication.comm_mon import MonPersistenceOrm


class Example(MonPersistenceOrm.Base):
    __tablename__ = 'example'

    # not needed as schema is specified already in engine, but will needs to be specified in case of working with more schemas:
    #__table_args__ = {"schema": "some_schema"}

    id = Column(Integer, primary_key=True)
    ins_time = Column(TIMESTAMP, server_default=func.now())
    rest_health = Column(Integer, comment='REST: actuator/health is (not) "UP" - 0/1')
    rmq_inc_cnt = Column(Integer, comment='RabbitMQ - messages count')
    rmq_inc_readout = Column(Integer, comment='RabbitMQ - messages queue readout status')
    db_example_wait = Column(Integer, comment='OracleDB - count of rows with some status for example waiting')
    db_example_errors = Column(Integer, comment='OracleDB - count of rows with some status for example error')
    db_example_json = Column(JSON, comment='OracleDB - several values, in form of json')
    db_example_count_status = Column(Integer, comment='Status - 0 / 1 if the count is or is not above limit')
