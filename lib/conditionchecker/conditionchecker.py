# -*- coding: utf-8 -*-
import re
__all__ = ['Condition']


class Condition(object):

    def __init__(self, **kwargs):
        if 'does_not_match' in kwargs:
            self.does_not_match = kwargs['does_not_match']
            print self.does_not_match

        if 'match' in kwargs:
            self.match = kwargs['match']
            print self.match

    def check(self, datas):
    # want too read all the feed with no filter
        if self.match == "" and self.does_not_match == '':
            for entry in datas.entries:
                yield entry
        # need to filter something
        else:
            if self.match != '':
                pattern = self.match
                prog = re.compile(pattern)

            if self.does_not_match != '':
                pattern2 = self.does_not_match
                prog2 = re.compile(pattern2)

            for entry in datas.entries:

                cond1 = False
                if self.match != '':
                    match = prog.match(entry['title'])
                if match:
                    cond1 = True
                if not cond1:
                    match = prog.match(entry['description'])
                if match:
                    cond1 = True

                cond2 = False
                if self.does_not_match != '':
                    match2 = prog2.match(entry['title'])
                if match2:
                    cond2 = True
                if not cond2:
                    match2 = prog2.match(entry['description'])
                if match2:
                    cond2 = True

                # found the does_not_match
                if cond2 and match2:
                    continue
                # if not
                elif cond1 and match:
                    yield entry
                # otherwise pass, dont need them too
                else:
                    pass
