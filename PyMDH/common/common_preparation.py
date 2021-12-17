from communication.comm_mon import MonPersistenceOrm


def prepare4Run():

    #logger.info('preps')
    pass


def prepareAfterStart():

    # create all non-existing Mon DB tables (or some other assets) which do not exists yet.
    # Also small note: SQL Alchemy is unfortunatelly not able to modify already existing objects (altering tables etc...)
    MonPersistenceOrm.Base.metadata.create_all(MonPersistenceOrm.engine)

