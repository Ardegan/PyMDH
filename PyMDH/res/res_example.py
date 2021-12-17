from config.settings import RABBIT_EXAMPLE_VHOST
from config.settings import REST_URL

dictRestCalls = {
    'rest_health': {
        'base_url': REST_URL,
        'function': 'getHealthStatus'
    }
}

dictRabbitQueues = {
    'rmq_inc_cnt': {
        'vhost': RABBIT_EXAMPLE_VHOST,
        'queue': 'some.queue'
    },
    'rmq_inc_readout': {
        'vhost': RABBIT_EXAMPLE_VHOST,
        'queue': 'some.queue',
        'function': 'getQueueReadoutStatus'
    }
}

# Example of time placeholder: between {fromTime} - interval '3' day and {toTime} - interval '30' minute
dictSelects = {
    'db_example_wait': ''' select 10 from dual ''',
    'db_example_errors': ''' select 11 from dual '''
}

dictSelectsJson = {
    'db_example_json': ''' select 'type', 
                                    1, 
                                    2,
                                    3.7
                                from dual '''
}

dictCountExample = {
    'db_example_count_status': ''' select 48562 from dual '''
}
