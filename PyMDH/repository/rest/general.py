import asyncio

from aiohttp import ClientSession

from communication.comm_rest import RestMonitor


async def getRestMonitorDict(dictionary):
    """
    Author: Lukas Fojtik, created on: 06.04.2020
    :param dictionary: dict - Dictionary of dictionaries containing keys named as monitoring check name.
    :return: dict - Dictionary (this time simple) containing again keys named as monitoring check name and values are results of those checks (mostly integers)
    """

    tasks = []

    async with ClientSession() as session:
        rm = RestMonitor(session)

        for check, assets in dictionary.items():

            rm.check = check

            functionName = assets.get('function')

            function = getattr(rm, functionName)
            task = function(assets.get('base_url'))

            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        dictRestMonitorResults = dict(responses)

    return dictRestMonitorResults