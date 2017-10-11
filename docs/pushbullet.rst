Pushbullet
==========

Service Description:
--------------------

Your devices working better together

Nota : to be able to work, this service requires that your host uses HTTPS

modifications of settings.py
----------------------------

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

modifications of th_settings.py
-------------------------------

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

The service keys
----------------

Here are the modifications of .env file you will need to do to be able to use your credentials with Pushbullet

.. code-block:: python

    TH_PUSHBULLET_CLIENT_ID= 'your pushbulet id'
    TH_PUSHBULLET_CLIENT_SECRET= 'your pushbulet secret'

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
