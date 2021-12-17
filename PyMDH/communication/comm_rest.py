from aiohttp import client_exceptions, BasicAuth
from sanic.log import error_logger, logger


class RestMonitor:
    """
    Class for getting REST related checks as are health checks or specific API checks etc.."
    """

    timeout = 20

    def __init__(self, session):
        self._session = session
        self._check = None

    @property
    def check(self):
        return self._check

    @check.setter
    def check(self, value):
        self._check = value

    async def getHttpResponse(self, url, user=None, password=None):
        """
        Author: Lukas Fojtik, created on: 30.03.2021
        Use session object to perform 'get' request on url
        :param password: credentials - password.
        :param user: credentials - user. If not provided, do the call without credentials.
        :param session: aiohttp library ClientSession class object
        :param url: str - whole url to be called
        :return: dict - content of body
        """

        dictGetParams = {
            'url': url,
            'verify_ssl': False,
            'allow_redirects': False,
            'timeout': self.timeout
        }

        if user:
            httpAuth = BasicAuth(user, password)
            dictGetParams['auth'] = httpAuth

        try:

            # async with self._session.get(url, verify_ssl=True, allow_redirects=False, auth=httpAuth, timeout=self.timeout) as response:
            async with self._session.get(**dictGetParams) as response:

                status = response.status

                if response.status == 200:
                    body = await response.json()
                    return status, body
                else:
                    return status

        except client_exceptions.ClientConnectorError as err:
            error_logger.error("Error during request %s %s" % (type(err), err))

    async def getHealthStatus(self, baseUrl, user=None, password=None):
        """
        Author: Lukas Fojtik, created on: 30.03.2021
        Obtain health status from response - aimed at actuator formatted body.
        :return: 0 - UP, 1 - DOWN
        """

        url = baseUrl + '/actuator/health'

        logger.debug('Calling health check API: ' + url)

        try:
            status, body = await self.getHttpResponse(url, user, password)
        except TypeError as err:
            error_logger.error("Health check returns empty response for url: " + url)
            return

        if not status == 200:
            error_logger.error("Health check returns non 200 http status for url: " + url + ", status: " + status)
            return 1
        else:
            logger.debug('Health check returns body:' + str(body))

            healthStatus = body.get('status')

            if healthStatus == 'UP':
                result = 0
            else:
                result = 1

            return self._check, result


