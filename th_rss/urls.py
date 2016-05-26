from django.conf.urls import url
from th_rss.views import MyRssFeeds, MyRssFeed

urlpatterns = [
    url(r'^(?P<uuid>[A-Za-z-0-9]{8}-[A-Za-z-0-9]{4}-[A-Za-z-0-9]{4}-'
        r'[A-Za-z-0-9]{4}-[A-Za-z-0-9]{12})/$',
        MyRssFeed.as_view(),
        name="my_feed"),
    url(r'^$', MyRssFeeds.as_view(), name="my_feeds"),
]
