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

From the page http://127.0.0.1:8000/th/service/add/

.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/installation_guide/public_service_wallabag_add.png
   :alt: My Activated Services

then in the form, select Taiga in the dropdown box and press "Activate it"

Defining a trigger
~~~~~~~~~~~~~~~~~~

with Taiga as consumer, when another service is used as a provider

.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/installation_guide/taiga_consumer_step3.png
    :alt: taiga step 3

.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/installation_guide/taiga_consumer_step4.png
    :alt: taiga step 4

with Taiga as provider, when another service is used as a consumer

.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/installation_guide/taiga_provider_step1.png
    :alt: taiga step 1

.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/installation_guide/taiga_provider_step2.png
    :alt: taiga step 2

Installation Guide
------------------

Configuration from the Admin panel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

http://127.0.0.1:8000/admin/django_th/servicesactivated/

.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/installation_guide/service_taiga.png
    :target: https://taiga.io/
    :alt: Taiga
