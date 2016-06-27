# coding: utf-8
import arrow

# evernote API
from evernote.api.client import EvernoteClient
from evernote.edam.notestore import NoteStore
import evernote.edam.type.ttypes as Types
from evernote.edam.error.ttypes import EDAMSystemException
from evernote.edam.error.ttypes import EDAMErrorCode

# django classes
from django.conf import settings
from django.utils.log import getLogger
from django.core.cache import caches

# django_th classes
from django_th.services.services import ServicesMgr
from django_th.models import UserService, ServicesActivated
from th_evernote.models import Evernote
from th_evernote.evernote_mgr import create_note, set_notebook, get_notebook, \
    set_header, set_tag, get_tag, set_note_attribute, set_note_footer
from th_evernote.sanitize import sanitize

"""
    handle process with evernote
    put the following in settings.py

    TH_EVERNOTE = {
        'sandbox': True,
        'consumer_key': 'abcdefghijklmnopqrstuvwxyz',
        'consumer_secret': 'abcdefghijklmnopqrstuvwxyz',
    }
    sanbox set to True to make your test and False for production purpose

    TH_SERVICES = (
        ...
        'th_evernote.my_evernote.ServiceEvernote',
        ...
    )
"""

logger = getLogger('django_th.trigger_happy')

cache = caches['th_evernote']


