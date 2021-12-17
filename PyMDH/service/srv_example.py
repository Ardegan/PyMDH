import asyncio
from datetime import datetime, time

from sanic.log import logger
from common.common_tools import TimeTools
from communication.comm_mon import MonPersistenceOrm
from model.mdl_example import Example
from repository.oracledb.repo_example import ExampleOracleRepo
from repository.rabbit.repo_example import ExampleRabbitRepo


async def getResults(inputTime):
    """
    Author: Lukas Fojtik, Created: 10.3.2020
    """

    listCorros = [ExampleRabbitRepo.getResult(), ExampleOracleRepo.getResult(inputTime)]

    if not TimeTools.isNowEndOfMonthRange(3) and time(4, 0) <= datetime.now().time() <= time(18, 0):
        listCorros.append(ExampleOracleRepo.getCountStatusExample())

    listResults = await asyncio.gather(*listCorros)

    dictResults = {k: v for d in listResults for k, v in d.items()}

    logger.info(f'DD result: {dictResults}')
    return dictResults


async def main():
    """
    Author: Lukas Fojtik, Created: 10.3.2020
    Main function for scheduled gathering of checks and saving them to related MonitoringDB tables
    :return: N/A
    """

    startTaskTime = TimeTools.getStrfTimePrecisSec()

    await asyncio.sleep(1)

    ## Obtain and save to MonitoringDB

    # get results
    dictResults = await getResults(startTaskTime)

    # set results to the model object
    exampleNew = Example(ins_time=TimeTools.getStrfNow(), **dictResults)

    # write object parameters to monitoring db
    with MonPersistenceOrm() as mpo:
        mpo.session.add(exampleNew)
        mpo.session.commit()

