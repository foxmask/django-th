.. _services:

Services
========

This page covers the services that are handled by TriggerHappy, and will guide you through their installation

Activate the services
---------------------

to activate a service, you will need to follow those steps

* Requesting a key to the Services
* Adding the key to your .env file
* Activating the service from http://127.0.0.1:8000/th/service/add/


in details this gives us:


Requesting a key to the Services
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For each service, Trigger Happy expects to have some consumer key coming from the wanted service.
So you need to register an account on each of the services, then require a key.


Adding the key to the .env file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    TH_<SERVICE_NAME>_CONSUMER_KEY = 'your key'
    TH_<SERVICE_NAME>_CONSUMER_SECRET = 'your secret'

For example for Twitter:

.. code-block:: python

    TH_TWITTER_CONSUMER_KEY = 'abcdefghijklmnopqrstuvwxyz',
    TH_TWITTER_CONSUMER_SECRET = 'abcdefghijklmnopqrstuvwxyz',


Activate the service
~~~~~~~~~~~~~~~~~~~~

From the page http://127.0.0.1:8000/th/service/add/


Disable an existing service from the admin panel
------------------------------------------------

From this page http://127.0.0.1:8000/admin/django_th/servicesactivated/, select the service(s) you don't need and in the action dropdown choose 'Status disable'
Thus, the service(s) won't be available for anyone.


Supported services
------------------

Here are the services that will follow almost the same previous path

.. toctree::
   :maxdepth: 2

   evernote
   github
   instapush
   mastodon
   pelican
   pocket
   pushbullet
   rss
   slack
   taiga
   todoist
   trello
   tumblr
   twitter
   wallabag


