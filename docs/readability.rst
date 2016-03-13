Readability
===========

Service Description:
--------------------

a "Read it Later" service

modifications of settings.py
----------------------------

1) INSTALLED_APPS :

.. code-block:: python

    INSTALLED_APPS = (
        'th_readability',
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
        # Readability Cache
        'th_readability':
        {
            'TIMEOUT': 500,
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/5",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },

3) TH_SERVICES

add this line to the TH_SERVICES setting

.. code-block:: python

    TH_SERVICES = (
        'th_readability.my_readability.ServiceReadability',
    )



4) The service keys

I strongly recommend that your put the following in a local_settings.py, to avoid to accidentally push this to a public repository


.. code-block:: python

    TH_READABILITY = {
        # get your credential by subscribing to
        # https://www.readability.com/settings/account
        'consumer_key': '<your readability key>',
        'consumer_secret': '<your readability secret>',
    }


creation of the table of the services
-------------------------------------

enter the following command

.. code-block:: bash

    python manage.py migrate


from the admin panel, activation of the service
-----------------------------------------------

from http://yourdomain.com/admin/django_th/servicesactivated/add/

* Select "Readability",
* Set the Status to "Enabled"
* Check Auth Required: this will permit to redirect to the user (or you) to Readability to ask to confirm the access to hist/your Readability account
* Fill a description


