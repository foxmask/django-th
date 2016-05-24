# coding: utf-8
import sys
import arrow

# evernote API
from evernote.api.client import EvernoteClient
from evernote.edam.notestore import NoteStore
import evernote.edam.type.ttypes as Types
from evernote.edam.error.ttypes import EDAMSystemException, EDAMUserException
from evernote.edam.error.ttypes import EDAMErrorCode

# django classes
from django.utils.translation import ugettext as _
from django.conf import settings
from django.utils.log import getLogger
from django.core.cache import caches

# django_th classes
from django_th.services.services import ServicesMgr
from django_th.models import UserService, ServicesActivated
from th_evernote.models import Evernote
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

    def __init__(self, token=None):
        super(ServiceEvernote, self).__init__(token)
        self.sandbox = settings.TH_EVERNOTE['sandbox']
        self.consumer_key = settings.TH_EVERNOTE['consumer_key']
        self.consumer_secret = settings.TH_EVERNOTE['consumer_secret']
        self.token = token

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
        # get the data from the last time the trigger has been started
        # the filter will use the DateTime format in standard
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

        # result spec to tell to evernote
        # what information to include in the response
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
            content = self.cleaning_content(whole_note.content)
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

            try:
                note_store = self.client.get_note_store()
            except EDAMSystemException as e:
                # rate limite reach have to wait 1 hour !
                if e.errorCode == EDAMErrorCode.RATE_LIMIT_REACHED:
                    sentance = "Rate limit reached {code}"
                    sentance += "Retry your request in {msg} seconds"
                    sentance += " - date set to cache again until"
                    sentance += " limit reached"
                    logger.warn(sentance.format(
                        code=e.errorCode,
                        msg=e.rateLimitDuration))
                    # put again in cache the data that could not be
                    # published in Evernote yet
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

            # note object
            note = Types.Note()
            if trigger.notebook:
                # get the notebookGUID ...
                notebook_id = self.get_notebook(note_store, trigger.notebook)
                # create notebookGUID if it does not exist then return its id
                note.notebookGuid = self.set_notebook(note_store,
                                                      trigger.notebook,
                                                      notebook_id)

                if trigger.tag:
                    # ... and get the tagGUID if a tag has been provided
                    tag_id = self.get_tag(note_store, trigger.tag)
                    if tag_id is False:
                        tag_id = self.set_tag(note_store, trigger.tag, tag_id)
                        # set the tag to the note if a tag has been provided
                        note.tagGuids = tag_id

                logger.debug("notebook that will be used %s", trigger.notebook)

            # attribute of the note: the link to the website
            note_attribute = self.set_note_attribute(data)
            if note_attribute:
                note.attributes = note_attribute

            # footer of the note
            footer = self.set_note_footer(data, trigger)
            content += footer

            note.title = title
            note.content = self.set_evernote_header()
            note.content += self.get_sanitize_content(content)
            # create a note
            return self._create_note(note_store, note, trigger_id, data)

        else:
            sentence = "no title provided for trigger ID {}"
            logger.critical(sentence.format(trigger_id))
            return False

    @staticmethod
    def get_notebook(note_store, my_notebook):
        """
            get the notebook from its name
        """
        notebook_id = 0
        notebooks = note_store.listNotebooks()
        # get the notebookGUID ...
        for notebook in notebooks:
            if notebook.name.lower() == my_notebook.lower():
                notebook_id = notebook.guid
                break
        return notebook_id

    @staticmethod
    def set_notebook(note_store, my_notebook, notebook_id):
        """
            create a notebook
        """
        if notebook_id == 0:
            new_notebook = Types.Notebook()
            new_notebook.name = my_notebook
            new_notebook.defaultNotebook = False
            notebook_id = note_store.createNotebook(new_notebook).guid

        return notebook_id

    @staticmethod
    def get_tag(note_store, my_tags):
        """
            get the tags from his Evernote account
            :param note_store Evernote Instance
            :param my_tags string
            :return: array of the tag to create
        """
        tag_id = []
        listtags = note_store.listTags()
        # cut the string by piece of tag with comma
        if ',' in my_tags:
            for my_tag in my_tags.split(','):
                for tag in listtags:
                    # remove space before and after
                    # thus we keep "foo bar"
                    # but not " foo bar" nor "foo bar "
                    if tag.name.lower() == my_tag.lower().lstrip().rstrip():
                        tag_id.append(tag.guid)
                        break
        else:
            for tag in listtags:
                if tag.name.lower() == my_tags.lower():
                    tag_id.append(tag.guid)
                    break

        return tag_id

    def set_tag(self, note_store, my_tags, tag_id):
        """
            create a tag if not exists
            :param my_tags string
            :param tag_id id of the tag(s) to create
            :return: array of the tag to create
        """
        # tagGUID does not exist:
        # create it if a tag has been provided
        new_tag = Types.Tag()
        if ',' in my_tags:
            for my_tag in my_tags.split(','):
                new_tag.name = my_tag
                tag_id.append(self._create_tag(note_store, new_tag))
        elif my_tags:
            new_tag.name = my_tags
            tag_id.append(self._create_tag(note_store, new_tag))

        return tag_id

    @staticmethod
    def _create_note(note_store, note, trigger_id, data):
        """
            create a note
            :param note_store Evernote instance
            :param note
            :param trigger_id id of the trigger
            :param data to save or to put in cache
            :type Evernote Instance
            :type note: string
            :type trigger_id: int
            :type data: dict
            :return boolean
            :rtype boolean
        """
        # create the note !
        try:
            created_note = note_store.createNote(note)
            sentance = str('note %s created') % created_note.guid
            logger.debug(sentance)
            return True
        except EDAMSystemException as e:
            if e.errorCode == EDAMErrorCode.RATE_LIMIT_REACHED:
                sentance = "Rate limit reached {code}"
                sentance += "Retry your request in {msg} seconds"
                logger.warn(sentance.format(
                    code=e.errorCode,
                    msg=e.rateLimitDuration))
                # put again in cache the data that could not be
                # published in Evernote yet
                cache.set('th_evernote_' + str(trigger_id),
                          data,
                          version=2)
                return True
            else:
                logger.critical(e)
                return False
        except EDAMUserException as e:
            if e.errorCode == EDAMErrorCode.ENML_VALIDATION:
                sentance = "Data ignored due to validation"
                sentance += " error : err {code} {msg}"
                logger.warn(sentance.format(
                    code=e.errorCode,
                    msg=e.parameter))
                return True
        except Exception as e:
            logger.critical(e)
            return False

    @staticmethod
    def _create_tag(note_store, new_tag):
        """
            :param new_tag: create this new tag
            :return: new tag id
        """
        try:
            return note_store.createTag(new_tag).guid
        except EDAMUserException as e:
            if e.errorCode == EDAMErrorCode.DATA_CONFLICT:
                logger.info("Evernote Data Conflict Err {0}".format(e))
            elif e.errorCode == EDAMErrorCode.BAD_DATA_FORMAT:
                logger.critical("Evernote Err {0}".format(e))

    @staticmethod
    def set_evernote_header():
        """
            preparing the hearder of Evernote
        """
        prolog = '<?xml version="1.0" encoding="UTF-8"?>'
        prolog += '<!DOCTYPE en-note SYSTEM \
        "http://xml.evernote.com/pub/enml2.dtd">\n'
        return prolog

    @staticmethod
    def get_sanitize_content(content):
        """
            tidy and sanitize content
        """
        enml = sanitize(content)
        # python 2
        if sys.version_info.major == 2:
            return enml.encode('ascii', 'xmlcharrefreplace')
        else:
            return str(enml)

    @staticmethod
    def set_note_attribute(data):
        """
           add the link of the 'source' in the note
           get a NoteAttributes object
        """
        na = False
        if data.get('link'):
            na = Types.NoteAttributes()
            # add the url
            na.sourceURL = data['link']
            # add the object to the note
        return na

    @staticmethod
    def set_note_footer(data, trigger):
        """
            handle the footer of the note
        """
        footer = ''
        if data.get('link'):
            provided_by = _('Provided by')
            provided_from = _('from')
            footer_from = "<br/><br/>{} <em>{}</em> {} <a href='{}'>{}</a>"

            footer = footer_from.format(
                provided_by, trigger.trigger.description, provided_from,
                data.get('link'), data.get('link'))

        return footer

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
            self.callback_url(request, 'evernote'))

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
            # 1) we get the previous objet
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
    def cleaning_content(data):

        data = data.replace('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">\n<en-note>', '')
        data = data.replace('</en-note>', '')

        return data
