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

    TH_WALLABAG = {
        'client_id' = 'abcdefghijklmnopqrstuvwxyz'
        'client_secret' = 'abcdefghijklmnopqrstuvwxyz'
        'username' = 'jane'
        'password' = 'doe'
    }
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
        trigger_id = kwargs['trigger_id']
        cache.set('th_wallabag_' + str(trigger_id), data)

    def process_data(self, **kwargs):
        """
            get the data from the cache
            :param trigger_id: trigger ID from which to save data
            :type trigger_id: int
        """
        kw = {'cache_stack': 'th_wallabag',
              'trigger_id': str(kwargs['trigger_id'])}
        return super(ServiceWallabag, self).process_data(**kw)

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
        from th_wallabag.models import Wallabag

        status = False

        if self.token and 'link' in data and data['link'] is not None\
                and len(data['link']) > 0:
            # get the data of this trigger
            trigger = Wallabag.objects.get(trigger_id=trigger_id)

            title = self.set_title(data)
            # convert htmlentities
            title = HtmlEntities(title).html_entity_decode

            try:
                self.wall.post_entries(url=data['link'], title=title, tags=(trigger.tag.lower()))

                sentence = str('wallabag {} created').format(data['link'])
                logger.debug(sentence)
                status = True
            except Exception as e:
                if e.errno == 401:
                    new_token = self.refresh_token()
                    old_token = self.token
                    UserService.objects.filter(token=old_token, name='ServiceWallabag').update(token=new_token)

                    # new wallabag session with new token
                    new_wall = Wall(host=self.service_host,
                                    client_secret=self.service_client_secret,
                                    client_id=self.service_client_id,
                                    token=new_token)
                    try:
                        return new_wall.post_entries(url=data['link'], title=title, tags=(trigger.tag.lower()))
                    except Exception as e:
                        logger.critical(e.errno, e.strerror)
                        status = False
                else:
                    logger.critical(e.errno, e.strerror)
                    status = False

        else:
            logger.critical(
                "no token or link provided for trigger ID {} ".format(trigger_id))
            status = False
        return status

    def auth(self, request):
        """
            let's auth the user to the Service
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
            # finally we save the user auth token
            # As we already stored the object ServicesActivated
            # from the UserServiceCreateView now we update the same
            # object to the database so :
            # 1) we get the previous objet
            us = UserService.objects.get(
                user=request.user,
                name=ServicesActivated.objects.get(name='ServiceWallabag'))
            # 2) Readability API require to use 4 params consumer_key/secret +
            # token_key/secret instead of usually get just the token
            # from an access_token request. So we need to add a string
            # separator for later use to split on this one
            us.token = request.session['oauth_token']
            # 3) and save everything
            us.save()
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
