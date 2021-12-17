# general logging settings
LOG_LEVEL_ROOT = 'DEBUG'

SQLALCHEMY_ECHO_DEBUG = True

# base config for sanic framework
HOST = '0.0.0.0'
PORT = '8010'
DEBUG = True

# Tasks settings (described in tasks.tasklist)
SCHED_MODE_EXAMPLE = 'min'

# DB settings
DB_URL = 'mysql+mysqlconnector://user:pass@host:3306/schema'
ORACLE_DB_URL = 'oracle+cx_oracle://user:pass@(description)'

# Rabbit
RABBIT_API_URL = 'https://rabbit.some.domain:15672/api'
RABBIT_USER = 'user'
RABBIT_PASSWORD = 'pass'

RABBIT_EXAMPLE_VHOST = 'vhost'


# REST
REST_URL = 'https://some.application.domain/root'


