Twitter
=======

Service Description:
--------------------

a Social Network

User Guide
----------

Activation of the service
~~~~~~~~~~~~~~~~~~~~~~~~~

From the page http://127.0.0.1:8000/th/service/

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/public_services.png
   :alt: Services

from the "Services available" part of the page, select Twitter and press "Activate it"


Defining a trigger
~~~~~~~~~~~~~~~~~~

with Twitter as provider, when another service is used as a consumer

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/twitter_provider_step1.png
    :alt: twitter step 1

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/twitter_provider_step2.png
    :alt: twitter step 2

with Twitter as consumer, when another service is used as a provider

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/twitter_consumer_step3.png
    :alt: twitter step 3

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/twitter_consumer_step4.png
    :alt: twitter step 4

if you tick the "fav" checkbox, this will allow you to "save" the tweet to another service, for example to Wallabag, to be read later.

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

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/service_twitter.png
    :target: https://twitter.com/
    :alt: Twitter
