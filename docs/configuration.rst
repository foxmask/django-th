=============
Configuration
=============

Here are the details that will permit to make working the application correctly

urls.py
-------

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


settings.py 
-----------

add the module django_th, and its friends, to the INSTALLED_APPS


.. code-block:: python

   INSTALLED_APPS = (
        ...
        'formtools',
        'django_js_reverse',
        'redisboard',
        'django_th',
        'th_rss',
        'th_pocket',
        'th_readability',
        'evernote',
        'th_evernote',
        'th_twitter',
        'th_holidays',
        'th_trello',
        'th_github',
        'haystack',  # mandatory  if you plan to use th_search
        'th_search', # then follow instructions from http://django-haystack.readthedocs.org/

    )


this setting supposes you already own a Pocket account

TH_SERVICES
~~~~~~~~~~~

TH_SERVICES is a list of the services, like for example,  

.. code-block:: python

    TH_SERVICES = (
        # comment the line to disable the service you dont want
        'th_rss.my_rss.ServiceRss',
        'th_pocket.my_pocket.ServicePocket',
        'th_evernote.my_evernote.ServiceEvernote',
        'th_readability.my_readability.ServiceReadability',
        'th_trello.my_trello.ServiceTrello',        
        'th_twitter.my_twitter.ServiceTwitter',
        'th_github.my_github.ServiceGithub',
    )



Update the database
-------------------

Once the settings is done, enter the following command to sync the database



if you start from scratch and dont have created a django application yet, you should do :


.. code-block:: bash

    python manage.py syncdb


otherwise do :


.. code-block:: bash

    python manage.py migrate


if you meet some errors with this last command, have a look at MIGRATION_0.10.x_to_0.11.x.rst file


Activate the services
---------------------

to activate a service, you will need to follow those steps

* Requesting a key to the Services
* Adding the key to your settings file
* Adding the service from the Admin
* Activating the service from your account from the public part of the website
* Why this process ?


Requesting a key to the Services
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For each service, Trigger Happy expects to have some consumer key coming from the wanted service.
So for each service, you need to register an account on each of this service, then required a key. 

You can have a look at the `README of Twitter <https://github.com/foxmask/django-th-twitter/blob/master/README.rst>`_, or `README of Pocket <https://github.com/foxmask/django-th-pocket/blob/master/README.rst>`_

Adding the key to the settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Once you own the keys., You add them to the settings.py file in 

.. code-block:: python

    TH_<SERVICE_NAME> = (
        'consumer_key' => 'foobar',
        'consumer_token' => 'blabla'
    )

For example for Twitter :

.. code-block:: python

    TH_TWITTER = {
        'consumer_key': 'abcdefghijklmnopqrstuvwxyz',
        'consumer_secret': 'abcdefghijklmnopqrstuvwxyz',
    }


IMPORTANT : 

With all the service you will enable, to avoid to share your key by accident, I strongly recommand that you put all of them in a seperate local_settings.py that you include at the end of the main settings.py 

So, when I speak about settings.py think about local_settings.py



Adding the service from the Admin
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once you did **python manage.py syncdb** and followed the standard process to bootstrap the application, go to the admin panel of the application.

Admin Home of Trigger Happy : 

.. image:: http://foxmask.info/public/trigger_happy/admin_home.png


Admin list of activated services if Trigger Happy : 

.. image:: http://foxmask.info/public/trigger_happy/admin_service_list.png


Admin Detail of one service of Trigger Happy : 

.. image:: http://foxmask.info/public/trigger_happy/admin_service_details.png

Activating the service from your account from the public part of the website
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once your services are setup from the admin, you can go on the public part of the website and activate the service you need.

"My activated services" :

.. image:: http://foxmask.info/public/trigger_happy/public_services_activated.png

Why this process ? 
~~~~~~~~~~~~~~~~~~

