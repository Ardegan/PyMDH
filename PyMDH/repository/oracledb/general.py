import asyncio

from common.common_tools import GlobalVars
from communication.comm_oracle import OraclePersistenceRaw
from sanic.log import logger, error_logger


async def getOracleDbResult(input, fetchType ='fetchOne'):
    '''
    Author: Lukas Fojtik, 21.1.2020
    :param fetchType:
    :param input: string or dictionary ( OracleDB select(s) )
    :return: either string or dictionary based on type of input variable
    '''

    def fetchOracleDbResultString():
        with OraclePersistenceRaw() as conn:
            return conn.fetchOne(input)[0]

    def fetchOracleDbResultsDict():
        dictResult = {}
        with OraclePersistenceRaw() as conn:
            for k, v in input.items():
                if isinstance(k, str):
                    result = conn.fetchOne(v)[0]
                    dictResult[k] = result
                if isinstance(k, tuple):
                    result = conn.fetchOne(v)
                    dictResult.update(dict(zip(k, result)))
        return dictResult

    def fetchOracleDbResultsDictAll():
        dictResult = {}
        with OraclePersistenceRaw() as conn:
            for k, v in input.items():
                result = conn.fetchAll(v)
                dictResult[k] = result
        return dictResult

    if fetchType == 'fetchOne':
    # check whether "input" parameter is str or dict and based on that run appropriate function
        if isinstance(input, str):
            func2run = fetchOracleDbResultString
        elif isinstance(input, dict):
            func2run = fetchOracleDbResultsDict
    elif fetchType == 'fetchAll':
        func2run = fetchOracleDbResultsDictAll
    else:
        logger.warning('Unsupported input type for sql statement on OracleDB: ' + str(type(input)))
        func2run = None


    # Note: asyncio library in python 3.5+ always returns proper event loop by get_event_loop() so no need to globalise one
    loop = asyncio.get_event_loop()
    executor = GlobalVars.getThreadPoolExecutor()

    try:
        result = await loop.run_in_executor(executor, func2run)
    except TypeError as err:
        error_logger.exception("Error during fetching OracleDB result: %s %s" % (type(err), err))
        result = {}

    return result


def getFromOra(datetime, pandaMod):

    dictPandaMode2Ora = {
        'min' : '1/24/60',
        '5min' : '5/24/60',
        '10min' : '10/24/60',
        'h' : '1/24',
        'd' : '1'
    }

    fromString = f'''to_date('{datetime}','yyyy-mm-dd hh24:mi:ss') - {dictPandaMode2Ora.get(pandaMod)}'''
    return fromString

def getToOra(datetime):
    toString = f'''to_date('{datetime}','yyyy-mm-dd hh24:mi:ss')'''
    return toString

