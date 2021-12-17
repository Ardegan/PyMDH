from repository.rest.general import getRestMonitorDict
from res.res_example import dictRestCalls


class ExampleRestRepo:

    @staticmethod
    async def getResult():
        """
        Author: Lukas Fojtik, created on: 08.04.2021
        Obtaining monitoring values of REST checks
        :return: Dictionary containing BAS related monitoring results obtained via REST API of apps
        """

        return await getRestMonitorDict(dictRestCalls)
