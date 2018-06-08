Pocket
======

Service Description:
--------------------

a "Read it Later" service

User Guide
----------

Activation of the service
~~~~~~~~~~~~~~~~~~~~~~~~~

From the page http://127.0.0.1:8000/th/service/

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/public_services.png
   :alt: Services

from the "Services available" part of the page, select Pocket and press "Activate it"

Defining a trigger
~~~~~~~~~~~~~~~~~~

with Pocket as provider, when another service is used as a consumer

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/pocket_provider_step1.png
    :alt: pocket step 1

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/pocket_provider_step2.png
    :alt: pocket step 2

with Pocket as consumer, when another service is used as a provider

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/pocket_consumer_step3.png
    :alt: pocket step 3

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/pocket_consumer_step4.png
    :alt: pocket step 4


Installation Guide
------------------

Requesting a key
~~~~~~~~~~~~~~~~

On https://getpocket.com/developer/ , click on 'create a new app'

Fill the form and get the information that you will need to provide in the next paragraph


The service keys
~~~~~~~~~~~~~~~~

.. code-block:: python

    TH_POCKET_CONSUMER_KEY= 'your pocket key'

Configuration from the Admin panel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

http://127.0.0.1:8000/admin/django_th/servicesactivated/

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/service_pocket.png
    :target: https://getpocket.com/
    :alt: Pocket
