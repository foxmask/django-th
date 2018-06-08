Trello
======

Service Description:
--------------------

a Kanban application

User Guide
----------

Activation of the service
~~~~~~~~~~~~~~~~~~~~~~~~~

From the page http://127.0.0.1:8000/th/service/

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/public_services.png
   :alt: Services

from the "Services available" part of the page, select Trello and press "Activate it"


Defining a trigger
~~~~~~~~~~~~~~~~~~

with Trello as provider, when another service is used as a consumer

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/trello_provider_step1.png
    :alt: trello step 1

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/trello_provider_step2.png
    :alt: trello step 2

with Trello as consumer, when another service is used as a provider

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/trello_consumer_step3.png
    :alt: trello step 3

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/trello_consumer_step4.png
    :alt: trello step 4

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

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/service_trello.png
    :target: https://trello.com/
    :alt: Trello
