Todoist
=======

Service Description:
--------------------

a Tasks Managements

Nota : to be able to work, this service requires that your host uses HTTPS

modifications of settings.py
----------------------------

1) INSTALLED_APPS :

.. code-block:: python

    INSTALLED_APPS = (
        'th_todoist',
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
        # Todoist Cache
        'th_todoist':
        {
            'TIMEOUT': 500,
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/11",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        },

3) TH_SERVICES

add this line to the TH_SERVICES setting

.. code-block:: python

    TH_SERVICES = (
        'th_todoist.my_todoist.ServiceTodoist',
    )



4) The service keys

I strongly recommend that your put the following in a local_settings.py, to avoid to accidentally push this to a public repository


.. code-block:: python

    TH_TODOIST = {
        # get your credential by subscribing to
        # https://developer.todoist.com/appconsole.html
        'client_id': '<your todoist id>',
        'client_secret': '<your todoist secret>',
    }


creation of the table of the services
-------------------------------------

enter the following command

.. code-block:: bash

    python manage.py migrate


from the admin panel, activation of the service
-----------------------------------------------

from http://yourdomain.com/admin/django_th/servicesactivated/add/

* Select "Todoist",
* Set the Status to "Enabled"
* Check Auth Required: this will permit to redirect the user (or you) to Todoist website to confirm the access of the Todoist account
* Fill a description
