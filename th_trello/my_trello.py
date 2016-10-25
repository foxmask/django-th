# coding: utf-8
# Trello API
from trello import TrelloClient

# django classes
from django.conf import settings
from django.utils.translation import ugettext as _
from django.utils.log import getLogger
from django.core.cache import caches

# django_th classes
from django_th.apps import DjangoThConfig
from django_th.services.services import ServicesMgr
from django_th.models import update_result

"""
    handle process with Trello
    put the following in settings.py

    TH_TRELLO = {
        'consumer_key': 'abcdefghijklmnopqrstuvwxyz',
        'consumer_secret': 'abcdefghijklmnopqrstuvwxyz',
    }

    TH_SERVICES = (
        ...
        'th_trello.my_trello.ServiceTrello',
        ...
    )

"""

logger = getLogger('django_th.trigger_happy')

cache = caches['th_trello']


class ServiceTrello(ServicesMgr):
    """
        Serivce Trello
    """
    # Boards own Lists own Cards

    def __init__(self, token=None, **kwargs):
        super(ServiceTrello, self).__init__(token, **kwargs)
        # app name
        self.app_name = DjangoThConfig.verbose_name
        # expiration
        self.expiry = "30days"
        # scope define the rights access
        self.scope = 'read,write'
        self.oauth = 'oauth1'
        self.service = 'ServiceTrello'

        base = 'https://www.trello.com'
        self.AUTH_URL = '{}/1/OAuthAuthorizeToken'.format(base)
        self.REQ_TOKEN = '{}/1/OAuthGetRequestToken'.format(base)
        self.ACC_TOKEN = '{}/1/OAuthGetAccessToken'.format(base)
        self.consumer_key = settings.TH_TRELLO['consumer_key']
        self.consumer_secret = settings.TH_TRELLO['consumer_secret']
        if token:
            token_key, token_secret = token.split('#TH#')
            self.trello_instance = TrelloClient(self.consumer_key,
                                                self.consumer_secret,
                                                token_key,
                                                token_secret)

    def read_data(self, **kwargs):
        """
            get the data from the service

            :param kwargs: contain keyword args : trigger_id at least
            :type kwargs: dict
        """
        trigger_id = kwargs.get('trigger_id')
        data = list()
        cache.set('th_trello_' + str(trigger_id), data)
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
        from th_trello.models import Trello

        data['output_format'] = 'md'
        title, content = super(ServiceTrello, self).save_data(trigger_id,
                                                              **data)

        if len(title):
            # get the data of this trigger
            t = Trello.objects.get(trigger_id=trigger_id)
            # footer of the card
            footer = self.set_card_footer(data, t)
            content += footer

            # 1 - we need to search the list and board where we will
            # store the card so ...

            # 1.a search the board_id by its name
            # by retrieving all the boards
            boards = self.trello_instance.list_boards()

            board_id = ''
            my_list = ''
            for board in boards:
                if t.board_name == board.name.decode('utf-8'):
                    board_id = board.id
                    break

            if board_id:
                # 1.b search the list_id by its name
                my_board = self.trello_instance.get_board(board_id)
                lists = my_board.open_lists()
                # just get the open list ; not all the archive ones
                for list_in_board in lists:
                    # search the name of the list we set in the form
                    if t.list_name == list_in_board.name.decode('utf-8'):
                        # return the (trello) list object
                        # to be able to add card at step 3
                        my_list = my_board.get_list(list_in_board.id)
                        break
                # we didnt find the list in that board
                # create it
                if my_list == '':
                    my_list = my_board.add_list(t.list_name)

            else:
                # 2 if board_id and/or list_id does not exist, create it/them
                my_board = self.trello_instance.add_board(t.board_name)
                # add the list that didnt exists and
                # return a (trello) list object
                my_list = my_board.add_list(t.list_name)

            # 3 create the card
            # create the Trello card
            my_list.add_card(title, content)

            sentence = str('trello {} created').format(data['link'])
            logger.debug(sentence)
            status = True
        else:
            sentence = "no token or link provided for trigger ID " \
                       "{}".format(trigger_id)
            update_result(trigger_id, msg=sentence)
            status = False

        return status

    @staticmethod
    def set_card_footer(data, trigger):
        """
            handle the footer of the note
        """
        footer = ''
        if data.get('link'):
            provided_by = _('Provided by')
            provided_from = _('from')
            footer_from = "<br/><br/>{} <em>{}</em> {} <a href='{}'>{}</a>"

            description = trigger.trigger.description
            footer = footer_from.format(
                provided_by, description, provided_from,
                data.get('link'), data.get('link'))

            import pypandoc
            footer = pypandoc.convert(footer, 'md', format='html')

        return footer

    def auth(self, request):
        """
            let's auth the user to the Service
            :param request: request object
            :return: callback url
            :rtype: string that contains the url to redirect after auth
        """
        request_token = super(ServiceTrello, self).auth(request)
        callback_url = self.callback_url(request)

        # URL to redirect user to, to authorize your app
        auth_url_str = '{auth_url}?oauth_token={token}'
        auth_url_str += '&scope={scope}&name={name}'
        auth_url_str += '&expiration={expiry}&oauth_callback={callback_url}'
        auth_url = auth_url_str.format(auth_url=self.AUTH_URL,
                                       token=request_token['oauth_token'],
                                       scope=self.scope,
                                       name=self.app_name,
                                       expiry=self.expiry,
                                       callback_url=callback_url)

        return auth_url

    def callback(self, request, **kwargs):
        """
            Called from the Service when the user accept to activate it
            :param request: request object
            :return: callback url
            :rtype: string , path to the template
        """
        return super(ServiceTrello, self).callback(request, **kwargs)
