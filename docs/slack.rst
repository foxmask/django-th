Slack
=====

Service Description:
--------------------

A messaging app for teams who put robots on Mars

modifications of settings.py
----------------------------

1) INSTALLED_APPS :

add or uncomment the following line

.. code-block:: python

    INSTALLED_APPS = (
        # 'th_slack',
    )

to get

.. code-block:: python

    INSTALLED_APPS = (
        'th_slack',
    )

modifications of th_settings.py
-------------------------------

1) TH_SERVICES

add or uncomment the following line

.. code-block:: python

    TH_SERVICES = (
        # 'th_slack.my_slack.ServiceSlack',
    )

to get

.. code-block:: python

    TH_SERVICES = (
        'th_slack.my_slack.ServiceSlack',
    )

creation of the table of the services
-------------------------------------

enter the following command

.. code-block:: bash

    python manage.py migrate


from the admin panel, activation of the service
-----------------------------------------------

from http://yourdomain.com/admin/django_th/servicesactivated/add/

* Select "Slack",
* Set the Status to "Enabled"
* Fill a description
