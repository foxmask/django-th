# coding: utf-8
# add here the call of any native lib of python like datetime etc.
import arrow
# django classes
from django.core.urlresolvers import reverse
from django.core.cache import caches
# django_th classes
from django_th.services.services import ServicesMgr
from django_th.html_entities import HtmlEntities
from django_th.models import UserService, ServicesActivated, update_result

from logging import getLogger
import requests
from requests import HTTPError

from th_wallabag.models import Wallabag
# add the python API here if needed
from wallabag_api.wallabag import Wallabag as Wall

"""
    handle process with wallabag
    put the following in settings.py

    TH_SERVICES = (
        ...
        'th_wallabag.my_wallabag.ServiceWallabag',
        ...
    )
"""

logger = getLogger('django_th.trigger_happy')

cache = caches['django_th']


class ServiceWallabag(ServicesMgr):
    """
        Service Wallabag
    """
    def __init__(self, token=None, **kwargs):
        super(ServiceWallabag, self).__init__(token, **kwargs)
        self.token = token
        self.user = kwargs.get('user')

    def _get_wall_data(self):
        us = UserService.objects.get(user=self.user, name='ServiceWallabag')

        params = dict({'access_token': self.token,
                       'archive': 0,
                       'star': 0,
                       'delete': 0,
                       'sort': 'created',
                       'order': 'desc',
                       'page': 1,
                       'perPage': 30,
                       'tags': []})

        responses = requests.get(us.host + '/api/entries.json',
                                 params=params)
        if responses.status_code == 401:
            params['access_token'] = Wall.get_token(host=us.host, **params)
            responses = requests.get(us.host + '/api/entries.json',
                                     params=params)
        elif responses.status_code != 200:
            raise HTTPError(responses.status_code, responses.json())

        return responses

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
        self.date_triggered = arrow.get(kwargs.get('date_triggered'))
        self.trigger_id = kwargs.get('trigger_id')
        self.user = kwargs.get('user', '')

        responses = self._get_wall_data()

        data = []
        try:
            json_data = responses.json()

            for d in json_data['_embedded']['items']:
                created_at = arrow.get(d.get('created_at'))
                date_triggered = arrow.get(self.date_triggered)

                if created_at > date_triggered:
                    data.append({'title': d.get('title'),
                                 'content': d.get('content')})
                    # digester
                    self.send_digest_event(self.trigger_id,
                                           d.get('title'),
                                           link='')
            if len(data) > 0:
                cache.set('th_wallabag_' + str(self.trigger_id), data)
        except Exception as e:
                logger.critical(e)
                update_result(self.trigger_id, msg=e, status=False)
        return data

    def wall(self):
        """
            refresh the token from the API
            then call a Wallabag instance
            then store the token
        :return: wall instance
        """
        us = UserService.objects.get(user=self.user, name='ServiceWallabag')
        params = {
            'client_id': us.client_id,
            'client_secret': us.client_secret,
            'username': us.username,
            'password': us.password,
        }
        try:
            token = Wall.get_token(host=us.host, **params)
        except Exception as e:
            update_result(self.trigger_id, msg=e, status=False)
            logger.critical('{} {}'.format(self.user, e))
            return False

        wall = Wall(host=us.host, client_secret=us.client_secret,
                    client_id=us.client_id, token=token)

        UserService.objects.filter(user=self.user,
                                   name='ServiceWallabag').update(token=token)

        return wall

    def _create_entry(self, title, data, tags):
        """
            create an entry
            :param title: string
            :param data: dict
            :param tags: list
            :return: boolean
        """
        status = False
        if data.get('link') and len(data.get('link')) > 0:
            wall = self.wall()
            if wall is not False:
                try:
                    wall.post_entries(url=data.get('link').encode(), title=title, tags=(tags.lower()))
                    logger.debug('wallabag {} created'.format(data.get('link')))
                    status = True
                except Exception as e:
                    logger.critical('issue with something else that a token link ? : {}'.format(data.get('link')))
                    logger.critical(e)
                    update_result(self.trigger_id, msg=e, status=False)
                    status = False
        else:
            status = True  # we ignore empty link
        return status

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
        self.trigger_id = trigger_id

        trigger = Wallabag.objects.get(trigger_id=trigger_id)

        title = self.set_title(data)
        if title is not None:
            # convert htmlentities
            title = HtmlEntities(title).html_entity_decode

            return self._create_entry(title, data, trigger.tag)
        else:
            # we ignore data without title so return True to let
            # the process continue without
            # raising exception
            return True

    def auth(self, request):
        """
            let's auth the user to the Service
            :param request: request object
            :return: callback url
            :rtype: string that contains the url to redirect after auth

        """
        service = UserService.objects.get(
            user=request.user, name='ServiceWallabag')
        callback_url = 'http://%s%s' % (
            request.get_host(), reverse('wallabag_callback'))
        params = {'username': service.username,
                  'password': service.password,
                  'client_id': service.client_id,
                  'client_secret': service.client_secret}
        access_token = Wall.get_token(host=service.host, **params)
        request.session['oauth_token'] = access_token
        return callback_url

    def callback(self, request, **kwargs):
        """
            Called from the Service when the user accept to activate it
            :param request: request object
            :return: callback url
            :rtype: string , path to the template
        """

        try:
            UserService.objects.filter(
                user=request.user,
                name=ServicesActivated.objects.get(name='ServiceWallabag')
            )
        except KeyError:
            return '/'

        return 'wallabag/callback.html'
