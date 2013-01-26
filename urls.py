from django.conf.urls import patterns, include, url

# from django.contrib import admin
# admin.autodiscover()

from .forms import ProfileForm
from registration.forms import RegistrationFormUniqueEmail

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
            {'form_class': ProfileForm,
             'success_url': '/', }
        ),

    url(r'^profiles/(?P<username>\w+)/$',
        'profiles.views.profile_detail',
        ),

    url(r'^profiles/$',
        'profiles.views.profile_list',
        ),


    # ****************************************
    # admin module
    # ****************************************
    # url(r'^admin/', include(admin.site.urls)),
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
    url(r'^$', 'django_th.views.base',
        name='base'),
    url(r'^trigger/$', 'django_th.views.home',
        name='home'),
    url(r'^trigger/add/$', 'django_th.views.add_service',
        name='add_service'),
    url(r'^trigger/save/$', 'django_th.views.save_service',
        name='save_service'),
    url(r'^trigger/edit/(?P<trigger_id>\d+)$', 'django_th.views.edit_service',
        name='edit_service'),
    url(r'^trigger/delete/(?P<trigger_id>\d+)$', 'django_th.views.delete_service',
        name='delete_service'),
    url(r'^trigger/deleted/$', 'django_th.views.deleted_service',
        name='deleted_service'),
    url(r'^trigger/added$', 'django_th.views.added_service',
        name='added_service'),
    url(r'^trigger/edited$', 'django_th.views.edited_service',
        name='edited_service'),
    url(r'^trigger/hasbeendeleted', 'django_th.views.hasbeendeleted_service',),
    # *********************************************
    #  Linked Account
    # *********************************************
    # url(r"^linked_accounts/", include("linked_accounts.urls"))
)
