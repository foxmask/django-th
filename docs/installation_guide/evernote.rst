Evernote
========

Service Description:
--------------------

This service allows to take notes, photos, schedule things and so on

User Guide
----------

Activation of the service
~~~~~~~~~~~~~~~~~~~~~~~~~

From the page http://127.0.0.1:8000/th/service/

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/public_services.png
   :alt: Services

from the "Services available" part of the page, select Evernote and press "Activate it"

Defining a trigger
~~~~~~~~~~~~~~~~~~

with Evernote as provider, when another service is used as a consumer

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/evernote_provider_step1.png
    :alt: evernote step 1

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/evernote_provider_step2.png
    :alt: evernote step 2

with Evernote as consumer, when another service is used as a provider

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/evernote_consumer_step3.png
    :alt: evernote step 3

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/evernote_consumer_step4.png
    :alt: evernote step 4

Installation Guide
------------------

Requesting a key
~~~~~~~~~~~~~~~~

On https://dev.evernote.com/ at the top right of the page, click on 'get an api key'.

Fill the form and get the informations that you will need to provide in the next paragraph


The service keys
~~~~~~~~~~~~~~~~

Here are the modifications of .env file you will need to make to be able to use your credentials with Evernote

.. code-block:: python

    TH_EVERNOTE_SANDBOX = False
    TH_EVERNOTE_CONSUMER_KEY = 'your consumer key'
    TH_EVERNOTE_CONSUMER_SECRET =  'your consumer secret'


Configuration from the Admin panel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

http://127.0.0.1:8000/admin/django_th/servicesactivated/

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/service_evernote.png
    :target: https://evernote.com/
    :alt: Evernote
