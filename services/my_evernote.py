# -*- coding: utf-8 -*-

from .services import Services
from evernote.api.client import EvernoteClient
from django.conf import settings
"""
    handle process with evernote
    put the following in settings.py

    TH_SERVICE_EVERNOTE = {
        'sandbox': True,
        'consumer_key': 'abcdefghijklmnopqrstuvwxyz',
        'consumer_secret': 'abcdefghijklmnopqrstuvwxyz',
    }
    sanbox set to True to make your test and False for production purpose
"""


class ServiceEvernote(Services):

    def get_title(self):
        pass

    def get_body(self):
        pass

    def process_data(self):
        pass

    def get_evernote_client(self, token=None):
        if token:
            return EvernoteClient(token=token,
                            sandbox=settings.TH_SERVICE_EVERNOTE['sandbox'])
        else:
            return EvernoteClient(
                consumer_key=settings.TH_SERVICE_EVERNOTE['consumer_key'],
                consumer_secret=settings.TH_SERVICE_EVERNOTE['consumer_secret'],
                sandbox=settings.TH_SERVICE_EVERNOTE['sandbox']
            )
