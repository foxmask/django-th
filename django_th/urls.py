from django.conf.urls import include, url
from django.conf import settings
from django_th.forms.wizard import DummyForm, ProviderForm
from django_th.forms.wizard import ConsumerForm, ServicesDescriptionForm

from django_th.views import TriggerListView, TriggerDeleteView
from django_th.views import TriggerUpdateView, TriggerEditedTemplateView
from django_th.views import TriggerDeletedTemplateView
from django_th.views_fbv import trigger_switch_all_to, trigger_edit
from django_th.views_fbv import trigger_on_off, fire_trigger
from django_th.views_fbv import service_related_triggers_switch_to
from django_th.views_fbv import logout_view

from django_th.views_userservices import UserServiceListView
from django_th.views_userservices import UserServiceCreateView
from django_th.views_userservices import UserServiceUpdateView
from django_th.views_userservices import UserServiceDeleteView
from django_th.views_userservices import renew_service
from django_th.views_wizard import UserServiceWizard
from django_th.views_wizard import finalcallback

from django_js_reverse.views import urls_js


from django.contrib import admin
admin.autodiscover()

urlpatterns = [
             url(r'^jsreverse/$', urls_js, name='js_reverse'),
             # ****************************************
             # admin module
             # ****************************************
             url(r'^admin/', include(admin.site.urls)),
             # ****************************************
             # auth module
             # ****************************************
             url(r'^auth/', include('django.contrib.auth.urls')),
             # ****************************************
             # customized logout action
             # ****************************************
             url(r'^logout/$', logout_view, name='logout'),

             # ****************************************
             # trigger happy module
             # ****************************************
             url(r'^th/$', TriggerListView.as_view(),
                 name='base'),
             url(r'^th/trigger/filter_by/(?P<trigger_filtered_by>[a-zA-Z]+)$',
                 TriggerListView.as_view(),
                 name='trigger_filter_by'),
             url(r'^th/trigger/order_by/(?P<trigger_ordered_by>[a-zA-Z_]+)$',
                 TriggerListView.as_view(),
                 name='trigger_order_by'),
             url(r'^th/trigger/$', TriggerListView.as_view(),
                 name='home'),
             # ****************************************
             # * trigger
             # ****************************************
             url(r'^th/trigger/delete/(?P<pk>\d+)$',
                 TriggerDeleteView.as_view(),
                 name='delete_trigger'),
             url(r'^th/trigger/edit/(?P<pk>\d+)$',
                 TriggerUpdateView.as_view(),
                 name='edit_trigger'),
             url(r'^th/trigger/editprovider/(?P<trigger_id>\d+)$',
                 trigger_edit, {'edit_what': 'Provider'},
                 name='edit_provider'),
             url(r'^th/trigger/editconsumer/(?P<trigger_id>\d+)$',
                 trigger_edit, {'edit_what': 'Consumer'},
                 name='edit_consumer'),
             url(r'^th/trigger/edit/thanks',
                 TriggerEditedTemplateView.as_view(),
                 name="trigger_edit_thanks"),
             url(r'^th/trigger/delete/thanks',
                 TriggerDeletedTemplateView.as_view(),
                 name="trigger_delete_thanks"),
             url(r'^th/trigger/onoff/(?P<trigger_id>\d+)$',
                 trigger_on_off,
                 name="trigger_on_off"),
             url(r'^th/trigger/all/(?P<switch>(on|off))$',
                 trigger_switch_all_to,
                 name="trigger_switch_all_to"),
             # ****************************************
             # * service
             # ****************************************
             url(r'^th/service/$', UserServiceListView.as_view(),
                 name='user_services'),
             url(r'^th/service/(?P<action>\w+)$',
                 UserServiceListView.as_view(),
                 name='user_services'),
             url(r'^th/service/add/$', UserServiceCreateView.as_view(),
                 name='add_service'),
             url(r'^th/service/edit/(?P<pk>\d+)$',
                 UserServiceUpdateView.as_view(),
                 name='edit_service'),
             url(r'^th/service/delete/(?P<pk>\d+)$',
                 UserServiceDeleteView.as_view(),
                 name='delete_service'),
             url(r'^th/service/renew/(?P<pk>\d+)$',
                 renew_service,
                 name="renew_service"),
             url(r'^th/service/delete/$',
                 UserServiceDeleteView.as_view(),
                 name='delete_service'),
             url(r'^th/service/onoff/(?P<user_service_id>\d+)/(?P<switch>'
                 r'(on|off))$',
                 service_related_triggers_switch_to,
                 name="service_related_triggers_switch_to"),
             # ****************************************
             # wizard
             # ****************************************
             url(r'^th/service/create/$',
                 UserServiceWizard.as_view([ProviderForm,
                                            DummyForm,
                                            ConsumerForm,
                                            DummyForm,
                                            ServicesDescriptionForm]),
                 name='create_service'),
             # every service will use django_th.views.finalcallback
             # and give the service_name value to use to
             # trigger the real callback
             url(r"^th/callbackevernote/$",
                 finalcallback,
                 {'service_name': 'ServiceEvernote', },
                 name="evernote_callback",
                 ),
             url(r"^th/callbackgithub/$",
                 finalcallback,
                 {'service_name': 'ServiceGithub', },
                 name="github_callback",
                 ),
             url(r"^th/callbackpocket/$",
                 finalcallback,
                 {'service_name': 'ServicePocket', },
                 name="pocket_callback",
                 ),
             url(r"^th/callbackpushbullet/$",
                 finalcallback,
                 {'service_name': 'ServicePushbullet', },
                 name="pushbullet_callback",
                 ),
             url(r"^th/callbackreddit/$",
                 finalcallback,
                 {'service_name': 'ServiceReddit', },
                 name="reddit_callback",
                 ),
             url(r"^th/callbacktodoist/$",
                 finalcallback,
                 {'service_name': 'ServiceTodoist', },
                 name="todoist_callback",
                 ),
             url(r"^th/callbacktrello/$",
                 finalcallback,
                 {'service_name': 'ServiceTrello', },
                 name="trello_callback",
                 ),
             url(r"^th/callbacktumblr/$",
                 finalcallback,
                 {'service_name': 'ServiceTumblr', },
                 name="tumblr_callback",
                 ),
             url(r"^th/callbacktwitter/$",
                 finalcallback,
                 {'service_name': 'ServiceTwitter', },
                 name="twitter_callback",
                 ),
             url(r"^th/callbackwallabag/$",
                 finalcallback,
                 {'service_name': 'ServiceWallabag', },
                 name="wallabag_callback",
                 ),
             url(r"^th/callbackmastodon/$",
                 finalcallback,
                 {'service_name': 'ServiceMastodon', },
                 name="mastodon_callback",
                 ),
             url(r'^th/myfeeds/', include('th_rss.urls')),

             url(r'^th/api/taiga/webhook/', include('th_taiga.urls')),
             url(r'^th/api/slack/webhook/', include('th_slack.urls'))
             ]

if settings.DJANGO_TH.get('fire'):
    urlpatterns += url(r'^th/trigger/fire/(?P<trigger_id>\d+)$',
                       fire_trigger, name="fire_trigger"),
