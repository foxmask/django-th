Pocket
======

Service Description:
--------------------

a "Read it Later" service

modifications of settings.py
----------------------------

add or uncomment the following line

.. code-block:: python

    INSTALLED_APPS = (
        # 'th_pocket',
    )

to get

.. code-block:: python

    INSTALLED_APPS = (
        'th_pocket',
    )


modifications of th_settings.py
-------------------------------

uncomment the following line

.. code-block:: python

    TH_SERVICES = (
        # 'th_pocket.my_pocket.ServicePocket',
    )

to get

.. code-block:: python

    TH_SERVICES = (
        'th_pocket.my_pocket.ServicePocket',
    )


The service keys
----------------

Here are the modifications of .env file you will need to do to be able to use your credentials with Pocket

.. code-block:: python

    TH_POCKET_CONSUMER_KEY= 'your pocket key'


creation of the table of the services
-------------------------------------

enter the following command

.. code-block:: bash

    python manage.py migrate


from the admin panel, activation of the service
-----------------------------------------------

from http://yourdomain.com/admin/django_th/servicesactivated/add/

* Select "Pocket",
* Set the Status to "Enabled"
* Check Auth Required: this will enable redirection of the user (or you) to Pocket website to confirm the access of the Pocket account
* Provide a description

