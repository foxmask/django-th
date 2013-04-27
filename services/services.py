# -*- coding: utf-8 -*-


class ServicesMgr(object):

    name = ''
    title = ''
    body = ''
    data = {}

    def __unicode__(self):
        return "%s" % (self.name)

    def get_title(self):
        pass

    def get_body(self):
        pass

    def process_data(self):
        pass

    def save_data(self):
        pass

    def auth(self):
        """
            get the auth of the services
        """
        pass