* it is simple : actually, to use Trigger Happy you need to install and host it by yourself, and so, you need to "declare" for each service your instance of TriggerHappy. 
* Other details : you need to activate the service from the admin panel, BECAUSE, TriggerHappy is planed to be used by many other users soon. So the admin of the instance of TriggerHappy will decide if he wants to offer the possibility to use this service of this other one. Once the admin has done his job, the end user, from the "public part" can go to the list of services and add the new one etc.


Others settings
---------------

They are necessary if you want to be able to follow the log, cache rss and use the site framework


CACHE 
~~~~~

For each TriggerHappy component, define one cache like below 

.. code:: python
    CACHES = {
        # Evernote Cache
        'th_evernote':
        {
            'TIMEOUT': 500,
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "127.0.0.1:6379",
            "OPTIONS": {
                "DB": 1,
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },
        # Pocket Cache
        'th_pocket':
        {
            'TIMEOUT': 500,
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "127.0.0.1:6379",
            "OPTIONS": {
                "DB": 2,
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },
        # RSS Cache
        'th_rss':
        {
            'TIMEOUT': 500,
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "127.0.0.1:6379",
            "OPTIONS": {
                "DB": 3,
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },
        # Readability
        'th_readability':
        {
            'TIMEOUT': 500,
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "127.0.0.1:6379",
            "OPTIONS": {
                "DB": 4,
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },
        # Trello Cache
        'th_trello':
        {
            'TIMEOUT': 500,
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "127.0.0.1:6379",
            "OPTIONS": {
                "DB": 5,
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },
        # Twitter Cache
        'th_twitter':
        {
            'TIMEOUT': 500,
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "127.0.0.1:6379",
            "OPTIONS": {
                "DB": 6,
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },
        # Github Cache
        'th_github':
        {
            'TIMEOUT': 500,
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "127.0.0.1:6379",
            "OPTIONS": {
                "DB": 7,
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },        
    }


The Log 
~~~~~~~

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


CELERY 
~~~~~~

Celery will handle tasks itself to populate the cache from provider services
and then exploit it to publish the data to the expected consumer services

* From Settings


Define the broker then the scheduler

.. code:: python

    from celery.schedules import crontab

    BROKER_URL = 'redis://localhost:6379/0'

    CELERYBEAT_SCHEDULE = {
        'read-data': {
            'task': 'django_th.tasks.read_data',
            'schedule': crontab(minute='12,24,36,48'),
        },
        'publish-data': {
            'task': 'django_th.tasks.publish_data',
            'schedule': crontab(minute='20,40,59'),
        },
        'outside-cache': {
            'task': 'django_th.tasks.get_outside_cache',
            'schedule': crontab(minute='15,30,45'),
        },
    }


* From SUPERVISORD


.. code:: python

    [program:django_th_worker]
    user = foxmask
    directory=/home/projects/trigger-happy/th
    command=/home/projects/trigger-happy/bin/celery -A django_th worker --autoscale=10,3 -l info
    autostart=true
    autorestart=true
    redirect_stderr=true
    stdout_logfile=/home/projects/trigger-happy/logs/trigger-happy.log
    stderr_logfile=/home/projects/trigger-happy/logs/trigger-happy-err.log

    [program:django_th_beat]
    user = foxmask
    directory=/home/projects/trigger-happy/th
    command=/home/projects/trigger-happy/bin/celery -A django_th beat -l info
    autostart=true
    autorestart=true
    redirect_stderr=true
    stdout_logfile=/home/projects/trigger-happy/logs/trigger-happy.log
    stderr_logfile=/home/projects/trigger-happy/logs/trigger-happy-err.log



REDISBOARD
~~~~~~~~~~

.. code:: python

    # REDISBOARD
    REDISBOARD_DETAIL_FILTERS = ['.*']


HAYSTACK 
~~~~~~~~~

if you plan to use the search feature, put the engine of your choice, for example : 

.. code:: python

    # needed to th_search and haystack
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
            'URL': 'http://127.0.0.1:9200/',
            'INDEX_NAME': 'haystack',
        },
    }
