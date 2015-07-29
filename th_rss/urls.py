from django.conf.urls import url
from th_rss.gen_feeds import MyRssFeeds

urlpatterns = [
    url(r'^(?P<uuid>[A-Za-z-0-9]{8}-[A-Za-z-0-9]{4}-[A-Za-z-0-9]{4}-[A-Za-z-0-9]{4}-[A-Za-z-0-9]{12})/$', MyRssFeeds.as_view()),
]