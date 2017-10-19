Pushbullet
==========

Service Description:
--------------------

Your devices working better together

Nota: to be able to work, this service requires that your host uses HTTPS

User Guide
----------

Activation of the service from the page http://127.0.0.1:8000/th/service/add/

.. image:: https://github.com/foxmask/django-th/blob/master/docs/public_service_wallabag_add.png
   :alt: My Activated Services

then in the form, select Pushbullet in the dropdown box and press "Activate it"


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

.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/service_pushbullet.png
    :target: https://pushbullet.com/
    :alt: pushbullet
