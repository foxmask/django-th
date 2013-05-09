# -*- coding: utf-8 -*-


class ServicesMgr(object):

    name = ''
    title = ''
    body = ''
    data = {}

    def __unicode__(self):
        return "%s" % (self.name)

    def set_title(self, string):
        self.title = string

    def set_body(self, string):
        self.body = string

    def get_title(self):
        return self.title

    def get_body(self):
        return self.body

    def process_data(self):
        pass

    def save_data(self):
        pass

    def auth(self):
        """
            get the auth of the services
        """
        pass
