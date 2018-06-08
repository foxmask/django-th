Taiga
=====

Service Description:
--------------------

Taiga is a project management platform for agile developers & designers and project managers who want a beautiful tool that makes work truly enjoyable.

this app does not need any key, you need to have a Taiga account and being able to provide a webhook

this webhook can be defined from https://tree.taiga.io/project/<your account>-<your community>/admin/third-parties/webhooks

User Guide
----------

Activation of the service
~~~~~~~~~~~~~~~~~~~~~~~~~

From the page http://127.0.0.1:8000/th/service/

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/public_services.png
   :alt: Services

from the "Services available" part of the page, select Taiga, then set the username and password, the host, and press "Activate it"

Defining a trigger
~~~~~~~~~~~~~~~~~~

with Taiga as provider, when another service is used as a consumer

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/taiga_provider_step1.png
    :alt: taiga step 1

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/taiga_provider_step2.png
    :alt: taiga step 2

with Taiga as consumer, when another service is used as a provider

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/taiga_consumer_step3.png
    :alt: taiga step 3

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/taiga_consumer_step4.png
    :alt: taiga step 4

Installation Guide
------------------

Configuration from the Admin panel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

http://127.0.0.1:8000/admin/django_th/servicesactivated/

Check "auth required", and "self hosted", even if you plan to use taiga.io

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/service_taiga.png
    :target: https://taiga.io/
    :alt: Taiga
