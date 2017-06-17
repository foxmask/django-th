Taiga
=====

Service Description:
--------------------

Taiga is a project management platform for agile developers & designers and project managers who want a beautiful tool that makes work truly enjoyable.

modifications of settings.py
----------------------------

1) INSTALLED_APPS :

add or uncomment the following line

.. code-block:: python

    INSTALLED_APPS = (
        # 'th_taiga',
    )

to get

.. code-block:: python

    INSTALLED_APPS = (
        'th_taiga',
    )

modifications of th_settings.py
-------------------------------

1) TH_SERVICES

add or uncomment the following line

.. code-block:: python

    TH_SERVICES = (
        # 'th_taiga.my_taiga.ServiceTaiga',
    )

to get

.. code-block:: python

    TH_SERVICES = (
        'th_taiga.my_taiga.ServiceTaiga',
    )

creation of the table of the services
-------------------------------------

enter the following command

.. code-block:: bash

    python manage.py migrate


from the admin panel, activation of the service
-----------------------------------------------

from http://yourdomain.com/admin/django_th/servicesactivated/add/

* Select "Taiga",
* Set the Status to "Enabled"
* Fill a description
