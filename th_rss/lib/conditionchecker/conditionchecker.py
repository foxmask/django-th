# -*- coding: utf-8 -*-

__all__ = ['Condition']


class Condition(object):
    '''
        class Condition permits to reduce the size of the data to return
        by applying a rule of filtering
    '''

    def __init__(self, **kwargs):
        '''
            set the 2 filters type : match and does_not_match
        '''
        if 'does_not_match' in kwargs:
            self.does_not_match = kwargs['does_not_match']

        if 'match' in kwargs:
            self.match = kwargs['match']

    def check(self, datas, *filers):
        '''
            this method permits to reduce the quantity of information to read
            by applying some filtering
            here '*filers' can receive a list of properties to be filtered
        '''
        # special case : no filter : want to read all the feed
        if self.match == "" and self.does_not_match == '':
            yield datas
        # let's filtering :
        else:
            condition1 = False
            condition2 = False
            # arg contain the property from which we want to check the 'data'
            for prop in filers:
                # check if my datas contains my property
                if prop in datas:
                    # filter to find only this data
                    if self.match != '' and condition1 is False:
                        condition1 = self.filter_that(self.match,
                                                      datas[prop])
                    # filter to exclude this data,
                    # when found, continue to the next entry
                    if self.does_not_match != '' and condition2 is False:
                        condition2 = self.filter_that(self.does_not_match,
                                                      datas[prop])
                        if condition2:
                            continue
        if condition1 and condition2 is False:
            yield datas

    def filter_that(self, criteria, data):
        '''
            this method just use the module 're' to check if the data contain
            the string to find
        '''
        import re
        prog = re.compile(criteria)

        return True if prog.match(data) else False
