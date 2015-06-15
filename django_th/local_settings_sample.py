# sample for dev purpose
# to be used by the command :
# python manage.py --settings=my_app.local_settings
from .settings import *

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
    'consumer_key': 'my key',
    'consumer_secret': 'my secret'
}

# CELERY
BROKER_URL = 'redis://localhost:6379/0'

CELERYBEAT_SCHEDULE = {
    'add-read-data': {
        'task': 'django_th.tasks.read_data',
        'schedule': crontab(minute='*/27'),
    },
    'add-publish-data': {
        'task': 'django_th.tasks.publish_data',
        'schedule': crontab(minute='*/59'),
    },
}

# REDISBOARD
REDISBOARD_DETAIL_FILTERS = ['.*']
