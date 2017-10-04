Mastodon
========

Service Description:
--------------------

Your self-hosted, globally interconnected microblogging community

modifications of settings.py
----------------------------

1) INSTALLED_APPS :

add or uncomment the following line

.. code-block:: python

    INSTALLED_APPS = (
        # 'th_mastodon',
    )

to get

.. code-block:: python

    INSTALLED_APPS = (
        'th_mastodon',
    )

modifications of th_settings.py
-------------------------------

1) TH_SERVICES

add or uncomment the following line

.. code-block:: python

    TH_SERVICES = (
        # 'th_mastodon.my_mastodon.ServiceMastdoon',
    )

to get

.. code-block:: python

    TH_SERVICES = (
        'th_mastodon.my_mastodon.ServiceMastdoon',
    )

creation of the table of the services
-------------------------------------

enter the following command

.. code-block:: bash

    python manage.py migrate


from the admin panel, activation of the service
-----------------------------------------------

from http://yourdomain.com/admin/django_th/servicesactivated/add/

* Select "Mastodon",
* Set the Status to "Enabled"
* Check Auth Required: this will permit to redirect the user (or you) to Mastodon website to confirm the access of the Mastodon account
* Fill a description to something like "Your self-hosted, globally interconnected microblogging community"
