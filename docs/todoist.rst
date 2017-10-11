Todoist
=======

Service Description:
--------------------

a Tasks Managements

Nota : to be able to work, this service requires that your host uses HTTPS

modifications of settings.py
----------------------------

add or uncomment the following line

.. code-block:: python

    INSTALLED_APPS = (
        # 'th_todoist',
    )

to get

.. code-block:: python

    INSTALLED_APPS = (
        'th_todoist',
    )


modifications of th_settings.py
-------------------------------

add or uncomment the following line

.. code-block:: python

    TH_SERVICES = (
        # 'th_todoist.my_todoist.ServiceTodoist',
    )

to get

.. code-block:: python

    TH_SERVICES = (
        'th_todoist.my_todoist.ServiceTodoist',
    )

The service keys
----------------

Here are the modifications of .env file you will need to do to be able to use your credentials with Todoist

.. code-block:: python

    TH_TODOIST_CLIENT_ID= 'your todoist id'
    TH_TODOIST_CLIENT_SECRET= 'your todoist secret'


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
