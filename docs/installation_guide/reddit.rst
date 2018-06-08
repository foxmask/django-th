Reddit
========

Service Description:
--------------------

The front page of internet

User Guide
----------

Activation of the service
~~~~~~~~~~~~~~~~~~~~~~~~~

From the page http://127.0.0.1:8000/th/service/

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/public_services.png
   :alt: Services

from the "Services available" part of the page, select Reddit and press "Activate it"


Defining a trigger
~~~~~~~~~~~~~~~~~~

with Reddit as provider, when another service is used as a consumer

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/reddit_provider_step1.png
    :alt: reddit step 1

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/reddit_provider_step2.png
    :alt: reddit step 2

with Reddit as consumer, when another service is used as a provider

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/reddit_consumer_step3.png
    :alt: reddit step 3

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/reddit_consumer_step4.png
    :alt: reddit step 4

Installation Guide
------------------

Requesting a key
~~~~~~~~~~~~~~~~

On https://dev.evernote.com/ at the top right of the page, click on 'get an api key'.

Fill the form and get the informations that you will need to provide in the next paragraph


The service keys
~~~~~~~~~~~~~~~~

Here are the modifications of .env file you will need to make to be able to use your credentials with Reddit

.. code-block:: python

    TH_REDDIT_CLIENT_ID='your consumer key'
    TH_REDDIT_CLIENT_SECRET='your consumer secret'
    TH_REDDIT_USER_AGENT=TriggerHappy:1.5.0 (by /u/push-things2)


Configuration from the Admin panel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

http://127.0.0.1:8000/admin/django_th/servicesactivated/

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/service_reddit.png
    :target: https://reddit.com/
    :alt: Reddit
