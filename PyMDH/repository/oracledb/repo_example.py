from config.settings import SCHED_MODE_EXAMPLE
from res import res_example
from repository.oracledb.general import getOracleDbResult, getFromOra, getToOra
from common.common_tools import VarTools


class ExampleOracleRepo:

    @staticmethod
    async def getResult(inputTime):
        """
        Author: Lukas Fojtik, created on: 10.03.2020
        Obtaining monitoring values from OracleDB
        :return: Dictionary containing related monitoring results obtained from OracleDB
        """

        # Usual checks
        dictSelects = res_example.dictSelects
        dictSelectsFilled = VarTools.formatDictionaryValues(dictSelects, fromTime=getFromOra(inputTime, SCHED_MODE_EXAMPLE), toTime=getToOra(inputTime))
        dictResultsCasual = await getOracleDbResult(dictSelectsFilled)

        # Checks which results in form of JSON
        dictSelectsJson = res_example.dictSelectsJson
        dictJson = await getOracleDbResult(dictSelectsJson, 'fetchAll')

        listFinal = []

        for i in dictJson.get('db_example_json'):
            dictRequestsNested = {
                'type': i[0],
                'first_count': i[1],
                'second_count': i[2],
                'some_average': float(i[3])
            }

            listFinal.append(dictRequestsNested)

        dictJsonFinal = {'db_example_json': listFinal}

        # Combine results and return them
        dictResults = {**dictResultsCasual, **dictJsonFinal}

        return dictResults

    @staticmethod
    async def getStatusResult(dbInput, minLimit):

        resultDict = await getOracleDbResult(dbInput)
        resultValue = next(iter(resultDict.values()))

        if resultValue is None:
            return resultDict

        resultKey = next(iter(resultDict.keys()))

        resultStatus = 0 if resultValue > minLimit else 1
        resultDict[resultKey] = resultStatus

        return resultDict

    @staticmethod
    async def getCountStatusExample():

        selectDict = res_example.dictCountExample
        return await ExampleOracleRepo.getStatusResult(selectDict, 50_000)

