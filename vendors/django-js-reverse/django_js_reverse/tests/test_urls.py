#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include


pattern_ns_1 = patterns('',
                        url(r'^ns1_1/$', 'foo', name='ns1_1'),
                        url(r'^ns1_2/$', 'foo', name='ns1_2'))

pattern_ns_2 = patterns('',
                        url(r'^ns2_1/$', 'foo', name='ns2_1'),
                        url(r'^ns2_2/$', 'foo', name='ns2_2'))

pattern_ns = patterns('',
                      url(r'^ns1/$', include(pattern_ns_1,  namespace='ns1')),
                      url(r'^ns2/$', include(pattern_ns_2,  namespace='ns2')))

urlpatterns = patterns('',
                       url(r'^jsreverse/$', 'django_js_reverse.views.urls_js', name='js_reverse'),

                       # test urls
                       url(r'^test_no_url_args/$', 'foo',
                           name='test_no_url_args'),
                       url(r'^test_one_url_args/(?P<arg_one>[-\w]+)/$', 'foo',
                           name='test_one_url_args'),
                       url(r'^test_two_url_args/(?P<arg_one>[-\w]+)-(?P<arg_two>[-\w]+)/$', 'foo',
                           name='test_two_url_args'),
                       url(r'^test_unicode_url_name/$', 'foo',
                           name=u'test_unicode_url_name'),
                       # test namespace
                       url(r'^ns/$', include(pattern_ns_2,  namespace='ns2'))
)