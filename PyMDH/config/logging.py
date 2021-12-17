import logging
import sys, os
from datetime import datetime

from config.settings import LOG_LEVEL_ROOT
from config.settings_general import LOG_NAME, pathProject

pathLogDir = os.path.abspath(os.path.join(pathProject, 'log'))
pathLogFile = os.path.join(pathLogDir, LOG_NAME)
maxBytes2Rotate = 1024*1024*10
maxBackupCount=5

try:
    os.makedirs(pathLogDir, exist_ok=True)
except OSError as err:
    print(str(datetime.now()) + " Unable to create directory for logs: %s %s" % (type(err), err))

LOGGING_CONFIG_DEFAULTS = dict(
    version=1,
    disable_existing_loggers=False,
    loggers={
        "sanic.root": {"level": LOG_LEVEL_ROOT, "handlers": ["console", "file"]},
        "sanic.error": {
            "level": "INFO",
            "handlers": ["error_console", "error_file"],
            "propagate": True,
            "qualname": "sanic.error",
        },
        "sanic.access": {
            "level": "INFO",
            "handlers": ["access_console", "access_file"],
            "propagate": True,
            "qualname": "sanic.access",
        },
    },
    handlers={
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": sys.stdout,
        },
        "error_console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": sys.stderr,
        },
        "access_console": {
            "class": "logging.StreamHandler",
            "formatter": "access",
            "stream": sys.stdout,
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "generic",
            "filename": pathLogFile,
            "maxBytes" : maxBytes2Rotate,
            "backupCount" : maxBackupCount
        },
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "generic",
            "filename": pathLogFile,
            "maxBytes" : maxBytes2Rotate,
            "backupCount" : maxBackupCount
        },
        "access_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "access",
            "filename": pathLogFile,
            "maxBytes" : maxBytes2Rotate,
            "backupCount" : maxBackupCount
        }

    },
    formatters={
        "generic": {
            "format": "[%(asctime)s.%(msecs)03d] [%(process)d] [%(levelname)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "class": "logging.Formatter",
        },
        "access": {
            "format": "%(asctime)s.%(msecs)03d - (%(name)s)[%(levelname)s][%(host)s]: "
                      + "%(request)s %(message)s %(status)d %(byte)d",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "class": "logging.Formatter",
        },
    },
)

logger = logging.getLogger("sanic.root")
error_logger = logging.getLogger("sanic.error")
access_logger = logging.getLogger("sanic.access")
