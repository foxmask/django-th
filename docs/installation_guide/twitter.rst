Twitter
=======

Service Description:
--------------------

a Social Network

User Guide
----------

Activation of the service from the page http://127.0.0.1:8000/th/service/add/

.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/installation_guide/public_service_wallabag_add.png
   :alt: My Activated Services

then in the form, select Twitter in the dropdown box and press "Activate it"


Installation Guide
------------------

Requesting a key
~~~~~~~~~~~~~~~~

Access the page https://apps.twitter.com/app/new

* in the field "WebSite", set https://<yourdomain.com>
* in the field "Callback URL", set https://<yourdomain.com>/th/callbacktwitter

then validate and grab the key on the next page

The service keys
~~~~~~~~~~~~~~~~

Here are the modifications of .env file you will need to make to be able to use your credentials with Twitter

.. code-block:: python

    TH_TWITTER_CONSUMER_KEY= 'your twitter key'
    TH_TWITTER_CONSUMER_SECRET= 'your twitter secret'

Configuration from the Admin panel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

http://127.0.0.1:8000/admin/django_th/servicesactivated/

.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/installation_guide/service_twitter.png
    :target: https://twitter.com/
    :alt: Twitter
