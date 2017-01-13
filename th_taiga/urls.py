from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from th_taiga.api import views

urlpatterns = [
    url(r'(?P<trigger_id>\d+)/(?P<key>[a-zA-Z0-9-]+)$', views.taiga,)
]

urlpatterns = format_suffix_patterns(urlpatterns)
