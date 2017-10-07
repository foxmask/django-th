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
        # uncomment the lines to enable the service you need
        # 'th_evernote',
        # 'th_github',
        # 'th_instapush',
        # 'th_pelican',
        # 'th_pocket',
        # 'th_pushbullet',
        # 'th_todoist',
        # 'th_trello',
        # 'th_twitter',
        'th_wallabag',
    )


do not forget to uncomment one of the service th_pocket, th_evernote (and then evernote also) th_twitter, th_trello, th_github otherwise, the application won't work.

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
~~~~~~~~~~~~~~~~~~~~
in the th_settings.py file, setup the TH_SERVICES

TH_SERVICES
-----------

TH_SERVICES is a list of services, like for example,

.. code-block:: python

    TH_SERVICES = (
        # uncomment the lines to enable the service you need
        # uncomment the lines to enable the service you need
        # 'th_evernote.my_evernote.ServiceEvernote',
        # 'th_github.my_github.ServiceGithub',
        # 'th_instapush.my_instapush.ServiceInstapush',
        # 'th_pelican.my_pelican.ServicePelican',
        # 'th_pocket.my_pocket.ServicePocket',
        # 'th_pushbullet.my_pushbullet.ServicePushbullet',
        'th_rss.my_rss.ServiceRss',
        # 'th_todoist.my_todoist.ServiceTodoist',
        # 'th_trello.my_trello.ServiceTrello',
        # 'th_twitter.my_twitter.ServiceTwitter',
        'th_wallabag.my_wallabag.ServiceWallabag',
    )

do not forget to uncomment one of the line to enable another service, or the application won't work.

Cache
-----

They are necessary if you want to be able to follow the log and set the cache

For each TriggerHappy component, define one cache like below

.. code-block:: python

    CACHES = {
        'default':
        {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': BASE_DIR + '/cache/',
            'TIMEOUT': 600,
            'OPTIONS': {
                'MAX_ENTRIES': 1000
            }
        },
        # Evernote Cache
        'th_evernote':
        {
            'TIMEOUT': 500,
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/1",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },
        # GitHub
        'th_github':
        {
            'TIMEOUT': 3600,
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/2",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },
        # Pelican
        'th_pelican':
        {
            'TIMEOUT': 3600,
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/3",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },
        # Pocket Cache
        'th_pocket':
        {
            'TIMEOUT': 500,
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/4",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },
        # Pushbullet
        'th_pushbullet':
        {
            'TIMEOUT': 3600,
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/5",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },
        # RSS Cache
        'th_rss':
        {
            'TIMEOUT': 500,
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/6",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },
        # Todoist
        'th_todoist':
        {
            'TIMEOUT': 3600,
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/7",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },
        # Trello
        'th_trello':
        {
            'TIMEOUT': 3600,
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/8",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },
        # Twitter Cache
        'th_twitter':
        {
            'TIMEOUT': 500,
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/9",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },
        # Wallabag
        'th_wallabag':
        {
            'TIMEOUT': 3600,
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/10",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },
        'redis-cache':
        {
            'TIMEOUT': 3600,
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://localhost:6379/11",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "MAX_ENTRIES": 5000,
            }
        },
        'django_th':
        {
            'TIMEOUT': 3600,
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://localhost:6379/12",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "MAX_ENTRIES": 5000,
            }
        },
    }

in the settings, 'default' may already exist in your settings.py, so don't use it, otherwise, if it doesn't, django will complain, so add it.


Logging
-------

in the LOGGING add to loggers

.. code-block:: python

    LOGGING = {
        'handlers': {
            ...
            'file': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': BASE_DIR + '/trigger_happy.log',
                'maxBytes': 61280,
                'backupCount': 3,
                'formatter': 'verbose',

            },
        }
        'loggers':
        {
            ...
            'django_th.trigger_happy': {
                'handlers': ['console', 'file'],
                'level': 'INFO',
            }
        }
    }


Once this is done we can create tasks in the crontab :


Suppose my virtualenv is created in /home/trigger-happy and the django app is located in /home/trigger-happy/th :

.. code-block:: bash

    */12 * * * * . /home/trigger-happy/bin/activate && cd /home/trigger-happy/th/ && ./manage.py read
    */15 * * * * . /home/trigger-happy/bin/activate && cd /home/trigger-happy/th/ && ./manage.py publish
    */20 * * * * . /home/trigger-happy/bin/activate && cd /home/trigger-happy/th/ && ./manage.py recycle
