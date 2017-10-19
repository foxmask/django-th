Trello
======

Service Description:
--------------------

a Kanban application

User Guide
----------

Activation of the service from the page http://127.0.0.1:8000/th/service/add/

.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/installation_guide/public_service_wallabag_add.png
   :alt: My Activated Services

then in the form, select Todoist in the dropdown box and press "Activate it"


Installation Guide
------------------

Requesting a key
~~~~~~~~~~~~~~~~

Once you are connected, go to https://trello.com/app-key


The service keys
~~~~~~~~~~~~~~~~

Here are the modifications of .env file you will need to make to be able to use your credentials with Trello

.. code-block:: python

    TH_TRELLO_CONSUMER_KEY= 'your trello key'
    TH_TRELLO_CONSUMER_SECRET= 'your trello secret'

Configuration from the Admin panel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

http://127.0.0.1:8000/admin/django_th/servicesactivated/

.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/installation_guide/service_trello.png
    :target: https://trello.com/
    :alt: Trello
