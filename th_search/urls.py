from django.conf.urls import patterns, url

from th_search.views import TriggerHappySearchView

urlpatterns = patterns('',
                       url(r"^$",
                           TriggerHappySearchView.as_view(),
                           name='haystack_search'),)
