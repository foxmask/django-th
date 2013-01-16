from django.conf.urls import patterns, include, url

# from django.contrib import admin
# admin.autodiscover()

from django_th.forms import ProfileForm
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
    url(r'^$', 'django_th.views.base', name='base'),
    url(r'^th/$', 'django_th.views.home', name='home'),
    url(r'^th/add/$', 'django_th.views.add_trigger', name='add_trigger'),
    url(r'^th/save/$', 'django_th.views.save_trigger', name='save_trigger'),
    url(r'^th/edit/(?P<trigger_id>/\d+)/$', 'django_th.views.edit_trigger', name='edit_trigger'),
    url(r'^th/delete/(?P<trigger_id>/\d+)/$', 'django_th.views.delete_trigger', name='delete_trigger'),



)


