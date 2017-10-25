Pushbullet
==========

Service Description:
--------------------

Your devices working better together

Nota: to be able to work, this service requires that your host uses HTTPS

User Guide
----------

Activation of the service
~~~~~~~~~~~~~~~~~~~~~~~~~

From the page http://127.0.0.1:8000/th/service/

.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/installation_guide/public_services.png
   :alt: Services

from the "Services available" part of the page, select Pushbullet and press "Activate it"


Defining a trigger
~~~~~~~~~~~~~~~~~~

with Pushbullet as provider, when another service is used as a consumer

.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/installation_guide/pushbullet_provider_step1.png
    :alt: pushbullet step 1

.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/installation_guide/pushbullet_provider_step2.png
    :alt: pushbullet step 2

with Pushbullet as consumer, when another service is used as a provider

.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/installation_guide/pushbullet_consumer_step3.png
    :alt: pushbullet step 3

.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/installation_guide/pushbullet_consumer_step4.png
    :alt: pushbullet step 4


Installation Guide
------------------

Requesting a key
~~~~~~~~~~~~~~~~

On https://www.pushbullet.com/#settings/account

Fill the form and get the informations that you will need to provide in the next paragraph


The service keys
~~~~~~~~~~~~~~~~

Here are the modifications of .env file you will need to do to be able to use your credentials with Pushbullet

.. code-block:: python

    TH_PUSHBULLET_CLIENT_ID= 'your pushbulet id'
    TH_PUSHBULLET_CLIENT_SECRET= 'your pushbulet secret'

Configuration from the Admin panel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

http://127.0.0.1:8000/admin/django_th/servicesactivated/

.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/installation_guide/service_pushbullet.png
    :target: https://pushbullet.com/
    :alt: pushbullet
