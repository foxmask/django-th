# coding: utf-8
# add here the call of any native lib of python like datetime etc.

# add the python API here if needed
from wallabag_api.wallabag import Wallabag as Wall
# django classes
from django.core.urlresolvers import reverse
from django.utils.log import getLogger
from django.core.cache import caches

# django_th classes
from django_th.services.services import ServicesMgr
from django_th.html_entities import HtmlEntities
from django_th.models import UserService, ServicesActivated

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

    def __init__(self, token=None):
        super(ServiceWallabag, self).__init__(token)
        self.token = token
        if token:
            try:
                us = UserService.objects.get(token=token, name='ServiceWallabag')

                self.service_username = us.username
                self.service_password = us.password
                self.service_host = us.host
                self.service_client_secret = us.client_secret
                self.service_client_id = us.client_id

                self.wall = Wall(host=self.service_host,
                                 client_secret=self.service_client_secret,
                                 client_id=self.service_client_id,
                                 token=self.token)
            except UserService.DoesNotExist:
                pass

    def _new_wall(self, token):
        """
            new Wallabag instance
            :param token:
            :return: instance
        """
        return Wall(host=self.service_host,
                    client_secret=self.service_client_secret,
                    client_id=self.service_client_id,
                    token=token)

    def _create_entry(self, userservice_id, url, title, tags, shootagain=False):
        """
            Create an entry
            :param userservice_id: id of the service to update with new token
            :param url:  url to save
            :param title: title to set
            :param tags: tags to set
            :param shootagain: retry to create a post after a 401
            :return: status
        """
        if shootagain:
            new_token = self.refresh_token()
            new_wall = self._new_wall(new_token)
            # update the token
            UserService.objects.filter(id=userservice_id).update(token=new_token)
        try:
            if shootagain:
                status = new_wall.post_entries(url=url,
                                               title=title,
                                               tags=tags
                                               )
            else:
                status = self.wall.post_entries(url=url,
                                                title=title,
                                                tags=tags)
            sentence = str('wallabag {} created').format(url)
            logger.debug(sentence)
        except Exception as e:
            if e.errno == 401:
                if shootagain:
                    # break circular call :P
                    logger.critical(e.errno, e.strerror)
                    status = False
                self._create_entry(userservice_id=userservice_id,
                                   url=url,
                                   title=title,
                                   tags=tags,
                                   shootagain=True)
            else:
                logger.critical(e.errno, e.strerror)
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
        data = list()
        trigger_id = kwargs.get('trigger_id')
        cache.set('th_wallabag_' + str(trigger_id), data)

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
                # get the wallabag data for this trigger
                from th_wallabag.models import Wallabag
                trigger = Wallabag.objects.get(trigger_id=trigger_id)

                title = self.set_title(data)
                # convert htmlentities
                title = HtmlEntities(title).html_entity_decode

                status = self._create_entry(userservice_id=data['userservice_id'],
                                            url=data['link'],
                                            title=title,
                                            tags=trigger.tag.lower())
            else:
                logger.warning(
                    "no link provided for trigger ID {}, so we ignore it".format(trigger_id))
                status = True
        else:
            logger.critical(
                "no token provided for trigger ID {}".format(trigger_id))
            status = False

        return status

    def auth(self, request):
        """
            let's auth the user to the Service
            :param request: request object
            :return: callback url
            :rtype: string that contains the url to redirect after auth
 
        """
        service = UserService.objects.get(user=request.user, name='ServiceWallabag')
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

    def refresh_token(self):
        """
            refresh the expired token
            :return: boolean
        """
        params = {'username': self.service_username,
                  'password': self.service_password,
                  'client_id': self.service_client_id,
                  'client_secret': self.service_client_secret}
        return Wall.get_token(host=self.service_host, **params)
