# coding: utf-8
import datetime
import time
import arrow

# pocket API
import pocket
from pocket import Pocket

# django classes
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.log import getLogger
from django.core.cache import caches

# django_th classes
from django_th.services.services import ServicesMgr
from django_th.models import UserService, ServicesActivated
from django_th.html_entities import HtmlEntities
from django_th.publishing_limit import PublishingLimit

"""
    handle process with pocket
    put the following in settings.py

    TH_POCKET = {
        'consumer_key': 'abcdefghijklmnopqrstuvwxyz',
    }

    TH_SERVICES = (
        ...
        'th_pocket.my_pocket.ServicePocket',
        ...
    )

"""

logger = getLogger('django_th.trigger_happy')

cache = caches['th_pocket']


class ServicePocket(ServicesMgr):

    def __init__(self, token=None):
        self.consumer_key = settings.TH_POCKET['consumer_key']
        if token:
            self.pocket = Pocket(self.consumer_key, token)

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
        # pocket uses a timestamp date format
        since = int(
            time.mktime(datetime.datetime.timetuple(date_triggered)))

        if token is not None:

            # get the data from the last time the trigger have been started
            # timestamp form
            pockets = self.pocket.get(since=since, state="unread")

            if pockets is not None and len(pockets[0]['list']) > 0:
                for my_pocket in pockets[0]['list'].values():
                    if my_pocket['excerpt']:
                        content = my_pocket['excerpt']
                    elif my_pocket['given_title']:
                        content = my_pocket['given_title']
                    my_date = arrow.get(str(date_triggered),
                                        'YYYY-MM-DD HH:mm:ss')\
                                   .to(settings.TIME_ZONE)
                    data.append({'my_date': str(my_date),
                                 'tag': '',
                                 'link': pocket['given_url'],
                                 'title': pocket['given_title'],
                                 'content': content,
                                 'tweet_id': 0})
                cache.set('th_pocket_' + str(trigger_id), data)

        return data

    def process_data(self, trigger_id):
        """
            get the data from the cache
            :param trigger_id: trigger ID from which to save data
            :type trigger_id: int
        """
        cache_data = cache.get('th_pocket_' + str(trigger_id))
        return PublishingLimit.get_data('th_pocket', cache_data, trigger_id)

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
        from th_pocket.models import Pocket as PocketModel

        status = False

        if token and 'link' in data and data['link'] is not None\
                and len(data['link']) > 0:
            # get the pocket data of this trigger
            trigger = PocketModel.objects.get(trigger_id=trigger_id)

            title = ''
            title = self.set_title(data)
            # convert htmlentities
            title = HtmlEntities(title).html_entity_decode

            try:
                self.pocket.add(
                    url=data['link'], title=title, tags=(trigger.tag.lower()))

                sentence = str('pocket {} created').format(data['link'])
                logger.debug(sentence)
                status = True
            except Exception as e:
                logger.critical(e)
                status = False

        else:
            logger.critical("no token provided for trigger ID %s ", trigger_id)
        return status

    def auth(self, request):
        """
            let's auth the user to the Service
        """
        callback_url = 'http://%s%s' % (
            request.get_host(), reverse('pocket_callback'))

        request_token = Pocket.get_request_token(
            consumer_key=self.consumer_key,
            redirect_uri=callback_url)

        # Save the request token information for later
        request.session['request_token'] = request_token

        # URL to redirect user to, to authorize your app
        auth_url = Pocket.get_auth_url(
            code=request_token, redirect_uri=callback_url)

        return auth_url

    def callback(self, request):
        """
            Called from the Service when the user accept to activate it
        """

        try:
            # finally we save the user auth token
            # As we already stored the object ServicesActivated
            # from the UserServiceCreateView now we update the same
            # object to the database so :
            # 1) we get the previous object
            us = UserService.objects.get(
                user=request.user,
                name=ServicesActivated.objects.get(name='ServicePocket'))
            # 2) then get the token
            access_token = Pocket.get_access_token(
                consumer_key=self.consumer_key,
                code=request.session['request_token'])

            us.token = access_token
            # 3) and save everything
            us.save()
        except KeyError:
            return '/'

        return 'pocket/callback.html'
