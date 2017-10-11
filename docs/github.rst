GitHub
======

Service Description:
--------------------

Powerful collaboration, code review, and code management for open source and private projects. Public projects are always free.

modifications of settings.py
----------------------------

add or uncomment the following line

.. code-block:: python

    INSTALLED_APPS = (
        # 'th_github',
    )

to get

.. code-block:: python

    INSTALLED_APPS = (
        'th_github',
    )

modifications of th_settings.py
-------------------------------

add or uncomment the following line

.. code-block:: python

    TH_SERVICES = (
        # 'th_github.my_github.ServiceGithub',
    )

to get

.. code-block:: python

    TH_SERVICES = (
        'th_github.my_github.ServiceGithub',
    )


The service keys
----------------

Here are the modifications of .env file you will need to do to be able to use your credentials with Github

.. code-block:: python

    TH_GITHUB = {
        TH_GITHUB_USERNAME= 'username'
        TH_GITHUB_PASSWORD= 'password'
        TH_GITHUB_CONSUMER_KEY= 'your consumer key'
        TH_GITHUB_CONSUMER_SECRET= 'your consumer secret'
    }

creation of the table of the services
-------------------------------------

enter the following command

.. code-block:: bash

    python manage.py migrate


from the admin panel, activation of the service
-----------------------------------------------

from http://yourdomain.com/admin/django_th/servicesactivated/add/

* Select "GitHub",
* Set the Status to "Enabled"
* Check Auth Required: this will permit to redirect the user (or you) to GitHub website to confirm the access of the GitHub account
* Provide a description

