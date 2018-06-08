Todoist
=======

Service Description:
--------------------

a Tasks Management tool

Nota: to be able to work, this service requires that your host uses HTTPS

User Guide
----------

Activation of the service
~~~~~~~~~~~~~~~~~~~~~~~~~

From the page http://127.0.0.1:8000/th/service/

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/public_services.png
   :alt: Services

from the "Services available" part of the page, select Todoist and press "Activate it"


Defining a trigger
~~~~~~~~~~~~~~~~~~

with Todoist as provider, when another service is used as a consumer

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/todoist_provider_step1.png
    :alt: todoist step 1

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/todoist_provider_step2.png
    :alt: todoist step 2

with Todoist as consumer, when another service is used as a provider

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/todoist_consumer_step3.png
    :alt: todoist step 3

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/todoist_consumer_step4.png
    :alt: todoist step 4

Installation Guide
------------------

Requesting a key
~~~~~~~~~~~~~~~~

On https://api.todoist.com/app?lang=fr#start select "generate a new api key"


The service keys
~~~~~~~~~~~~~~~~

Here are the modifications of .env file you will need to make to be able to use your credentials with Todoist

.. code-block:: python

    TH_TODOIST_CLIENT_ID= 'your todoist id'
    TH_TODOIST_CLIENT_SECRET= 'your todoist secret'


Configuration from the Admin panel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

http://127.0.0.1:8000/admin/django_th/servicesactivated/

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/service_todoist.png
    :target: https://todoist.com/
    :alt: Todoist
