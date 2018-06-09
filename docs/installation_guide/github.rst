GitHub
======

Service Description:
--------------------

Powerful collaboration, code review, and code management for open source and private projects. Public projects are always free.

User Guide
----------

Activation of the service
~~~~~~~~~~~~~~~~~~~~~~~~~

From the page http://127.0.0.1:8000/th/service/

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/public_services.png
   :alt: Services

from the "Services available" part of the page, select Github and press "Activate it"

Defining a trigger
~~~~~~~~~~~~~~~~~~

with Github as provider, when another service is used as a consumer

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/github_provider_step1.png
    :alt: github step 1

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/github_provider_step2.png
    :alt: github step 2

with Github as consumer, when another service is used as a provider

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/github_consumer_step3.png
    :alt: github step 3

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/github_consumer_step4.png
    :alt: github step 4

Installation Guide
------------------

Requesting a key
~~~~~~~~~~~~~~~~

On https://github.com/settings/developers, click on "New Oauth App" button at right.

Fill the form and get the informations that you will need to provide in the next paragraph


The service keys
~~~~~~~~~~~~~~~~

Here are the modifications of .env file you will need to make to be able to use your credentials with Github

.. code-block:: python

    TH_GITHUB_USERNAME= 'username'
    TH_GITHUB_PASSWORD= 'password'
    TH_GITHUB_CONSUMER_KEY= 'your consumer key'
    TH_GITHUB_CONSUMER_SECRET= 'your consumer secret'

Configuration from the Admin panel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

http://127.0.0.1:8000/admin/django_th/servicesactivated/

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/service_github.png
    :target: https://github.com/
    :alt: Github
