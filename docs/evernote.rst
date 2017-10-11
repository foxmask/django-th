Evernote
========

Service Description:
--------------------

This service allows to take notes, photos, schedules things and so on

modifications of settings.py
----------------------------

add or uncomment the following lines

.. code-block:: python

    INSTALLED_APPS = (
        # 'evernote',
        # 'th_evernote',
    )

to get

.. code-block:: python

    INSTALLED_APPS = (
        'evernote',
        'th_evernote',
    )


modifications of th_settings.py
-------------------------------

add or uncomment the following line

.. code-block:: python

    TH_SERVICES = (
        # 'th_evernote.my_evernote.ServiceEvernote',
    )

to get

.. code-block:: python

    TH_SERVICES = (
        'th_evernote.my_evernote.ServiceEvernote',
    )


The service keys
----------------

Here are the modifications of .env file you will need to do to be able to use your credentials with Evernote

.. code-block:: python

    TH_EVERNOTE_SANDBOX = False 
    TH_EVERNOTE_CONSUMER_KEY = 'your consumer key'
    TH_EVERNOTE_CONSUMER_SECRET =  'your consumer secret'


creation of the table of the services
-------------------------------------

enter the following command

.. code-block:: bash

    python manage.py migrate


from the admin panel, activation of the service
-----------------------------------------------

from http://yourdomain.com/admin/django_th/servicesactivated/add/

* Select "Evernote",
* Set the Status to "Enabled"
* Check Auth Required: this will permit to redirect the user (or you) to the Evernote website to confirm the access of the Evernote account
* Provide a description

