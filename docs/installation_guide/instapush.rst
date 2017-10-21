Instapush
=========

Service Description:
--------------------

Notification service

User Guide
----------

Activation of the service
~~~~~~~~~~~~~~~~~~~~~~~~~

From the page http://127.0.0.1:8000/th/service/add/

.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/installation_guide/public_service_wallabag_add.png
   :alt: My Activated Services

then in the form, select Instapush in the dropdown box then in the form, just fill the user token, then press "Activate it"

with Instapush as consumer, when another service is used as a provider

.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/installation_guide/instapush_consumer_step3.png
    :alt: instapush step 3

.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/installation_guide/instapush_consumer_step4.png
    :alt: instapush step 4

instapush is not used as provider as it's just send notification from others data

Installation Guide
------------------

Requesting a key
~~~~~~~~~~~~~~~~

Configuration from the Admin panel
----------------------------------

http://127.0.0.1:8000/admin/django_th/servicesactivated/

.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/installation_guide/service_instapush.png
    :target: https://instapush.im/
    :alt: Instapush
