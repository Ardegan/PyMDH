import pandas
from datetime import datetime, timedelta, time, date

from common.common_tools import TimeTools

from sanic_scheduler import task
from config.logging import logger

import service.srv_example as ftr_dd
from config import settings


# Obtain seconds to next starting time - i.e. 1st second of next minute, 5minute, hour etc..
def sec2start(schedPoint):
    """
    Author: Lukas Fojtik, created on: 25.11.2019
    :param schedPoint: Pandas ceil to next time checkpoint:
    'min' - next minute (example: 13:52:00)
    '5min' - next 5minute (example: 13:55:00)
    'h' - next hour (example: 14:00:00)
    'd' = next day (00:00:00)
    :return: int - number of seconds to above plus 1 sec to ensure correctness
    """
    nowDT = datetime.now()

    if isinstance(schedPoint, time):

        if schedPoint > datetime.now().time():
            midnightDate = date.today()
        else:
            midnightDate = date.today() + timedelta(days=1)

        nextSP = datetime.combine(midnightDate, schedPoint)

    else:
        nextSP = pandas.Timestamp.now().ceil(schedPoint).to_pydatetime()

    sec2startOfSP = ((nextSP - nowDT).total_seconds() + 1)
    return timedelta(seconds=sec2startOfSP)


# Define tasks schedule

# useful links: https://github.com/asmodius/sanic-scheduler

def setup_tasks(app):
    """
    Author: Lukas Fojtik, created on: 25.11.2019
    Setup schedule of tasks.
    Task methods are being setup with parameters of time to rerun and time to first start (seconds, days...).
    :param app: Sanic application object
    :return: N/A
    """

    @task(TimeTools.pandasTsCm2Timedelta(settings.SCHED_MODE_EXAMPLE), sec2start(settings.SCHED_MODE_EXAMPLE))
    async def example(_):
        logger.info("example - starting ")
        await ftr_dd.main()
        logger.info("example - finishing ")





