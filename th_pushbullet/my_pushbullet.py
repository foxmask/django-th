# coding: utf-8
import arrow
# Pushbullet
from pushbullet import Pushbullet as Pushb

# django classes
from django.conf import settings
from django.utils.log import getLogger
from django.core.cache import caches

# django_th classes
from django_th.services.services import ServicesMgr
from django_th.models import update_result
from th_pushbullet.models import Pushbullet


"""
    handle process with pushbullet
    put the following in settings.py

    TH_PUSHBULLET = {
        'client_id': 'abcdefghijklmnopqrstuvwxyz',
        'client_secret': 'abcdefghijklmnopqrstuvwxyz',
    }
    TH_SERVICES = (
        ...
        'th_pushbullet.my_pushbullet.ServicePushbullet',
        ...
    )
"""

logger = getLogger('django_th.trigger_happy')

cache = caches['th_pushbullet']


class ServicePushbullet(ServicesMgr):
    """
        Service Pushbullet
    """
    def __init__(self, token=None, **kwargs):
        super(ServicePushbullet, self).__init__(token, **kwargs)
        self.AUTH_URL = 'https://pushbullet.com/authorize'
        self.ACC_TOKEN = 'https://pushbullet.com/access_token'
        self.REQ_TOKEN = 'https://api.pushbullet.com/oauth2/token'
        self.consumer_key = settings.TH_PUSHBULLET['client_id']
        self.consumer_secret = settings.TH_PUSHBULLET['client_secret']
        self.scope = 'everything'
        self.service = 'ServicePushbullet'
        self.oauth = 'oauth2'
        if token:
            self.token = token
            self.pushb = Pushb(token)

    def read_data(self, **kwargs):
        """
            get the data from the service
            as the pushbullet service does not have any date
            in its API linked to the note,
            add the triggered date to the dict data
            thus the service will be triggered when data will be found

            :param kwargs: contain keyword args : trigger_id at least
            :type kwargs: dict

            :rtype: list
        """
        trigger_id = kwargs.get('trigger_id')
        trigger = Pushbullet.objects.get(trigger_id=trigger_id)
        date_triggered = kwargs.get('date_triggered')
        data = list()
        pushes = self.pushb.get_pushes()
        for p in pushes:
            title = 'From Pushbullet'
            created = arrow.get(p.get('created'))
            if created > date_triggered and p.get('type') == trigger.type and\
                (p.get('sender_email') == p.get('receiver_email') or
                 p.get('sender_email') is None):
                title = title + ' Channel' if p.get('channel_iden') and \
                                              p.get('title') is None else title
                # if sender_email and receiver_email are the same ;
                # that means that "I" made a note or something
                # if sender_email is None, then "an API" does the post

                body = p.get('body')
                data.append({'title': title, 'content': body})

        cache.set('th_pushbullet_' + str(trigger_id), data)
        return data

    def save_data(self, trigger_id, **data):
        """
            let's save the data
            :param trigger_id: trigger ID from which to save data
            :param data: the data to check to be used and save
            :type trigger_id: int
            :type data:  dict
            :return: the status of the save statement
            :rtype: boolean
        """
        title, content = super(ServicePushbullet, self).save_data(trigger_id,
                                                                  **data)

        if self.token:
            trigger = Pushbullet.objects.get(trigger_id=trigger_id)
            if trigger.type == 'note':
                status = self.pushb.push_note(title=title, body=content)
            elif trigger.type == 'link':
                status = self.pushb.push_link(title=title, body=content,
                                              url=data.get('link'))
                sentence = str('pushbullet {} created').format(title)
                logger.debug(sentence)
            else:
                # no valid type of pushbullet specified
                msg = "no valid type of pushbullet specified"
                logger.critical(msg)
                update_result(trigger_id, msg=msg)
                status = False
        else:
            msg = "no token or link provided for trigger " \
                  "ID {} ".format(trigger_id)
            logger.critical(msg)
            update_result(trigger_id, msg=msg)
            status = False
        return status
