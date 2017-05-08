from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from th_twitter.api import views

urlpatterns = [
    url(r'', views.tweet,)
]

urlpatterns = format_suffix_patterns(urlpatterns)
