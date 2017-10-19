Tumblr
=======

Service Description:
--------------------

A Microblogging tool and social network

User Guide
----------

Activation of the service from the page http://127.0.0.1:8000/th/service/add/

.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/installation_guide/public_service_wallabag_add.png
   :alt: My Activated Services

then in the form, select Tumblr in the dropdown box and press "Activate it"


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

.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/installation_guide/service_tumblr.png
    :target: https://tumblr.com/
    :alt: Tumblr
