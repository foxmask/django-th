from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

from registration.forms import RegistrationFormUniqueEmail

from .forms import ProfileForm
from .forms import ServicesDescriptionForm
from .forms.rss import RssForm
from .forms.evernote import EvernoteForm
from .views import TriggerListView, TriggerUpdateView, TriggerDeleteView,\
    TriggerAddedTemplateView,\
    TriggerEditedTemplateView,\
    TriggerDeletedTemplateView,\
    UserServiceListView,\
    UserServiceCreateView,\
    UserServiceUpdateView,\
    UserServiceDeleteView,\
    UserServiceAddedTemplateView,\
    UserServiceEditedTemplateView,\
    UserServiceDeletedTemplateView,\
    UserServiceWizard


urlpatterns = patterns('',
    # ****************************************
    # profiles module:
    #
    #
    # for each method ; add an extrat context
    # thus we can load a modal form to add
    # his own histo
    # ****************************************
    url(r'^profiles/edit/$',
        'profiles.views.edit_profile',
        {'form_class': ProfileForm, 'success_url': '/'}),

    url(r'^profiles/(?P<username>\w+)/$',
        'profiles.views.profile_detail',
        ),

    url(r'^profiles/$',
        'profiles.views.profile_list',
        ),


    # ****************************************
    # admin module
    # ****************************************
    url(r'^admin/', include(admin.site.urls)),
    # ****************************************
    # registration module
    # ****************************************
    url(r'^accounts/register/', 'registration.views.register',
        {'form_class': RegistrationFormUniqueEmail,
         'backend': 'registration.backends.default.DefaultBackend'}),
    url(r'^accounts/', include('registration.backends.default.urls')),

    # ****************************************
    # profile module
    # here to add the last method : create !
    # ****************************************
    url(r'^profiles/', include('profiles.urls')),

    # ****************************************
    # auth module
    # ****************************************
    url(r'^auth/', include('django.contrib.auth.urls')),
    # ****************************************
    # customized lgout action
    # ****************************************
    url(r'^logout/$', 'django_th.views.logout_view', name='logout'),

    # ****************************************
    # trigger happy module
    # ****************************************
    url(r'^$', TriggerListView.as_view(),
        name='base'),
    url(r'^trigger/$', TriggerListView.as_view(),
        name='home'),
    # ****************************************
    # * trigger
    # ****************************************
#    url(r'^trigger/add/$', TriggerCreateView.as_view(),
#        name='add_trigger'),
    url(r'^trigger/edit/(?P<pk>\d+)$', TriggerUpdateView.as_view(),
        name='edit_trigger'),
    url(r'^trigger/delete/(?P<pk>\d+)$', TriggerDeleteView.as_view(),
        name='delete_trigger'),
    url(r'^trigger/add/thanks', TriggerAddedTemplateView.as_view()),
    url(r'^trigger/edit/thanks', TriggerEditedTemplateView.as_view()),
    url(r'^trigger/delete/$', TriggerDeleteView.as_view(),
        name='delete_trigger'),
    url(r'^trigger/delete/thanks', TriggerDeletedTemplateView.as_view()),
    # ****************************************
    # * service
    # ****************************************
    url(r'^service/$', UserServiceListView.as_view(), name='user_services'),
    url(r'^service/add/$', UserServiceCreateView.as_view(),
        name='add_service'),
    url(r'^service/edit/(?P<pk>\d+)$', UserServiceUpdateView.as_view(),
        name='edit_service'),
    url(r'^service/delete/(?P<pk>\d+)$', UserServiceDeleteView.as_view(),
        name='delete_service'),
    url(r'^service/add/thanks', UserServiceAddedTemplateView.as_view()),
    url(r'^service/edit/thanks', UserServiceEditedTemplateView.as_view()),
    url(r'^service/delete/$', UserServiceDeleteView.as_view(),
        name='delete_service'),
    url(r'^service/delete/thanks', UserServiceDeletedTemplateView.as_view()),

    # wizard
    url(r'^service/create/$',
        UserServiceWizard.as_view([RssForm, EvernoteForm,
        ServicesDescriptionForm]),
        name='create_service'),

    #evernote
    url(r"^callbackevernote/$", "callback",
        {'from': 'evernote', }, name="evernote_callback",
        ),

    # *********************************************
    #  Linked Account
    # *********************************************
    # url(r"^linked_accounts/", include("linked_accounts.urls"))
)
