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

    def set_title(self, string):
        self.title = string

    def set_body(self, string):
        self.body = string

    def get_title(self):
        return self.title

    def get_body(self):
        return self.body

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
