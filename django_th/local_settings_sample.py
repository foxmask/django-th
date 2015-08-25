from celery.schedules import crontab

DEBUG = True

TH_EVERNOTE = {
    'sandbox': True,
    'consumer_key': 'my key',
    'consumer_secret': 'my secret',
}

TH_POCKET = {
    'consumer_key': 'my key',
}

TH_READABILITY = {
    'consumer_key': 'my key',
    'consumer_secret': 'my secret'
}

TH_TWITTER = {
    # get your credential by subscribing to
    # https://dev.twitter.com/
    'consumer_key': 'my key',
    'consumer_secret': 'my secret'
}

TH_TRELLO = {
    'consumer_key': 'my key',
    'consumer_secret': 'my secret'

}

# CELERY
BROKER_URL = 'redis://localhost:6379/0'

CELERYBEAT_SCHEDULE = {
    'add-read-data': {
        'task': 'django_th.tasks.read_data',
        'schedule': crontab(minute='27,54'),
    },
    'add-publish-data': {
        'task': 'django_th.tasks.publish_data',
        'schedule': crontab(minute='59'),
    },
    'add-outside-data': {
        'task': 'django_th.tasks.get_outside_cache',
        'schedule': crontab(minute='45'),
    },
}

# REDISBOARD
REDISBOARD_DETAIL_FILTERS = ['.*']

# needed to th_search and haystack
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
    },
}