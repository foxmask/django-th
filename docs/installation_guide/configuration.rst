=============
Configuration
=============

Here are the details that will allow the application to work correctly

setup urls.py
-------------

If TriggerHappy is the only project you installed in your virtualenv, go to "setup settings.py"
this setup is only needed when you add TriggerHappy to an **existing** application


add this line to the urls.py to be able to use the complete application

.. code-block:: python

    url(r'', include('django_th.urls')),

this will give something like

.. code-block:: python

    from django.conf.urls import patterns, include, url
    from django.contrib import admin

    urlpatterns = patterns('',
        # Examples:
        # url(r'^$', 'th.views.home', name='home'),
        # url(r'^blog/', include('blog.urls')),

        url(r'^admin/', include(admin.site.urls)),
        url(r'', include('django_th.urls')),
    )


setup settings.py
-----------------

add the module django_th, and its friends, to the INSTALLED_APPS


.. code-block:: python

   INSTALLED_APPS = (
        ...
        'formtools',
        'django_js_reverse',
        'rest_framework',
        'django_th',
        'th_rss',
        'th_evernote',
        'th_github',
        'th_instapush',
        'th_mastodon',
        'th_pelican',
        'th_pocket',
        'th_pushbullet',
        'th_reddit',
        'th_todoist',
        'th_trello',
        'th_twitter',
        'th_wallabag',
    )

comment the line of the application ervice you do not need, by adding a # before the single quote on each line.


setup for testing/debugging purpose
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    DEBUG = True
    ALLOWED_HOSTS = ['*']

setup for production purpose
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    DEBUG = False
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

or set the hostname of your own domain

.. code-block:: python

    DEBUG = False
    ALLOWED_HOSTS = ['mydomain.com']

setup th_settings.py
--------------------

TH_SERVICES is a list of services, like for example,

.. code-block:: python

    TH_SERVICES = (
        'th_evernote.my_evernote.ServiceEvernote',
        'th_github.my_github.ServiceGithub',
        'th_instapush.my_instapush.ServiceInstapush',
        'th_mastodon.my_mastodon.ServiceMastodon',
        'th_pelican.my_pelican.ServicePelican',
        'th_pocket.my_pocket.ServicePocket',
        'th_pushbullet.my_pushbullet.ServicePushbullet',
        'th_rss.my_rss.ServiceRss',
        'th_reddit.my_reddit.ServiceReddit',
        'th_todoist.my_todoist.ServiceTodoist',
        'th_trello.my_trello.ServiceTrello',
        'th_twitter.my_twitter.ServiceTwitter',
        'th_wallabag.my_wallabag.ServiceWallabag',
    )

comment the line of the service you do not need, by adding a # before the single quote on each line.


setup .env file
---------------

if you do not have any .env file in your project folder, then copy the django_th/env.sample to .env 

if you do have an existing .env file, copy the content of django_th/env.sample into it

then the parameters are the following

.. code-block:: python


    DJANGO_TH_PAGINATE_BY=5
    DJANGO_TH_PUBLISHING_LIMIT=2
    DJANGO_TH_PROCESSES=1
    DJANGO_TH_FAILED_TRIES=2
    DJANGO_TH_FIRE=True
    DJANGO_TH_DIGEST_EVENT=False
    DJANGO_TH_SHARING_MEDIA=True
    
    TH_EVERNOTE_SANDBOX=False
    TH_EVERNOTE_CONSUMER_KEY=
    TH_EVERNOTE_CONSUMER_SECRET=
    
    TH_GITHUB_USERNAME=
    TH_GITHUB_PASSWORD=
    TH_GITHUB_CONSUMER_KEY=
    TH_GITHUB_CONSUMER_SECRET=
    
    TH_POCKET_CONSUMER_KEY=

    TH_PUSHBULLET_CLIENT_ID=
    TH_PUSHBULLET_CLIENT_SECRET=
    
    TH_TODOIST_CLIENT_ID=
    TH_TODOIST_CLIENT_SECRET=

    TH_TUMBLR_CONSUMER_KEY=
    TH_TUMBLR_CONSUMER_SECRET=

    TH_TRELLO_CONSUMER_KEY=
    TH_TRELLO_CONSUMER_SECRET=

    TH_TWITTER_CONSUMER_KEY=
    TH_TWITTER_CONSUMER_SECRET=

    TH_PELICAN_AUTHOR=

for each :ref:`services` You will need to set the corresponding variables to be used by it
