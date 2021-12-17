# do not remove asyncio -> otherwise SEGFAULT error occurs

import asyncio
import config.logging as conflog
from config import settings
import controller.routes as routeslist
import tasks.tasklist as tasklist
import common.common_preparation as preparation
from sanic import Sanic
from sanic_scheduler import SanicScheduler
from config.logging import logger

# setup of core app
app = Sanic(__name__, log_config=conflog.LOGGING_CONFIG_DEFAULTS)
app.config.from_object(settings)
scheduler = SanicScheduler(app)


# check and prepare prerequisites for app to run
@app.listener('before_server_start')
async def handlePrequisities(app, loop):
    logger.info('Running prequisities actions..')
    preparation.prepare4Run()

# do actions after server start
@app.listener('after_server_start')
async def afterStartInit(app, loop):
    logger.info('Running after server start actions..')
    preparation.prepareAfterStart()


def init():
    """
    Author: Lukas Fojtik, created on: 25.11.2019
    Initialization of application.
    :return: N/A
    """

    routeslist.setup_routes(app)
    tasklist.setup_tasks(app)

    # debug parameter cause amongst other effects reload of eventually changed file (useful for changing configuration during run)
    # however this can be achieved also by parameter auto_reload=True
    app.run(host=app.config.HOST, port=app.config.PORT, debug=False, auto_reload=True)

if __name__ == "__main__":
    init()

