.. image:: https://travis-ci.org/foxmask/django-th.svg?branch=master
    :target: https://travis-ci.org/foxmask/django-th
    :alt: Travis Status

.. image:: https://readthedocs.org/projects/trigger-happy/badge/?version=latest
    :target: https://readthedocs.org/projects/trigger-happy/?badge=latest
    :alt: Documentation status

.. image:: https://pypip.in/version/django-th/badge.svg
    :target: https://pypi.python.org/pypi/django-th/
    :alt: Latest version

.. image:: https://pypip.in/py_versions/django-th/badge.svg
    :target: https://pypi.python.org/pypi/django-th/
    :alt: Supported Python versions

.. image:: https://pypip.in/license/django-th/badge.svg
    :target: https://pypi.python.org/pypi/django-th/
    :alt: License


====================
Django Trigger Happy
====================

Automatically share data between popular services you use on the web.
And instead of giving your credentials to them, become the owner of yours !

For example a new RSS item is published, django-trigger-happy will be able to 
automatically create a note on your Evernote account or create a bookmark to
your own Readability or Pocket account and so on

.. image:: http://trigger-happy.eu/static/th_esb.png


Description
===========

The goal of this project is to be independant from any other solution like 
IFTTT, CloudWork or others.

Thus you could host your own solution and manage your own triggers without 
depending any non-free solution.

With this project you can host triggers for you.

All you need is to have a hosting provider (or simply your own server ;) )
who permits to use a manager of tasks like "cron" and, of course Python.

Requirements
============

* Python 3.4.x
* `Django <https://pypi.python.org/pypi/Django/>`_ >= 1.8
* `arrow <https://pypi.python.org/pypi/arrow>`_ == 0.5.4
* django-formtools == 1.0
* `django-js-reverse <https://pypi.python.org/pypi/django-js-reverse>`_ == 0.5.1
* `libtidy-dev <http://tidy.sourceforge.net/>`_  >= 0.99

The latest libtidy-dev should be installed with your operating system package manager, not from pip.
On a Ubuntu system: 
 
.. code:: system

    apt-get install libtidy-dev


for celery

* `Celery <http://www.celeryproject.org/>`_ == 3.1.18

for evernote support

* `Evernote for python 3 <https://github.com/evernote/evernote-sdk-python3>`_ 

for pocket support

* `pocket <https://pypi.python.org/pypi/pocket>`_  == 0.3.5

for readability support

* `readability <https://pypi.python.org/pypi/readability-api>`_ == 1.0.0

for rss support

* `feedparser <https://pypi.python.org/pypi/feedparser>`_  == 5.1.3

for search engine

* `django-haystack <https://github.com/django-haystack/django-haystack>`_ == 2.3.1

for trello support

* `trello <https://github.com/sarumont/py-trello>`_  == 0.4.3

for twitter support

* `twython <https://github.com/ryanmcgrath/twython>`_  == 3.2.0


for redis support 

* `django-redis <https://pypi.python.org/pypi/django-redis>`_ == 4.1.0
* `django-redisboard <https://pypi.python.org/pypi/django-redisboard>`_ == 1.2.0



Installation
============

To get the project up and running, from your virtualenv, do:



From GitHub 
-----------


.. code-block:: bash

    git clone https://github.com/foxmask/django-th.git

then continue by installing :

.. code-block:: bash

    cd django-th
    python setup install
    cd ..
    pip install -r requirements-evernote.txt


From Pypi
---------

in 2 steps :

.. code:: system

    pip install django-th

and you will have to finish by 

.. code:: system

    pip install -r https://raw.githubusercontent.com/foxmask/django-th/master/requirements-evernote.txt

this is because Evernote SDK for Python 3 is not yet available on pypi

Parameters
==========

As usual you will setup the database parameters.

Important parts are the settings of the available services :

settings.py 
-----------

add the module django_th to the INSTALLED_APPS


.. code:: python

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
        'haystack',  # mandatory  if you plan to use th_search
        'th_search', # then follow instructions from http://django-haystack.readthedocs.org/

    )


TH_SERVICES
~~~~~~~~~~~

TH_SERVICES is a list of the supported services

.. code:: python

    TH_SERVICES = (
        # comment the line to disable the service you dont want
        'th_rss.my_rss.ServiceRss',
        'th_pocket.my_pocket.ServicePocket',
        'th_evernote.my_evernote.ServiceEvernote',
        'th_readability.my_readability.ServiceReadability',
        'th_trello.my_trello.ServiceTrello',
        'th_twitter.my_twitter.ServiceTwitter',
    )



TH_EVERNOTE
~~~~~~~~~~~

TH_EVERNOTE is the settings you will need to be able to add/read data in/from Evernote.

To be able to use Evernote see official FAQ :

* `How do I create an API key? <https://dev.evernote.com/support/faq.php#createkey>`_
* `How do I copy my API key from Sandbox to www (production)? <https://dev.evernote.com/support/faq.php#activatekey>`_

.. code:: python

    TH_EVERNOTE = {
        'sandbox': True, #set to False in production - to be able to use it with trigger happy of course ;)
        'consumer_key': 'abcdefghijklmnopqrstuvwxyz',
        'consumer_secret': 'abcdefghijklmnopqrstuvwxyz',
    }



