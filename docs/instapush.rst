Instapush
=========

Service Description:
--------------------

Notification service


modifications of settings.py
----------------------------

uncomment the following line

.. code-block:: python

    INSTALLED_APPS = (
        # 'th_instapsuh',
    )

to get

.. code-block:: python

    INSTALLED_APPS = (
        'th_instapsuh',
    )

modifications of th_settings.py
-------------------------------

uncomment the following line

.. code-block:: python

    TH_SERVICES = (
        # 'th_instapush.my_instapush.ServiceInstapush',
    )

to get

.. code-block:: python

    TH_SERVICES = (
        'th_instapush.my_instapush.ServiceInstapush',
    )


creation of the table of the services
-------------------------------------

enter the following command

.. code-block:: bash

    python manage.py migrate


from the admin panel, activation of the service
-----------------------------------------------

from http://yourdomain.com/admin/django_th/servicesactivated/add/

* Select "Instapush",
* Set the Status to "Enabled"
* Check Auth Required: do not check it
* Provide a description
