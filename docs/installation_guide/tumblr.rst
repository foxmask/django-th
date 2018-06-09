Tumblr
=======

Service Description:
--------------------

A Microblogging tool and social network

User Guide
----------

Activation of the service
~~~~~~~~~~~~~~~~~~~~~~~~~

From the page http://127.0.0.1:8000/th/service/

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/public_services.png
   :alt: Services

from the "Services available" part of the page, select Tumblr and press "Activate it"


Defining a trigger
~~~~~~~~~~~~~~~~~~

with Tumblr as provider, when another service is used as a consumer

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/tumblr_provider_step1.png
    :alt: tumblr step 1

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/tumblr_provider_step2.png
    :alt: tumblr step 2

with Tumblr as consumer, when another service is used as a provider

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/tumblr_consumer_step3.png
    :alt: tumblr step 3

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/tumblr_consumer_step4.png
    :alt: tumblr step 4

Installation Guide
------------------

Requesting a key
~~~~~~~~~~~~~~~~

Once you are connected, go to https://www.tumblr.com/oauth/apps

The service keys
~~~~~~~~~~~~~~~~

Here are the modifications of .env file you will need to make to be able to use your credentials with Tumblr

.. code-block:: python

    TH_TUMBLR_CONSUMER_KEY= 'your tumblr key'
    TH_TUMBLR_CONSUMER_SECRET= 'your tumblr secret'

Configuration from the Admin panel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

http://127.0.0.1:8000/admin/django_th/servicesactivated/

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/service_tumblr.png
    :target: https://tumblr.com/
    :alt: Tumblr
