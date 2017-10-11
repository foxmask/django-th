Pushbullet
==========

Service Description:
--------------------

Your devices working better together

Nota : to be able to work, this service requires that your host uses HTTPS

modifications of settings.py
----------------------------

1) INSTALLED_APPS :

uncomment the following line

.. code-block:: python

    INSTALLED_APPS = (
        # 'th_pushbullet',
    )

to get

.. code-block:: python

    INSTALLED_APPS = (
        'th_pushbullet',
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
        # Pushbullet Cache
        'th_pushbullet':
        {
            'TIMEOUT': 500,
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/12",
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
        # 'th_pushbullet.my_pushbullet.ServicePushbullet',
    )

to get

.. code-block:: python

    TH_SERVICES = (
        'th_pushbullet.my_pushbullet.ServicePushbullet',
    )

2) The service keys

Here are the modifications of .env file you will need to do to be able to use your credentials with Pushbullet

.. code-block:: python

    TH_PUSHBULLET = {
        # get your credential by subscribing to
        # https://www.pushbullet.com/#settings/clients
        TH_PUSHBULLET_CLIENT_ID= 'your pushbulet id'
        TH_PUSHBULLET_CLIENT_SECRET= 'your pushbulet secret'
    }

creation of the table of the services
-------------------------------------

enter the following command

.. code-block:: bash

    python manage.py migrate


from the admin panel, activation of the service
-----------------------------------------------

from http://yourdomain.com/admin/django_th/servicesactivated/add/

* Select "Pushbullet",
* Set the Status to "Enabled"
* Check Auth Required: this will permit to redirect to the user (or you) to Pushbullet to ask to confirm the access to his/your Pushbullet account
* Fill a description
