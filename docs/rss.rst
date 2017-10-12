RSS
===

Service Description:
--------------------

Service that grabs RSS all around the web or creates also RSS from other services

modifications of settings.py
----------------------------

1) INSTALLED_APPS:

add or uncomment the following line

.. code-block:: python

    INSTALLED_APPS = (
        # 'th_rss',
    )

to get

.. code-block:: python

    INSTALLED_APPS = (
        'th_rss',
    )

2) Cache:

After the default cache add:

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
        # RSS Cache
        'th_rss':
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

uncomment the following line

.. code-block:: python

    TH_SERVICES = (
        # 'th_rss.my_rss.ServiceRss',
    )

to get

.. code-block:: python

    TH_SERVICES = (
        'th_rss.my_rss.ServiceRss',
    )

creation of the table of the services
-------------------------------------

enter the following command

.. code-block:: bash

    python manage.py migrate


from the admin panel, activation of the service
-----------------------------------------------

from http://yourdomain.com/admin/django_th/servicesactivated/add/

* Select "RSS",
* Set the Status to "Enabled"
* Uncheck "Auth Required": this service does not require an authorization to access anything
* Provide a description