class ServiceEvernote(ServicesMgr):

    def __init__(self, token=None, **kwargs):
        super(ServiceEvernote, self).__init__(token, **kwargs)
        self.sandbox = settings.TH_EVERNOTE['sandbox']
        self.consumer_key = settings.TH_EVERNOTE['consumer_key']
        self.consumer_secret = settings.TH_EVERNOTE['consumer_secret']
        self.token = token
        self.service = 'ServiceEvernote'
        self.oauth = 'oauth1'

        kwargs = {'consumer_key': self.consumer_key,
                  'consumer_secret': self.consumer_secret,
                  'sandbox': self.sandbox}

        if self.token:
            kwargs = {'token': token, 'sandbox': self.sandbox}

        self.client = EvernoteClient(**kwargs)

    def read_data(self, **kwargs):
        """
            get the data from the service

            :param kwargs: contain keyword args : trigger_id at least
            :type kwargs: dict

            :rtype: list
        """
        date_triggered = kwargs.get('date_triggered')
        trigger_id = kwargs.get('trigger_id')

        kwargs['model_name'] = 'Evernote'

        trigger = super(ServiceEvernote, self).read_data(**kwargs)

        data = []
        new_date_triggered = arrow.get(str(date_triggered)[:-6],
                                       'YYYY-MM-DD HH:mm:ss')
        new_date_triggered = str(new_date_triggered).replace(
            ':', '').replace('-', '').replace(' ', '')
        date_filter = "created:{} ".format(new_date_triggered[:-6])

        notebook_filter = ''
        if trigger.notebook:
            notebook_filter = "notebook:{} ".format(trigger.notebook)
        tag_filter = "tag:{} ".format(trigger.tag) if trigger.tag != '' else ''

        complet_filter = ''.join((notebook_filter, tag_filter, date_filter))

        # filter
        my_filter = NoteStore.NoteFilter()
        my_filter.words = complet_filter

        spec = NoteStore.NotesMetadataResultSpec()
        spec.includeTitle = True
        spec.includeAttributes = True

        note_store = self.client.get_note_store()
        our_note_list = note_store.findNotesMetadata(self.token,
                                                     my_filter,
                                                     0,
                                                     100,
                                                     spec)

        for note in our_note_list.notes:
            whole_note = note_store.getNote(self.token,
                                            note.guid,
                                            True,
                                            True,
                                            False,
                                            False)
            content = self._cleaning_content(whole_note.content)
            data.append(
                {'title': note.title,
                 'my_date': arrow.get(note.created),
                 'link': whole_note.attributes.sourceURL,
                 'content': content})

        cache.set('th_evernote_' + str(trigger_id), data)

        return data

    def save_data(self, trigger_id, **data):
        """
            let's save the data
            don't want to handle empty title nor content
            otherwise this will produce an Exception by
            the Evernote's API

            :param trigger_id: trigger ID from which to save data
            :param data: the data to check to be used and save
            :type trigger_id: int
            :type data:  dict
            :return: the status of the save statement
            :rtype: boolean
        """
        kwargs = {}
        # set the title and content of the data
        title, content = super(ServiceEvernote, self).save_data(trigger_id,
                                                                data,
                                                                **kwargs)

        if len(title):
            # get the evernote data of this trigger
            trigger = Evernote.objects.get(trigger_id=trigger_id)
            # initialize notestore process
            note_store = self._notestore(trigger_id, data)
            if note_store is False:
                return False
            # note object
            note = self._notebook(trigger, note_store)
            # its attributes
            note = self._attributes(note, data)
            # its footer
            content = self._footer(trigger, data, content)
            # its title
            note.title = title if len(title) <= 255 else title[:255]
            # its content
            note = self._content(note, content)
            # create a note
            return create_note(note_store, note, trigger_id, data)

        else:
            logger.critical("no title provided "
                            "for trigger ID {}".format(trigger_id))
            return False

    def _notestore(self, trigger_id, data):
        try:
            note_store = self.client.get_note_store()
            return note_store
        except EDAMSystemException as e:
            # rate limit reach have to wait 1 hour !
            if e.errorCode == EDAMErrorCode.RATE_LIMIT_REACHED:
                logger.warn("Rate limit reached {code}\n"
                            "Retry your request in {msg} seconds\n"
                            "Data set to cache again until"
                            " limit reached".format(code=e.errorCode,
                                                    msg=e.rateLimitDuration)
                            )
                cache.set('th_evernote_' + str(trigger_id),
                          data,
                          version=2)
                return True
            else:
                logger.critical(e)
                return False
        except Exception as e:
            logger.critical(e)
            return False

    @staticmethod
    def _notebook(trigger, note_store):
        """
        :param trigger: trigger object
        :param note_store: note_store object
        :return: note object
        """
        note = Types.Note()
        if trigger.notebook:
            # get the notebookGUID ...
            notebook_id = get_notebook(note_store, trigger.notebook)
            # create notebookGUID if it does not exist then return its id
            note.notebookGuid = set_notebook(note_store,
                                             trigger.notebook,
                                             notebook_id)

            if trigger.tag:
                # ... and get the tagGUID if a tag has been provided
                tag_id = get_tag(note_store, trigger.tag)
                if tag_id is False:
                    tag_id = set_tag(note_store, trigger.tag, tag_id)
                    # set the tag to the note if a tag has been provided
                    note.tagGuids = tag_id

            logger.debug("notebook that will be used %s", trigger.notebook)
        return note

    @staticmethod
    def _attributes(note, data):
        """
        attribute of the note
        :param note: note object
        :param data:
        :return:
        """
        # attribute of the note: the link to the website
        note_attribute = set_note_attribute(data)
        if note_attribute:
            note.attributes = note_attribute
        return note

    @staticmethod
    def _footer(trigger, data, content):
        """
        footer of the note
        :param trigger: trigger object
        :param data: data to be used
        :param content: add the footer of the note to the content
        :return: content string
        """
        # footer of the note
        footer = set_note_footer(data, trigger)
        content += footer
        return content

    @staticmethod
    def _content(note, content):
        """
        content of the note
        :param note: note object
        :param content: content string to make the main body of the note
        :return:
        """
        note.content = set_header()
        note.content += sanitize(content)
        return note

    def get_evernote_client(self, token=None):
        """
            get the token from evernote
        """
        if token:
            return EvernoteClient(
                token=token,
                sandbox=self.sandbox)
        else:
            return EvernoteClient(
                consumer_key=self.consumer_key,
                consumer_secret=self.consumer_secret,
                sandbox=self.sandbox)

    def auth(self, request):
        """
            let's auth the user to the Service
        """
        client = self.get_evernote_client()
        request_token = client.get_request_token(
            self.callback_url(request))

        # Save the request token information for later
        request.session['oauth_token'] = request_token['oauth_token']
        request.session['oauth_token_secret'] = request_token[
            'oauth_token_secret']

        # Redirect the user to the Evernote authorization URL
        # return the URL string which will be used by redirect()
        # from the calling func
        return client.get_authorize_url(request_token)

    def callback(self, request, **kwargs):
        """
            Called from the Service when the user accept to activate it
        """
        try:
            client = self.get_evernote_client()
            # finally we save the user auth token
            # As we already stored the object ServicesActivated
            # from the UserServiceCreateView now we update the same
            # object to the database so :
            # 1) we get the previous object
            us = UserService.objects.get(
                user=request.user,
                name=ServicesActivated.objects.get(name='ServiceEvernote'))
            # 2) then get the token
            us.token = client.get_access_token(
                request.session['oauth_token'],
                request.session['oauth_token_secret'],
                request.GET.get('oauth_verifier', '')
            )
            # 3) and save everything
            us.save()
        except KeyError:
            return '/'

        return 'evernote/callback.html'

    @staticmethod
    def _cleaning_content(data):

        data = data.replace(
            '<?xml version="1.0" encoding="UTF-8"?>\n<'
            '!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
            '\n<en-note>', '')
        data = data.replace('</en-note>', '')

        return data
