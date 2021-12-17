from res import res_example

from repository.rabbit.general import getRabbitResultsDict


class ExampleRabbitRepo:

    @staticmethod
    async def getResult():
        '''
        Author: Lukas Fojtik, created on: 10.3.2020
        Obtaining monitoring values from RabbitMQ
        :return: dict - Dictionary containing monitoring results obtained from RabbitMQ
        '''

        dictRabbitQueues = res_example.dictRabbitQueues

        dictResults = await getRabbitResultsDict(dictRabbitQueues)

        return dictResults