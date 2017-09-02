Tumblr
=======

Service Description:
--------------------

A Microblogging and social network

modifications of settings.py
----------------------------

1) INSTALLED_APPS :

add or uncomment the following line

.. code-block:: python

    INSTALLED_APPS = (
        # 'th_tumblr',
    )

to get

.. code-block:: python

    INSTALLED_APPS = (
        'th_tumblr',
    )

2) Cache :

After the default cache add :

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
        # Tumblr Cache
        'th_tumblr':
        {
            'TIMEOUT': 500,
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/5",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },

modifications of th_settings.py
-------------------------------

1) TH_SERVICES

add or uncomment the following line

.. code-block:: python

    TH_SERVICES = (
        # 'th_tumblr.my_tumblr.ServiceTumblr',
    )

to get

.. code-block:: python

    TH_SERVICES = (
        'th_tumblr.my_tumblr.ServiceTumblr',
    )

2) The service keys

It's strongly recommended that your put the following in a local_settings.py, to avoid to accidentally push this to a public repository


.. code-block:: python

    TH_TUMBLR = {
        # get your credential by subscribing to
        # https://dev.twitter.com/
        'consumer_key': '<your tumblr key>',
        'consumer_secret': '<your tumblr secret>',
    }

creation of the table of the services
-------------------------------------

enter the following command

.. code-block:: bash

    python manage.py migrate


from the admin panel, activation of the service
-----------------------------------------------

from http://yourdomain.com/admin/django_th/servicesactivated/add/

* Select "Tumblr",
* Set the Status to "Enabled"
* Check Auth Required: this will permit to redirect the user (or you) to Tumblr website to confirm the access of the Tumblr account
* Fill a description
