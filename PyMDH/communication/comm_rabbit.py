from sanic.log import logger, error_logger
import aiohttp
from aiohttp import ClientSession
from aiohttp import client_exceptions


class RabbitManagement:
    """
    Class for getting RabbitMQ checks data based on calling RabbitMQ REST "Management API"
    Can be further optimized (split and move general async REST calls part into separate modul and keep here only RabbitMQ related part and/or remake it to work in batches and use only one session...)
    """

    dictEndpoints = {
        'queue_info': '/queues/{vhost}/{queue}',
    }

    def __init__(self, rabbitApiUrl, rabbitUser, rabbitPassword, timeout=20):
        self.rabbitApiUrl = rabbitApiUrl
        self.rabbitUser = rabbitUser
        self.rabbitPassword = rabbitPassword
        self.timeout = timeout

        self.httpAuth = aiohttp.BasicAuth(self.rabbitUser, self.rabbitPassword)
        self._check = ''

    @property
    def check(self):
        return self._check

    @check.setter
    def check(self, value):
        self._check = value

    async def fetchGetResponse(self, session, url):
        """
        Author: Lukas Fojtik, 21.1.2020
        Use session object to perform 'get' request on url
        :param session: aiohttp library ClientSession class object
        :param url: str - whole url to be called
        :return: dict - content of body
        """
        try:
            async with session.get(url, verify_ssl=False, allow_redirects=True, auth=self.httpAuth, timeout=self.timeout) as response:

                # check whether response is correct - http status 200 and only then return response body, otherwise return None
                try:
                    assert (response.status == 200),"Bad http status detected: %s while calling url: %s" % (response.status, url)
                    return await response.json()
                except AssertionError as err:
                    logger.warning(err)

        except aiohttp.client_exceptions.ClientConnectorError as err:
            error_logger.error("Error during request %s %s" % (type(err), err))


    async def getResponseResult(self, endpoint):
        """
        Author: Lukas Fojtik, 21.1.2020
        Compose Rabbit management API whole url and call method for fetching REST GET Response Body
        :param endpoint: str - RabbitMQ management API endpoint
        :return: dict - content of body
        """

        url = self.rabbitApiUrl + endpoint
        logger.debug('Calling rabbit mng API: ' + url)

        async with ClientSession() as session:
            return await self.fetchGetResponse(session, url)

    async def getMsgCount(self, vhost, queue):

        endpoint = RabbitManagement.dictEndpoints.get('queue_info').format(vhost=vhost, queue=queue)
        responseBody = await self.getResponseResult(endpoint)
        logger.debug(responseBody)

        try:
            msgCount = responseBody.get('messages')
        except AttributeError as err:
            error_logger.error("Unexpected response body from Rabbit %s %s" % (type(err), err))
            msgCount = None

        if msgCount == None:
            logger.warning(f'RabbitMQ MNG queues API: {endpoint} do not contain "messages" parameter or no response at all..')

        return self._check, msgCount

    async def getQueueReadoutStatus(self, vhost, queue):

        endpoint = RabbitManagement.dictEndpoints.get('queue_info').format(vhost=vhost, queue=queue)
        responseBody = await self.getResponseResult(endpoint)
        logger.debug(responseBody)

        try:
            msgCount = responseBody.get('messages')
            ackRateCount = responseBody['message_stats']['ack_details']['rate']
        except (AttributeError, KeyError) as err:
            # error_logger.error("Unexpected response body from Rabbit %s %s" % (type(err), err))
            error_logger.exception("Unexpected response body from Rabbit %s %s %s" % (type(err), err, responseBody), exc_info=True)
            return self._check, None

        if msgCount > 0 and ackRateCount == 0:
            result = 1
        else:
            result = 0

        return self._check, result




















