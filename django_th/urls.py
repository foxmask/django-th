from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from django_th.forms.wizard import DummyForm, ProviderForm, \
    ConsummerForm, ServicesDescriptionForm

from django_th.views import TriggerListView, TriggerDeleteView, \
    TriggerUpdateView, \
    TriggerEditedTemplateView, TriggerDeletedTemplateView, \
    UserServiceWizard, UserServiceListView, \
    UserServiceCreateView, UserServiceDeleteView, \
    UserServiceAddedTemplateView, UserServiceDeletedTemplateView, \
    trigger_on_off, trigger_switch_all_to, \
    trigger_edit_provider, trigger_edit_consummer, \
    renew_service

urlpatterns = \
    patterns('',
             # ****************************************
             # admin module
             # ****************************************
             # url(r'^admin/', include(admin.site.urls)),
             # ****************************************
             # auth module
             # ****************************************
             # url(r'^auth/', include('django.contrib.auth.urls')),
             # ****************************************
             # customized lgout action
             # ****************************************
             # url(r'^logout/$',
             #    'django_th.views.logout_view', name='logout'),

             # ****************************************
             # trigger happy module
             # ****************************************
             url(r'^th/$', TriggerListView.as_view(),
                 name='base'),
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
                 trigger_edit_provider,
                 name='edit_provider'),
             url(r'^th/trigger/editconsummer/(?P<trigger_id>\d+)$',
                 trigger_edit_consummer,
                 name='edit_consummer'),
             url(r'^th/trigger/edit/thanks',
                 TriggerEditedTemplateView.as_view()),
             url(r'^th/trigger/delete/thanks',
                 TriggerDeletedTemplateView.as_view()),
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
             url(r'^th/service/add/$', UserServiceCreateView.as_view(),
                 name='add_service'),
             url(r'^th/service/delete/(?P<pk>\d+)$',
                 UserServiceDeleteView.as_view(),
                 name='delete_service'),
             url(r'^th/service/add/thanks',
                 UserServiceAddedTemplateView.as_view(),
                 name="service_added"),
             url(r'^th/service/renew/(?P<pk>\d+)$',
                 renew_service,
                 name="renew_service"),
             url(r'^th/service/delete/$',
                 UserServiceDeleteView.as_view(),
                 name='delete_service'),
             url(r'^th/service/delete/thanks',
                 UserServiceDeletedTemplateView.as_view()),
             # ****************************************
             # wizard
             # ****************************************
             url(r'^service/create/$',
                 UserServiceWizard.as_view([ProviderForm,
                                            DummyForm,
                                            ConsummerForm,
                                            DummyForm,
                                            ServicesDescriptionForm]),
                 name='create_service'),
             # every service will use django_th.views.finalcallback
             # and give the service_name value to use to
             # trigger the real callback
             url(r"^th/callbackevernote/$",
                 "django_th.views.finalcallback",
                 {'service_name': 'ServiceEvernote', },
                 name="evernote_callback",
                 ),
             # url(r"^th/callbackpocket/$",
             #    "django_th.views.finalcallback",
             #    {'service_name': 'ServicePocket', },
             #    name="pocket_callback",
             #    ),
             # url(r"^th/callbackreadability/$",
             #    "django_th.views.finalcallback",
             #    {'service_name': 'ServiceReadability', },
             #    name="readability_callback",
             #    ),

             )
