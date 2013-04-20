# -*- coding: utf-8 -*-


class ThServices(object):

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
