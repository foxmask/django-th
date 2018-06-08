RSS
===

Service Description:
--------------------

Service that grabs RSS all around the web or creates also RSS from other services

User Guide
----------

Activation of the service
~~~~~~~~~~~~~~~~~~~~~~~~~

From the page http://127.0.0.1:8000/th/service/

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/public_services.png
   :alt: Services

from the "Services available" part of the page, select RSS and press "Activate it"


Defining a trigger
~~~~~~~~~~~~~~~~~~

with RSS as provider, when another service is used as a consumer

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/rss_provider_step1.png
    :alt: rss step 1

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/rss_provider_step2.png
    :alt: rss step 2

with RSS as consumer, when another service is used as a provider

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/rss_consumer_step3.png
    :alt: rss step 3

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/rss_consumer_step4.png
    :alt: rss step 4

Yes RSS can be used as a consumer. That way, Trigger Happy will generate a RSS Feeds from the provider of your choice.
Then you can access to the feeds by http://127.0.0.1:8000/th/myfeeds/. This can be useful for service that don't provide RSS or ATOM feeds like Twitter.


Installation Guide
------------------

Configuration from the Admin panel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/service_rss.png
    :alt: rss
