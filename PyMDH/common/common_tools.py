import datetime
from concurrent.futures import ThreadPoolExecutor


class GlobalVars:

    # Thread pool - keep it rather low, it is being used for while creating sessions into HomerDB
    _threadPoolExecutor = ThreadPoolExecutor(max_workers=5)

    @classmethod
    def getThreadPoolExecutor(cls):
        return cls._threadPoolExecutor


class TimeTools:

    @staticmethod
    def getStrfNow():
        """
        Author: Lukas Fojtik, 10.12.2019
        :return: str - current time string in format like for example: 2020-01-29 08:36:38.939770
        """
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        return now

    @staticmethod
    def getStrfTimePrecisSec(inputTime=None, timeDeltaVar=datetime.timedelta(seconds=0)):
        """
        Author: Lukas Fojtik, 04.02.2020
        :return: str - current time string in format like for example: 2020-01-29 08:36:38
        """

        if inputTime is None:
            inputTime = datetime.datetime.now()

        dateTimeVar = inputTime - timeDeltaVar
        result = dateTimeVar.strftime('%Y-%m-%d %H:%M:%S')

        return result

    @staticmethod
    def pandasTsCm2Timedelta(schedPoint):
        """
        Author: Lukas Fojtik, created on: 05.02.2020
        :param schedPoint: str - String specifying pandas Timestamp ceil mode (as used in sec2start function)
        :return: timedelta - converted Pandas Timestamp ceil mode to timedelta type
        """

        dictSP2deltaArg = {
            'min' : {'minutes' : 1},
            '5min' : {'minutes' : 5},
            '10min' : {'minutes' : 10},
            'h' : {'hours' : 1},
            'd' : {'days' : 1}
        }

        return datetime.timedelta(**dictSP2deltaArg.get(schedPoint))

    @staticmethod
    def isNowEndOfMonth():
        """
        Author: Lukas Fojtik 12.01.2021
        :return: Bool - whether is or is not today last day of month
        """
        dt = datetime.datetime.now()
        todays_month = dt.month
        tomorrows_month = (dt + datetime.timedelta(days=1)).month
        return True if tomorrows_month != todays_month else False

    @staticmethod
    def isNowEndOfMonthRange(days):
        """
        Author: Lukas Fojtik 29.01.2021
        :return: Bool - whether is or is not today one of last day of the month,
                    i.e. within last day of month - number of days specified as attribute
        """
        dt = datetime.datetime.now()
        todays_month = dt.month
        tolerance_month = (dt + datetime.timedelta(days=days)).month
        return True if tolerance_month != todays_month else False


class VarTools:

    @staticmethod
    def formatDictionaryValues(dictionary, **values):
        """
        Author: Lukas Fojtik, 04.02.2020
        :param dictionary: dict - Dictionary with values containing formatting elements - values like: "This fruit: {kindOfFruit} is tasty."
        :param values: kwargs - Keyword arguments for replacing formatting elements, like: kindOfFruit='Banana'
        :return: dict - Dictionary with values which now have filled formatting elements
        """

        dictFilled = {}

        for k, v in dictionary.items():
            x = v.format(**values)
            dictFilled[k] = x

        return dictFilled

