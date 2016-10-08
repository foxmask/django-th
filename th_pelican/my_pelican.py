# coding: utf-8
import arrow

from slugify import slugify

# django classes
from django.conf import settings
from django.utils.log import getLogger

# django_th classes
from django_th.services.services import ServicesMgr
from django_th.tools import to_datetime

"""
    TH_SERVICES = (
        ...
        'th_pelican.my_pelican.ServicePelican',
        ...
    )
"""

logger = getLogger('django_th.trigger_happy')


class ServicePelican(ServicesMgr):
    """
        Service Pelican
    """
    def __init__(self, token=None, **kwargs):
        super(ServicePelican, self).__init__(token, **kwargs)
        self.AUTHOR = settings.TH_PELICAN_AUTHOR \
            if settings.TH_PELICAN_AUTHOR else ''

    def _create_content(self, site_title, content, pelican_path, url, **data):
        """
            create the file in the 'content' directory of pelican
            :param content: the content of the post
            :param pelican_path: where the files are created
            :param url: url of the datasource
            :param data: the data to check to be used and save
            :type content: string
            :type pelican_path: string
            :type url: string
            :type data:  dict
            :return: the status of the save statement
            :rtype: boolean
        """
        published = to_datetime(data)

        category = data.get('category') if data.get('category') else ''
        tags = data.get('tags') if data.get('tags') else ''

        filename = self._set_filename(data.get('title'), pelican_path)

        full_content = self._set_full_content(site_title, data.get('title'),
                                              published, content, url,
                                              category, tags)

        try:
            with open(filename, 'w') as f:
                f.write(full_content)
            status = True
        except Exception as e:
            logger.critical(e)
            status = False

        return status

    @staticmethod
    def _set_filename(title, pelican_path):
        """
            build the filename
            :param title: the title of the post
            :param pelican_path: where the files are created
            :type title: string
            :type pelican_path: string
            :return: the filename
            :rtype: string
        """
        # cleaning the special char
        name = title.replace('/', '_').replace('\\', '_').\
            replace(' ', '_').replace(':', '_').replace('&', '').\
            replace('?', '').replace('!', '')

        return "{}/{}.html".format(pelican_path, name)

    def _set_full_content(self, site_title, title, published,
                          content, url, category='', tags=''):
        """
            generate the full content of the file
            create the file in the 'content' directory of pelican
            :param site_title: title of the website
            :param title: the title of the post
            :param content: the content of the post
            :param published: the date when the data
            has been published by the provider
            :param url: url of the datasource
            :param category: category of this data
            :type site_title: string
            :type title: string
            :type content: string
            :type published: string
            :type url: string
            :param category: string
            :return: the the complet content
            :rtype: string
        """

        header = self._set_meta(title, published, category, tags)
        content = self._set_content(content)
        footer = self._set_footer(url, site_title)

        full_content = self._set_html_begin() + self._set_title(title)
        full_content += header + content + footer + self._set_html_end()

        return full_content

    def _set_meta(self, title, published, category='', tags=''):
        """
            the header

            :param title: the title of the post
            :param published: the date when the data
            has been published by the provider
            :param category: category of this data
            :param tags: the tags
            :type title: string
            :type published: string
            :param category: string
            :param tags: string
            :return: the complet head
            :rtype: string
        """
        slug_published = slugify(arrow.get(published).format(
            'YYYY-MM-DD HH:mm'))
        slug_title = slugify(title)

        header = '\n\t\t<meta name="date" content="{}" />\n'.format(published)
        if tags:
            header += '\t\t<meta name="tags" content="{}" />\n'.format(tags)
        if category:
            header += '\t\t<meta name="category" content="{}" />\n'.format(
                category)
        if self.AUTHOR:
            header += '\t\t<meta name="authors" content="{}" />\n'.format(
                self.AUTHOR)
        header += '\t\t<meta name="slug" content="{}"/>\n'.format(
            slug_published + '-' + slug_title)
        header += '\t</head>'

        return header

    @staticmethod
    def _set_title(title):
        """
            the title of the Article
            :param title: the title of the post
            :type title: string
            :return: the title
            :rtype: string
        """
        return "\t<head>\n\t\t<title>{}</title>".format(title)

    @staticmethod
    def _set_content(content):
        """
            the body of the article
            :param content: the content
            :param content: string
            :return: the complet content
            :rtype: string
        """
        return "\n\t<body>{}".format(content)

    @staticmethod
    def _set_footer(url, name):
        """
            Footer of the article
            that displays what website provided
            the article
            :param url: string of the source
            :param name: name of the source
            :return: the complet footer
            :rtype: string
        """
        provided = "\t\t<p><em><a href='{}'>Provided by {}</a>" \
                   "</em></p>\n\t</body>"
        return provided.format(url, name)

    @staticmethod
    def _set_html_begin():
        """
           start the html page
        """
        return "<html>\n"

    @staticmethod
    def _set_html_end():
        """
           close the html page
        """
        return "\n</html>"

    def save_data(self, trigger_id, **data):
        """
            let's save the data
            :param trigger_id: trigger ID from which to save data
            :param data: the data to check to be used and save
            :type trigger_id: int
            :type data: dict
            :return: the status of the save statement
            :rtype: boolean
        """
        from th_pelican.models import Pelican

        title, content = super(ServicePelican, self).save_data(
            trigger_id, **data)

        trigger = Pelican.objects.get(trigger_id=trigger_id)

        params = {'tags': trigger.tags.lower(),
                  'category': trigger.category.lower()}

        if 'tags' in data:
            del data['tags']

        params.update(data)

        if self._create_content(trigger.title, content, trigger.path,
                                trigger.url, **params):
            sentence = 'pelican {} created'
            status = True
        else:
            sentence = 'pelican {} not created'
            status = False
        logger.debug(sentence.format(title))

        return status
