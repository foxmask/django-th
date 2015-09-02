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
        if 'content' in data:
            if type(data['content']) is list or type(data['content']) is tuple\
               or type(data['content']) is dict:
                if 'value' in data['content'][0]:
                    content = data['content'][0].value
            else:
                if type(data['content']) is str:
                    content = data['content']
                else:
                    # if not str or list or tuple
                    # or dict it could be feedparser.FeedParserDict
                    # so get the item value
                    content = data['content']['value']

        elif 'summary_detail' in data:
            if type(data['summary_detail']) is list or\
               type(data['summary_detail']) is tuple or\
               type(data['summary_detail']) is dict:
                if 'value' in data['summary_detail'][0]:
                    content = data['summary_detail'][0].value
            else:
                if type(data['summary_detail']) is str:
                    content = data['summary_detail']
                else:
                    # if not str or list or tuple
                    # or dict it could be feedparser.FeedParserDict
                    # so get the item value
                    content = data['summary_detail']['value']

        elif 'description' in data:
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
