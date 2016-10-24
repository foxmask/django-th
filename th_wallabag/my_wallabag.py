# coding: utf-8
# add here the call of any native lib of python like datetime etc.
import arrow
import requests
from requests import HTTPError
# add the python API here if needed
from wallabag_api.wallabag import Wallabag as Wall
# django classes
from django.core.urlresolvers import reverse
from django.utils.log import getLogger
from django.core.cache import caches

# django_th classes
from django_th.services.services import ServicesMgr
from django_th.html_entities import HtmlEntities
from django_th.models import UserService, ServicesActivated, update_result
from th_wallabag.models import Wallabag

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

cache = caches['th_wallabag']


class ServiceWallabag(ServicesMgr):
    """
        Service Wallabag
    """
    def __init__(self, token=None, **kwargs):
        super(ServiceWallabag, self).__init__(token, **kwargs)
        self.token = token
        self.user = kwargs.get('user')

    def _get_wall_data(self):
        us = UserService.objects.get(token=self.token, name='ServiceWallabag')

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
            params['access_token'] = self._refresh_token()
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
            if len(data) > 0:
                cache.set('th_wallabag_' + str(self.trigger_id), data)
        except Exception as e:
                logger.critical(e)
                update_result(self.trigger_id, msg=e)
        return data

    def new_wall(self, token):
        """
            produce a new wall instance
            :param token: to get
            :return: Wall instance
        """
        if token:
            try:
                us = UserService.objects.get(
                    token=self.token, name='ServiceWallabag')
            except UserService.DoesNotExist:
                us = UserService.objects.get(
                    user=self.user, name='ServiceWallabag')
            finally:
                return Wall(host=us.host, client_secret=us.client_secret,
                            client_id=us.client_id, token=us.token)

    def _create_entry(self, title, data, tags):
        """
            create an entry
            :param title: string
            :param data: dict
            :param tags: list
            :return: boolean
        """
        if data.get('link') and len(data.get('link')) > 0:
            wall = self.new_wall(self.token)
            try:
                wall.post_entries(url=data.get('link').encode(),
                                  title=title,
                                  tags=(tags.lower()))
                logger.debug('wallabag {} created'.format(data.get('link')))
                status = True
            except Exception as e:
                if e.errno == 401:
                    status = self._new_token(data.get('userservice_id'),
                                             data.get('link').encode(),
                                             title,
                                             tags.lower())
                else:
                    logger.critical('issue with something else that a token'
                                    ' link ? : {}'.format(data.get('link')))
                    logger.critical(e.errno, e.strerror)
                    update_result(self.trigger_id, msg=e)
                    status = False
        else:
            status = True  # we ignore empty link
        return status

    def _refresh_token(self):
        """
            refresh the expired token
            get the token of the service Wallabag
            for the user that uses Wallabag
            :return: boolean
        """
        us = UserService.objects.get(user=self.user, name='ServiceWallabag')
        params = {'username': us.username,
                  'password': us.password,
                  'client_id': us.client_id,
                  'client_secret': us.client_secret}
        return Wall.get_token(host=us.host, **params)

    def _new_token(self, userservice_id, link, title, tags):
        """
            create a new token
            :param userservice_id: id of the UserService
            :param link: string
            :param title: string
            :param tags: list
            :return: boolean
        """
        new_token = self._refresh_token()
        logger.info('new token : {}'.format(new_token))
        UserService.objects.filter(id=userservice_id).update(token=new_token)

        new_wall = self.new_wall(new_token)
        try:
            status = new_wall.post_entries(url=link, title=title, tags=tags)
        except Exception as e:
            logger.critical('could not create a post link ? : {}'.format(link))
            logger.critical(e)
            update_result(self.trigger_id, msg=e)
            status = False
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
        trigger = Wallabag.objects.get(trigger_id=trigger_id)

        title = self.set_title(data)
        # convert htmlentities
        title = HtmlEntities(title).html_entity_decode

        return self._create_entry(title, data, trigger.tag)

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
