GitHub
======

Service Description:
--------------------

Powerful collaboration, code review, and code management for open source and private projects. Public projects are always free.

modifications of settings.py
----------------------------

1) INSTALLED_APPS:

add or uncomment the following line

.. code-block:: python

    INSTALLED_APPS = (
        # 'th_github',
    )

to get

.. code-block:: python

    INSTALLED_APPS = (
        'th_github',
    )


2) Cache:

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
        # GitHub
        'th_github':
        {
            'TIMEOUT': 3600,
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/7",
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
        # 'th_github.my_github.ServiceGithub',
    )

to get

.. code-block:: python

    TH_SERVICES = (
        'th_github.my_github.ServiceGithub',
    )


2) The service keys

It's strongly recommended that you put the following in a local_settings.py, to avoid to accidentally push this to a public repository


.. code-block:: python

    TH_GITHUB = {
        'username': 'username',
        'password': 'password',
        'consumer_key': 'my key',
        'consumer_secret': 'my secret'
    }

creation of the table of the services
-------------------------------------

enter the following command

.. code-block:: bash

    python manage.py migrate


from the admin panel, activation of the service
-----------------------------------------------

from http://yourdomain.com/admin/django_th/servicesactivated/add/

* Select "GitHub",
* Set the Status to "Enabled"
* Check Auth Required: this will permit to redirect the user (or you) to GitHub website to confirm the access of the GitHub account
* Provide a description

