# coding: utf-8

# django classes
from django.conf import settings
from django.utils.log import getLogger
from django.core.cache import caches

# django_th classes
from django_th.services.services import ServicesMgr


"""
    This service permits to send mail

    put the following in settings.py

    TH_EMAIL = {
        'from': 'foo@bar.com,
    }

    TH_SERVICES = (
        ...
        'th_email.my_email.ServiceEmail',
        ...
    )

"""

logger = getLogger('django_th.trigger_happy')

cache = caches['th_email']


class ServiceEmail(ServicesMgr):

    def __init__(self, token=None):
        pass

    def read_data(self, token, trigger_id, date_triggered):
        """
            get the data from the service
            as the pocket service does not have any date
            in its API linked to the note,
            add the triggered date to the dict data
            thus the service will be triggered when data will be found
            :param trigger_id: trigger ID to process
            :param date_triggered: the date of the last trigger
            :type trigger_id: int
            :type date_triggered: datetime
            :return: list of data found from the date_triggered filter
            :rtype: list
        """
        data = list()
        cache.set('th_email_' + str(trigger_id), data)

    def process_data(self, trigger_id):
        """
            get the data from the cache
            :param trigger_id: trigger ID from which to save data
            :type trigger_id: int
        """
        return cache.get('th_email_' + str(trigger_id))

    def save_data(self, token, trigger_id, **data):
        """
            let's save the data

            :param trigger_id: trigger ID from which to save data
            :param **data: the data to check to be used and save
            :type trigger_id: int
            :type **data:  dict
            :return: the status of the save statement
            :rtype: boolean
        """
        from django.core.mail import send_mail
        from th_email.models import Email
        status = False

        if token and trigger_id:
            # get the details of this trigger
            trigger = Email.objects.get(trigger_id=trigger_id)

            title = (data['title'] if 'title' in data else '')

            send_mail(title, data, settings.TH_EMAIL['from'], [trigger.email],
                      fail_silently=False)

            sentance = str('Email {title} sent').format(title=title)
            logger.debug(sentance)
            status = True
        else:
            sentance = "no token or link provided for trigger ID {trigger_id}"
            logger.critical(sentance.format(trigger_id=trigger_id))
            status = False
        return status
