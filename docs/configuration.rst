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
        'django_rq',
        'th_rss',
        # uncomment the lines to enable the service you need
        # 'th_pocket',
        # 'th_readability',
        # 'evernote',
        # 'th_evernote',
        # 'th_twitter',
        # 'th_holidays',
        # 'th_trello',
        # 'th_github',
        # 'haystack',  # mandatory  if you plan to use th_search
        # 'th_search', # then follow instructions from http://django-haystack.readthedocs.org/

    )


do not forget to uncomment one of the service th_pocket, th_readability, th_evernote (and then evernote also) th_twitter, th_trello, th_github otherwise, the application wont work.

TH_SERVICES
~~~~~~~~~~~

TH_SERVICES is a list of the services, like for example,

.. code-block:: python

    TH_SERVICES = (
        # uncomment the lines to enable the service you need
        'th_rss.my_rss.ServiceRss',
        # 'th_pocket.my_pocket.ServicePocket',
        # 'th_evernote.my_evernote.ServiceEvernote',
        # 'th_readability.my_readability.ServiceReadability',
        # 'th_trello.my_trello.ServiceTrello',
        # 'th_twitter.my_twitter.ServiceTwitter',
        # 'th_github.my_github.ServiceGithub',
    )

do not forget to uncomment one of the line to enable another service, or the application wont work.


Update the database
-------------------

Once the settings is done, enter the following command to sync the database :


.. code-block:: bash

    python manage.py migrate


If you meet some errors with this command, have a look at MIGRATION_0.10.x_to_0.11.x.rst file


If you are installing the project from scratch, do not forget to create a super user:


.. code-block:: bash

    python manage.py createsuperuser


Start the application
---------------------

.. code-block:: bash

    python manage.py runserver


Now open your browser and go to 127.0.0.1:8000/th/ to start using the application


Activate the services
---------------------

to activate a service, you will need to follow those steps

* Requesting a key to the Services
* Adding the key to your settings file
* Adding the service from the Admin
* Activating the service from your account from the public part of the website
* Why this process ?


in details this gives us :


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

Once you did **python manage.py migrate** and followed the standard process to bootstrap the application, go to the admin panel of the application.

Admin Home of Trigger Happy :

.. image:: https://foxmask.trigger-happy.eu/static/trigger_happy/admin_home.png


Admin list of activated services if Trigger Happy :

.. image:: https://foxmask.trigger-happy.eu/static/trigger_happy/admin_service_list.png


Admin Detail of one service of Trigger Happy :

.. image:: https://foxmask.trigger-happy.eu/static/trigger_happy/admin_service_details.png

Activating the service from your account from the public part of the website
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once your services are setup from the admin, you can go on the public part of the website and activate the service you need.

"My activated services" :

.. image:: https://foxmask.trigger-happy.eu/static/trigger_happy/public_services_activated.png

Why this process ?
~~~~~~~~~~~~~~~~~~

* it is simple : actually, to use Trigger Happy you need to install and host it by yourself, and so, you need to "declare" for each service your instance of TriggerHappy to the service provider.
* Other details : you need to activate the service from the admin panel, BECAUSE, TriggerHappy is planed to be used by many other users soon. So the admin of the instance of TriggerHappy will decide if he wants to offer the possibility to use this service of this other one. Once the admin has done his job, the end user, from the "public part" can go to the list of services and add the new one etc.


Others settings
---------------

They are necessary if you want to be able to follow the log and set the cache


CACHE
~~~~~

For each TriggerHappy component, define one cache like below

.. code-block:: python

    CACHES = {
        'default':
        {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': BASE_DIR + '/cache/',
            'TIMEOUT': 600,
            'OPTIONS': {
                'MAX_ENTRIES': 10000
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
        # Pocket Cache
        'th_pocket':
        {
            'TIMEOUT': 500,
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/2",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },
        # RSS Cache
        'th_rss':
        {
            'TIMEOUT': 500,
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/3",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },
        # Readability
        'th_readability':
        {
            'TIMEOUT': 500,
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/4",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },
        # Trello Cache
        'th_trello':
        {
            'TIMEOUT': 500,
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/5",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },
        # Twitter Cache
        'th_twitter':
        {
            'TIMEOUT': 500,
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/6",
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
            "LOCATION": "redis://127.0.0.1:6379/7",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },
    }

in the settings, 'default' may already exist in your settings.py, so dont use it, otherwise, if it doesnt, django will complain, so add it.


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


DJANGO-RQ
~~~~~~~~~

Django-RQ will handle tasks itself to populate the cache from provider services
and then exploit it to publish the data to the expected consumer services

* From Settings

If you dont have a redis server that handles the cache for you then do the following :

.. code-block:: python

    RQ_QUEUES = {
        'default': {
            'TIMEOUT': 3600,
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/1",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },
        'high': {
            'TIMEOUT': 3600,
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/2",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },
        'low': {
            'TIMEOUT': 3600,
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/3",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        }
    }


Otherwise this should be enough :

.. code-block:: python

    CACHES = {
        [...]
        'redis-cache':
        {
                'TIMEOUT': 3600,
                "BACKEND": "django_redis.cache.RedisCache",
                "LOCATION": "redis://127.0.0.1:6379/10",
                "OPTIONS": {
                    "CLIENT_CLASS": "django_redis.client.DefaultClient",
                }
        },
        [...]
    }

    RQ_QUEUES = {
        'default': {
            'USE_REDIS_CACHE': 'redis-cache',
        },
        'high': {
            'USE_REDIS_CACHE': 'redis-cache',
        },
        'low': {
            'USE_REDIS_CACHE': 'redis-cache',
        },
    }


Once this is done we can create tasks in the crontab :


Suppose my virtualenv is created in /home/trigger-happy and the django app is located in /home/trigger-happy/th :

.. code-block:: bash

    */12 * * * * . /home/trigger-happy/bin/activate && cd /home/trigger-happy/django_th/ && ./manage.py fire_read_data && ../bin/rqworker-default-burst.sh
    */15 * * * * . /home/trigger-happy/bin/activate && cd /home/trigger-happy/th/ && ./manage.py fire_publish_data && ../bin/rqworker-high-burst.sh
    */20 * * * * . /home/trigger-happy/bin/activate && cd /home/trigger-happy/th/ && ./manage.py fire_get_outside_data && ../bin/rqworker-low-burst.sh

where `rqworker-default-burst.sh` contains :

.. code-block:: bash

    #!/bin/bash
    python manage.py rqworker default --burst &
    python manage.py rqworker default --burst &
    python manage.py rqworker default --burst &
    python manage.py rqworker default --burst &
    python manage.py rqworker default --burst &


where `rqworker-high-burst.sh` contains :

.. code-block:: bash

    #!/bin/bash
    python manage.py rqworker high --burst &
    python manage.py rqworker high --burst &
    python manage.py rqworker high --burst &
    python manage.py rqworker high --burst &
    python manage.py rqworker high --burst &

where `rqworker-low-burst.sh` contains :

.. code-block:: bash

    #!/bin/bash
    python manage.py rqworker low --burst &



TH_HOLIDAYS
~~~~~~~~~~~

To use the Holidays feature, just add this piece of HTML in the template templates/mark_all.html :


.. code:: html

    <li role="presentation"><a role="menuitem" href="{% url 'holidays' %}" title="{% trans 'Set Triggers on Holidays ?' %}"><span class="glyphicon glyphicon-flag"></span>&nbsp;&nbsp;{% trans 'Set Triggers on Holidays ?' %}</a></li>


HAYSTACK
~~~~~~~~

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
