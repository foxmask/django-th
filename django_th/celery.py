from __future__ import absolute_import

import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_th.settings')

app = Celery('django_th')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# will start the 2 tasks,
# one each 41 minutes
# the other one each hour
CELERYBEAT_SCHEDULE = {
    'add-read-data': {
        'task': 'tasks.read_data',
        'schedule': crontab(minute='*/41'),
    },
    'add-publish-data': {
        'task': 'tasks.publish_data',
        'schedule': crontab(hour='*/1'),
    },
}
