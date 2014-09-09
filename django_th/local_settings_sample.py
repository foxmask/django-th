# sample for dev purpose
# to be used by the command :
# python manage.py --settings=my_app.local_settings
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
