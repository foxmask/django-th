# coding: utf-8
import datetime
import time
import arrow

# pocket API
from pocket import Pocket

# django classes
from django.conf import settings
from django.utils.log import getLogger
from django.core.cache import caches

# django_th classes
from django_th.models import update_result
from django_th.services.services import ServicesMgr
from django_th.html_entities import HtmlEntities

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
    """
        Service Pocket
    """
    def __init__(self, token=None, **kwargs):
        super(ServicePocket, self).__init__(token, **kwargs)
        self.consumer_key = settings.TH_POCKET['consumer_key']
        self.token = token
        self.oauth = 'oauth1'
        self.service = 'ServicePocket'
        if token:
            self.pocket = Pocket(self.consumer_key, token)

    def _create_entry(self, url, title, tags):
        """
            Create an entry
            :param url:  url to save
            :param title: title to set
            :param tags: tags to set
            :return: status
        """
        try:
            self.pocket.add(url=url, title=title, tags=tags)
            sentence = str('pocket {} created').format(url)
            logger.debug(sentence)
            status = True
        except Exception as e:
            logger.critical(e)
            update_result(self.trigger_id, msg=e)
            status = False
        return status

    def read_data(self, **kwargs):
        """
            get the data from the service
            as the pocket service does not have any date
            in its API linked to the note,
            add the triggered date to the dict data
            thus the service will be triggered when data will be found

            :param kwargs: contain keyword args : trigger_id at least
            :type kwargs: dict

            :rtype: list
        """
        trigger_id = kwargs.get('trigger_id')
        date_triggered = kwargs.get('date_triggered')

        data = list()
        # pocket uses a timestamp date format
        since = int(
            time.mktime(datetime.datetime.timetuple(date_triggered)))

        if self.token is not None:

            # get the data from the last time the trigger have been started
            # timestamp form
            pockets = self.pocket.get(since=since, state="unread")
            content = ''
            if pockets is not None and len(pockets[0]['list']) > 0:
                for my_pocket in pockets[0]['list'].values():
                    if my_pocket.get('excerpt'):
                        content = my_pocket['excerpt']
                    elif my_pocket.get('given_title'):
                        content = my_pocket['given_title']
                    my_date = arrow.get(str(date_triggered),
                                        'YYYY-MM-DD HH:mm:ss')\
                        .to(settings.TIME_ZONE)
                    data.append({'my_date': str(my_date),
                                 'tag': '',
                                 'link': my_pocket['given_url'],
                                 'title': my_pocket['given_title'],
                                 'content': content,
                                 'tweet_id': 0})
                cache.set('th_pocket_' + str(trigger_id), data)

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
        if data.get('link'):
            if len(data.get('link')) > 0:
                # get the pocket data of this trigger
                from th_pocket.models import Pocket as PocketModel
                trigger = PocketModel.objects.get(trigger_id=trigger_id)

                title = self.set_title(data)
                # convert htmlentities
                title = HtmlEntities(title).html_entity_decode

                status = self._create_entry(url=data.get('link'),
                                            title=title,
                                            tags=(trigger.tag.lower()))
            else:
                msg = "no link provided for trigger ID {}," \
                      " so we ignore it".format(trigger_id)
                logger.warning(msg)
                update_result(trigger_id, msg=msg)
                status = True
        else:
            msg = "no token provided for trigger ID {}".format(trigger_id)
            logger.critical(msg)
            update_result(trigger_id, msg=msg)
            status = False
        return status

    def auth(self, request):
        """
            let's auth the user to the Service
            :param request: request object
            :return: callback url
            :rtype: string that contains the url to redirect after auth
        """
        callback_url = self.callback_url(request)

        request_token = Pocket.get_request_token(
            consumer_key=self.consumer_key,
            redirect_uri=callback_url)

        # Save the request token information for later
        request.session['request_token'] = request_token

        # URL to redirect user to, to authorize your app
        auth_url = Pocket.get_auth_url(
            code=request_token, redirect_uri=callback_url)

        return auth_url

    def callback(self, request, **kwargs):
        """
            Called from the Service when the user accept to activate it
            :param request: request object
            :return: callback url
            :rtype: string , path to the template
        """
        access_token = Pocket.get_access_token(
            consumer_key=self.consumer_key,
            code=request.session['request_token'])

        kwargs = {'access_token': access_token}

        return super(ServicePocket, self).callback(request, **kwargs)
