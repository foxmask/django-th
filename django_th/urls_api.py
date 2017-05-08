from django.conf.urls import include, url


urlpatterns = [

    url(r'^taiga/webhook/', include('th_taiga.urls')),
    url(r'^slack/webhook/', include('th_slack.urls')),

    url(r'^twitter', include('th_twitter.urls'))
]