TH_POCKET
~~~~~~~~~

TH_POCKET is the settings you will need to be able to add/read data in/from Pocket.

To be able to use Pocket :

* you will need to grad the pocket consumer key `by creating a new application <http://getpocket.com/developer/apps/>`_ with the rights access as below

.. image:: http://foxmask.info/public/trigger_happy/pocket_account_settings.png 

* then copy the "consumer key" of your application to the settings.py

.. code:: python

    TH_POCKET = {
        'consumer_key': 'abcdefghijklmnopqrstuvwxyz',
    }



TH_READABILITY
~~~~~~~~~~~~~~

TH_READABILITY is the settings you will need, to be able to add/read data in/from readability Service.

To be able to use readability :

* you will need to `grad the readability keys <https://readability.com/developers/api>`_
* create a new application at readability website, then

.. image:: http://foxmask.info/public/trigger_happy/readability_account_settings.png 

* copy the "keys & secret" of your application to the settings.py
 
.. code:: python

    TH_READABILITY = {
        'consumer_key': 'abcdefghijklmnopqrstuvwxyz',
        'consumer_secret': 'abcdefghijklmnopqrstuvwxyz',
    }



TH_TRELLO
~~~~~~~~~~

TH_TRELLO is the settings you will need to be able to add/read data in/from Trello.

To be able to use Trello:

* you will need to create an account at https://trello.com/docs/
* then create an application and adding to the URL request "scope=read,write"

.. image:: http://foxmask.info/public/trigger_happy/twitter_key_settings.png 

.. code:: python

    TH_TRELLO = {
        'consumer_key': 'abcdefghijklmnopqrstuvwxyz',
        'consumer_secret': 'abcdefghijklmnopqrstuvwxyz',
    }


TH_TWITTER
~~~~~~~~~~

TH_TWITTER is the settings you will need to be able to add/read data in/from Twitter.

To be able to use Twitter:

* you will need to create an account at https://apps.twitter.com/
* then create an application
* then on the Application Settings tab set the rights to "read and write permission"
* then on Keys tab copy the information and fill the settings.py with them

.. image:: http://foxmask.info/public/trigger_happy/twitter_key_settings.png 

.. code:: python

    TH_TWITTER = {
        'consumer_key': 'abcdefghijklmnopqrstuvwxyz',
        'consumer_secret': 'abcdefghijklmnopqrstuvwxyz',
    }

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
            'schedule': crontab(minute='27,54'),
        },
        'publish-data': {
            'task': 'django_th.tasks.publish_data',
            'schedule': crontab(minute='59'),
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
    


urls.py
-------

.. code:: python

    from django.conf.urls import patterns, include, url
    from django.contrib import admin

    urlpatterns = patterns('',
         # Examples:
         # url(r'^$', 'th.views.home', name='home'),
         # url(r'^blog/', include('blog.urls')),
  
         url(r'^admin/', include(admin.site.urls)),
         url(r'', include('django_th.urls')),
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


Starting the application
------------------------

.. code-block:: bash

    python manage.py runserver


Now that everything is in place, Celery will do our job in background 
in the meantime you will be able to manage your triggers from the front part



Setting up : Administration
===========================

Once the module is installed, go to the admin panel and activate the service you want. 

Currently there are 5 services, Evernote, Pocket, RSS, Trello and Twitter.

.. image:: http://foxmask.info/public/trigger_happy/th_admin_evernote_activated.png

.. image:: http://foxmask.info/public/trigger_happy/th_admin_pocket_activated.png

.. image:: http://foxmask.info/public/trigger_happy/th_admin_readability_activated.png

.. image:: http://foxmask.info/public/trigger_happy/th_admin_rss_activated1.png

.. image:: http://foxmask.info/public/trigger_happy/th_admin_twitter_activated.png



Once they are activated....

.. image:: http://foxmask.info/public/trigger_happy/admin_service_list.png


... User can use them



Usage :
=======

Activating services : 
---------------------

The user activates the service for their own need. If the service requires an external authentication, he will be redirected to the service which will ask him the authorization to acces the user's account. 
Once it's done, goes back to django-trigger-happy to finish and record the "auth token".

.. image:: http://foxmask.info/public/trigger_happy/public_services_activated.png

Using the activated services :
------------------------------

a set of 3 pages will ask to the user information that will permit to trigger data from a service "provider" to a service "consummer".

For example : 

* page 1 : the user gives a RSS feed
* page 2 : the user gives the name of the notebook where notes will be stored and a tag if he wants
* page 3 : the user gives a description


Fire the Triggers by hands :
============================

Here are the available management commands you can use by hand when you need to bypass the beat of Celery :

.. code:: python

    Available subcommands:

    [django_th]
        fire_read_data     # will put date in cache
        fire_publish_data  # will read cache and publish data
 

To start handling the queue of triggers you/your users configured, just set those 2 management commands in a crontab or any other scheduler solution of your choice, if you dont want to use the beat of Celery

Also : Keep in mind to avoid to set a too short duration between 2 run to avoid to be blocked by the externals services (by their rate limitation) you/your users want to reach.


Complete Documentation
======================

http://trigger-happy.readthedocs.org/


Blog posts :
============

You can find all details of all existing services of the blog :
http://www.foxmask.info/tag/TriggerHappy
