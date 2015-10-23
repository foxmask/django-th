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

    # Boards own Lists own Cards

    def __init__(self, token=None):
        # app name
        self.app_name = DjangoThConfig.verbose_name
        # expiration
        self.expiry = "30days"
        # scope define the rights access
        self.scope = 'read,write'

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
        cache.set('th_trello_' + str(trigger_id), data)

    def process_data(self, trigger_id):
        """
            get the data from the cache
            :param trigger_id: trigger ID from which to save data
            :type trigger_id: int
        """
        return super(ServiceTrello, self).process_data('th_trello',
                                                       str(trigger_id))

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
        from th_trello.models import Trello

        title = ''
        content = ''
        status = False
        kwargs = {'output_format': 'md'}
        title, content = super(ServiceTrello, self).save_data(data, **kwargs)

        if len(title):
            # get the data of this trigger
            t = Trello.objects.get(trigger_id=trigger_id)
            # footer of the card
            footer = self.set_card_footer(data, t)
            content += footer

            # 1 - we need to search the list and board where we will
            # store the card so ...

            # 1.a search the board_id by its name
            # by retreiving all the boards
            boards = self.trello_instance.list_boards()

            board_id = ''
            my_board = ''
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

            sentance = str('trello {} created').format(data['link'])
            logger.debug(sentance)
            status = True
        else:
            sentance = "no token or link provided for trigger ID {}"
            logger.critical(sentance.format(trigger_id))
            status = False

        return status

    def set_card_footer(self, data, trigger):
        """
            handle the footer of the note
        """
        footer = ''
        if 'link' in data:
            provided_by = _('Provided by')
            provided_from = _('from')
            footer_from = "<br/><br/>{} <em>{}</em> {} <a href='{}'>{}</a>"

            description = trigger.trigger.description
            footer = footer_from.format(
                provided_by, description, provided_from,
                data['link'], data['link'])

        return footer

    def auth(self, request):
        """
            let's auth the user to the Service
        """
        request_token = super(ServiceTrello, self).auth(request)
        callback_url = self.callback_url(request, 'trello')

        # URL to redirect user to, to authorize your app
        auth_url_str = '{auth_url}?oauth_token={token}&scope={scope}&name={name}'
        auth_url_str += '&expiration={expiry}&oauth_callback={callback_url}'
        auth_url = auth_url_str.format(auth_url=self.AUTH_URL,
                                       token=request_token['oauth_token'],
                                       scope=self.scope,
                                       name=self.app_name,
                                       expiry=self.expiry,
                                       callback_url=callback_url)

        return auth_url

    def callback(self, request):
        """
            Called from the Service when the user accept to activate it
        """
        kwargs = {'access_token': '', 'service': 'ServiceTrello',
                  'return': 'trello'}
        return super(ServiceTrello, self).callback(request, **kwargs)


