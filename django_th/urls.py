from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from django_th.forms.wizard import DummyForm, ProviderForm, ConsumerForm, ServicesDescriptionForm

from django_th.views import TriggerListView, TriggerDeleteView, TriggerUpdateView, TriggerEditedTemplateView, MeUpdate
from django_th.views import TriggerDeletedTemplateView, me
from django_th.views_fbv import trigger_switch_all_to, trigger_edit, trigger_on_off, fire_trigger
from django_th.views_fbv import service_related_triggers_switch_to

from django_th.views_userservices import UserServiceListView, UserServiceCreateView, UserServiceUpdateView
from django_th.views_userservices import UserServiceDeleteView, renew_service
from django_th.views_wizard import UserServiceWizard, finalcallback

from django_js_reverse.views import urls_js

urlpatterns = [
    path('jsreverse/', urls_js, name='js_reverse'),

    # ****************************************
    # admin module
    # ****************************************
    path('admin/', admin.site.urls),
    # ****************************************
    # profil
    # ****************************************
    path(r'me/', me, name='me'),
    path(r'me/edit/', MeUpdate.as_view(), name='edit_me'),

    # ****************************************
    # auth module
    # ****************************************
    path(
        'auth/password_change/',
        auth_views.PasswordChangeView.as_view(template_name='auth/change_password.html'),
    ),
    path(
        'auth/password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(template_name='auth/password_change_done.html'),
    ),
    path('auth/', include('django.contrib.auth.urls')),

    # ****************************************
    # trigger happy module
    # ****************************************
    path('th/', TriggerListView.as_view(), name='base'),
    url(r'^th/trigger/filter_by/(?P<trigger_filtered_by>[a-zA-Z]+)$', TriggerListView.as_view(),
        name='trigger_filter_by'),
    url(r'^th/trigger/order_by/(?P<trigger_ordered_by>[a-zA-Z_]+)$', TriggerListView.as_view(),
        name='trigger_order_by'),
    path('th/trigger/', TriggerListView.as_view(), name='home'),
    # ****************************************
    # * trigger
    # ****************************************
    url(r'^th/trigger/delete/(?P<pk>\d+)$', TriggerDeleteView.as_view(), name='delete_trigger'),
    url(r'^th/trigger/edit/(?P<pk>\d+)$', TriggerUpdateView.as_view(), name='edit_trigger'),
    path('th/trigger/editprovider/<int:trigger_id>', trigger_edit, {'edit_what': 'Provider'}, name='edit_provider'),
    path('th/trigger/editconsumer/<int:trigger_id>', trigger_edit, {'edit_what': 'Consumer'}, name='edit_consumer'),
    path('th/trigger/edit/thanks', TriggerEditedTemplateView.as_view(), name="trigger_edit_thanks"),
    path('th/trigger/delete/thanks', TriggerDeletedTemplateView.as_view(), name="trigger_delete_thanks"),
    path('th/trigger/onoff/<int:trigger_id>', trigger_on_off, name="trigger_on_off"),
    url(r'^th/trigger/all/(?P<switch>(on|off))$', trigger_switch_all_to, name="trigger_switch_all_to"),
    # ****************************************
    # * service
    # ****************************************
    path('th/services/', UserServiceListView.as_view(), name='user_services'),
    url(r'^th/service/add/(?P<service_name>\w+)$', UserServiceCreateView.as_view(), name='add_service'),
    url(r'^th/service/edit/(?P<pk>\d+)$', UserServiceUpdateView.as_view(), name='edit_service'),
    url(r'^th/service/delete/(?P<pk>\d+)$', UserServiceDeleteView.as_view(), name='delete_service'),
    url(r'^th/service/renew/(?P<pk>\d+)$', renew_service, name="renew_service"),
    path('th/service/delete/', UserServiceDeleteView.as_view(), name='delete_service'),
    url(r'^th/service/onoff/(?P<user_service_id>\d+)/(?P<switch>(on|off))$', service_related_triggers_switch_to,
        name="service_related_triggers_switch_to"),
    # ****************************************
    # wizard
    # ****************************************
    path('th/service/create/',
         UserServiceWizard.as_view([ProviderForm,
                                    DummyForm,
                                    ConsumerForm,
                                    DummyForm,
                                    ServicesDescriptionForm]),
         name='create_service'),
    # every service will use django_th.views.finalcallback
    # and give the service_name value to use to
    # trigger the real callback
    path("th/callbackevernote/", finalcallback, {'service_name': 'ServiceEvernote', }, name="evernote_callback",),
    path("th/callbackgithub/", finalcallback, {'service_name': 'ServiceGithub', }, name="github_callback",),
    path("th/callbackpocket/", finalcallback, {'service_name': 'ServicePocket', }, name="pocket_callback",),
    path("th/callbackpushbullet/", finalcallback, {'service_name': 'ServicePushbullet', }, name="pushbullet_callback",),
    path("th/callbackreddit/", finalcallback, {'service_name': 'ServiceReddit', }, name="reddit_callback",),
    path("th/callbacktodoist/", finalcallback, {'service_name': 'ServiceTodoist', }, name="todoist_callback",),
    path("th/callbacktrello/", finalcallback, {'service_name': 'ServiceTrello', }, name="trello_callback",),
    path("th/callbacktumblr/", finalcallback, {'service_name': 'ServiceTumblr', }, name="tumblr_callback",),
    path("th/callbacktwitter/", finalcallback, {'service_name': 'ServiceTwitter', }, name="twitter_callback",),
    path("th/callbackwallabag/", finalcallback, {'service_name': 'ServiceWallabag', }, name="wallabag_callback",),
    path("th/callbackmastodon/", finalcallback, {'service_name': 'ServiceMastodon', }, name="mastodon_callback",),
    path('th/myfeeds/', include('th_rss.urls')),

    path('th/api/taiga/webhook/', include('th_taiga.urls')),
    path('th/api/slack/webhook/', include('th_slack.urls'))
]

if settings.DJANGO_TH.get('fire'):
    urlpatterns += path('th/trigger/fire/<int:trigger_id>', fire_trigger, name="fire_trigger"),
