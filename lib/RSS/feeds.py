#!/usr/bin/python
# -*- coding: utf-8 -*-
import feedparser
import re


def get_feeds(url_to_parse, condition):

    """
    return  feed from a given url with condition(s)
    >>> get_feeds("PyPI_Newest_Packages.rss",{'match': 'django', 'does_not_match': 'UNKNOWN'}) # doctest: +ELLIPSIS    
    <generator object get_feeds at 0x...>
    """
    datas = feedparser.parse(url_to_parse)

    # want too read all the feed with no filter
    if condition['match'] == "" and condition['does_not_match'] == '':
        for entry in datas.entries:
            yield entry
    # need to filter something
    else:
        if condition['match'] != '':
            pattern = condition['match']
            prog = re.compile(pattern)

        if condition['does_not_match'] != '':
            pattern2 = condition['does_not_match']
            prog2 = re.compile(pattern2)

        for entry in datas.entries:

            cond1 = False
            if condition['match'] != '':
                match = prog.match(entry['title'])
                if match:
                    cond1 = True
            if not cond1:
                match = prog.match(entry['description'])
                if match:
                    cond1 = True

            cond2 = False
            if condition['does_not_match'] != '':
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

if __name__ == "__main__":
    import doctest
    doctest.testmod()
