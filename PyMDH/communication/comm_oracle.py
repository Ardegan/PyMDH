import sqlalchemy
from config import settings
from sanic.log import logger, error_logger
from sqlalchemy.pool import NullPool


class OraclePersistenceRaw:
    """
    Author: Lukas Fojtik, created on: 10.12.2019
    Class for communication with ORA DB
    To keep it simple and save, it uses just raw connector
    """

    def __init__(self):
        """
        poolclass=NullPool => disable pooling, i.e. after disposing of engine or closing ORM sqlalchemy session(), the DBAPI connection closes as well.
            Using only "RAW" core sqlalchemy without ORM Abstraction cause DBAPI conn close anyway but just to be sure..
        echo=True => print literal representation of final sql query to stdout
        """
        self.engine = sqlalchemy.create_engine(settings.ORACLE_DB_URL, poolclass=NullPool)#, echo=True)

    def __enter__(self):
        try:
            self.conn = self.engine.connect()
        except sqlalchemy.exc.DatabaseError as err:
            error_logger.error("Ora DB ERROR: %s %s" % (type(err), err))
        return self

    def __exit__(self, *args):
        self.conn.close()
        self.engine.dispose()

    def fetchOne(self, select):
        """
        :param select: str - explicit sql select statement string which should return one row
        :return: list - result from ORA DB
        """
        logger.debug('Selecting from OracleDB: '+select)

        row = None

        try:
            cursor = self.conn.execute(select)
            row = cursor.fetchone()
            cursor.close()
        except sqlalchemy.exc.DatabaseError as err:
            error_logger.error("Ora ERROR: %s %s" % (type(err), err))
        return row

    def fetchAll(self, select):

        logger.debug('Selecting from OracleDB: '+select)

        row = None

        try:
            cursor = self.conn.execute(select)
            row = cursor.fetchall()
            cursor.close()
        except sqlalchemy.exc.DatabaseError as err:
            error_logger.error("Ora ERROR: %s %s" % (type(err), err))
        return row


