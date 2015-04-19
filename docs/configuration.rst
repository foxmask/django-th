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
        'django_th',
        'th_rss',
        'th_pocket',
        'django_js_reverse',
    )

this setting supposes you already own a Pocket account

TH_SERVICES
~~~~~~~~~~~

TH_SERVICES is a list of the services, like for example,  

.. code-block:: python

    TH_SERVICES = (
        'th_rss.my_rss.ServiceRss',
        'th_pocket.my_pocket.ServicePocket',
    )

this setting supposes you already own a Pocket account

If you plan to integrate django_th in an existing project then, to deal with the templates and avoid the TemplateDoesNotExist error you can 
copy the template in your own templates directory or set the path like this :

.. code-block:: python

    import os
    PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
    TEMPLATE_DIRS += (
        PROJECT_DIR + '/../../lib/<python-version>/site-package/django_th/templates/',
    )


Update the database
-------------------

Once the settings is done, enter the following command to sync the database

.. code-block:: bash

    python manage.py makemigrations django_th
    python manage.py migrate



Activate the services
---------------------

to activate a service, you will need to follow those steps

* Requesting a key to the Services
* Adding the key to the settings
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
* Other details : you need to activate the service from the admin panel, BECAUSE, TriggerHappy is planed to be used by many other users soon. So the admin of the instance of TriggerHappy will decide if he want to offer the possibility to use this service of this other one. Once the admin has done his job, the end user, from the "public part" can go to the list of service and add the new one etc.


Others settings
---------------

They are necessary if you want to be able to follow the log, cache rss and use the site framework

Site Framework
~~~~~~~~~~~~~~

the site framework will be deprecated for the next release, anyway, for the current one (0.9.1) the required settings are :


.. code-block:: python

    SITE_ID = 1

in INSTALLED_APPS add 

.. code-block:: python

    'django.contrib.sites',

add to TEMPLATE_CONTEXT_PROCESSORS the context processor like this :

.. code-block:: python


    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        # get the Site information anywhere arround the page
        'django_th.context_processors.current_site',
        'django.core.context_processors.request'

The Cache 
~~~~~~~~~

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
        'rss':
        {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': BASE_DIR + '/cache/rss/',
            'TIMEOUT': 3600,
            'OPTIONS': {
                'MAX_ENTRIES': 1000
            }
        }
    }


The Log 
~~~~~~~

in the LOGGING add to loggers

.. code-block:: python

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


