Trello
======

Service Description:
--------------------

a Kanban application

modifications of settings.py
----------------------------

add or uncomment the following line

.. code-block:: python

    INSTALLED_APPS = (
        # 'th_trello',
    )

to get

.. code-block:: python

    INSTALLED_APPS = (
        'th_trello',
    )


modifications of th_settings.py
-------------------------------

add or uncomment the following line

.. code-block:: python

    TH_SERVICES = (
        # 'th_trello.my_trello.ServiceTrello',
    )

to get

.. code-block:: python

    TH_SERVICES = (
        'th_trello.my_trello.ServiceTrello',
    )


The service keys
----------------

Here are the modifications of .env file you will need to do to be able to use your credentials with Trello

.. code-block:: python

    TH_TRELLO_CONSUMER_KEY= 'your trello key'
    TH_TRELLO_CONSUMER_SECRET= 'your trello secret'
   
creation of the table of the services
-------------------------------------

enter the following command

.. code-block:: bash

    python manage.py migrate


from the admin panel, activation of the service
-----------------------------------------------

from http://yourdomain.com/admin/django_th/servicesactivated/add/

* Select "Trello",
* Set the Status to "Enabled"
* Check Auth Required: this will permit to redirect the user (or you) to Trello website to confirm the access of the Trello account
* Fill a description



