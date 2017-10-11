Twitter
=======

Service Description:
--------------------

a Social Network

modifications of settings.py
----------------------------

add or uncomment the following line

.. code-block:: python

    INSTALLED_APPS = (
        # 'th_twitter',
    )

to get

.. code-block:: python

    INSTALLED_APPS = (
        'th_twitter',
    )

modifications of th_settings.py
-------------------------------


add or uncomment the following line

.. code-block:: python

    TH_SERVICES = (
        # 'th_twitter.my_twitter.ServiceTwitter',
    )

to get

.. code-block:: python

    TH_SERVICES = (
        'th_twitter.my_twitter.ServiceTwitter',
    )

The service keys
----------------

Here are the modifications of .env file you will need to do to be able to use your credentials with Twitter

.. code-block:: python

    TH_TWITTER_CONSUMER_KEY= 'your twitter key'
    TH_TWITTER_CONSUMER_SECRET= 'your twitter secret'


creation of the table of the services
-------------------------------------

enter the following command

.. code-block:: bash

    python manage.py migrate


from the admin panel, activation of the service
-----------------------------------------------

from http://yourdomain.com/admin/django_th/servicesactivated/add/

* Select "Twitter",
* Set the Status to "Enabled"
* Check Auth Required: this will permit to redirect the user (or you) to Twitter website to confirm the access of the Twitter account
* Fill a description
