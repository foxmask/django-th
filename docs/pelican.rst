Pelican
=======

Service Description:
--------------------

Pelican Static Site Generator

modifications of settings.py
----------------------------

1) INSTALLED_APPS :

add or uncomment the following line

.. code-block:: python

    INSTALLED_APPS = (
        # 'th_pelican',
    )

to get

.. code-block:: python

    INSTALLED_APPS = (
        'th_pelican',
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
        # Pelican
        'th_pelican':
        {
            'TIMEOUT': 3600,
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/8",
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
        # 'th_pelican.my_pelican.ServicePelican',
    )

to get

.. code-block:: python

    TH_SERVICES = (
        'th_pelican.my_pelican.ServicePelican',
    )


4) Pelican Author :

Set an author that will be added to the creation of each post

.. code-block:: python

    TH_PELICAN_AUTHOR = 'Foxmask'


creation of the table of the services
-------------------------------------

enter the following command

.. code-block:: bash

    python manage.py migrate


from the admin panel, activation of the service
-----------------------------------------------

from http://yourdomain.com/admin/django_th/servicesactivated/add/

* Select "Pelican",
* Set the Status to "Enabled"
* Uncheck "Auth Required": this service does not required an authorization to access to something
* Fill a description

