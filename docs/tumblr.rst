Tumblr
=======

Service Description:
--------------------

A Microblogging and social network

modifications of settings.py
----------------------------

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


modifications of th_settings.py
-------------------------------

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

The service keys
----------------

Here are the modifications of .env file you will need to do to be able to use your credentials with Tumblr

.. code-block:: python

    TH_TUMBLR_CONSUMER_KEY= 'your tumblr key'
    TH_TUMBLR_CONSUMER_SECRET= 'your tumblr secret'


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
