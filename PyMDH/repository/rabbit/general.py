import asyncio

from communication.comm_rabbit import RabbitManagement
from config import settings


async def getRabbitResultsDict(dictionary):
    """
    Author: Lukas Fojtik, created on: 05.02.2020
    :param dictionary: dict - Dictionary of dictionaries containing keys named as monitoring check name.
    Value of each key should be dictionary containing keys 'vhost' and '<asset>' (like 'queue'). Values of this keys are names of those RMQ assets
    :return: dict - Dictionary (this time simple) containing again keys named as monitoring check name and values are results of those checks (mostly integers)
    """

    tasks = []

    for check, assets in dictionary.items():

        rm = RabbitManagement(settings.RABBIT_API_URL, settings.RABBIT_USER, settings.RABBIT_PASSWORD)
        rm.check = check

        functionName = assets.get('function')
        if not functionName:
            functionName = 'getMsgCount'

        function = getattr(rm, functionName)
        task = function(assets.get('vhost'),assets.get('queue'))

        tasks.append(task)

    responses = await asyncio.gather(*tasks)
    dictRabbitQueuesResults = dict(responses)

    return dictRabbitQueuesResults