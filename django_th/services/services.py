# -*- coding: utf-8 -*-


class ServicesMgr(object):

    name = ''
    title = ''
    body = ''
    data = {}

    class __ServicesMgr:
        def __init__(self, arg):
            self.val = arg

        def __str__(self):
            return repr(self) + self.val

    instance = None

    def __init__(self, arg):
        if not ServicesMgr.instance:
            ServicesMgr.instance = ServicesMgr.__ServicesMgr(arg)
        else:
            ServicesMgr.instance.val = arg

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __str__(self):
        return "%s" % self.name

    def _get_content(self, data, which_content):
        """
            get the content that could be hidden
            in the middle of "content" or "summary detail"
            from the data of the provider
        """
        content = ''
        if which_content in data:
            if type(data[which_content]) is list or\
               type(data[which_content]) is tuple or\
               type(data[which_content]) is dict:
                if 'value' in data[which_content][0]:
                    content = data[which_content][0].value
            else:
                if type(data[which_content]) is str:
                    content = data[which_content]
                else:
                    # if not str or list or tuple
                    # or dict it could be feedparser.FeedParserDict
                    # so get the item value
                    content = data[which_content]['value']
        return content

    def set_title(self, data):
        """
            handle the title from the data
        """
        title = ''
        title = (data['title'] if 'title' in data else data['link'])

        return title

    def set_content(self, data):
        """
            handle the content from the data
        """
        content = ''
        content = self._get_content(data, 'content')

        if content == '':
            content = self._get_content(data, 'summary_detail')

        if content == '':
            if 'description' in data:
                content = data['description']

        return content

    def process_data(self):
        """
            used to get data from the service
        """
        pass

    def save_data(self):
        """
            used to save data to the service
        """
        pass


    def auth(self):
        """
            get the auth of the services
        """
        pass

