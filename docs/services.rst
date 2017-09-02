Services
========

This page cover the services that are handled by TriggerHappy, and will guide you through their installation

Common Process

For all the services, the installation is the same :

* modifications of settings.py
* creation of the table of the services (if needed)
* from the admin panel, activation of the service (if needed)


Activate the services
---------------------

to activate a service, you will need to follow those steps

* Requesting a key to the Services
* Adding the key to your settings file
* Adding the service from the Admin
* Activating the service from your account from the public part of the website
* Why this process ?


in details this gives us :


Requesting a key to the Services
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For each service, Trigger Happy expects to have some consumer key coming from the wanted service.
So for each service, you need to register an account on each of this service, then required a key.

You can have a look at the `README of Twitter <https://github.com/foxmask/django-th-twitter/blob/master/README.rst>`_, or `README of Pocket <https://github.com/foxmask/django-th-pocket/blob/master/README.rst>`_

Adding the key to the th_settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Once you own the keys., You add them to the th_settings.py file in

.. code-block:: python

    TH_<SERVICE_NAME> = (
        'consumer_key' => 'foobar',
        'consumer_token' => 'blabla'
    )

For example for Twitter :

.. code-block:: python

    TH_TWITTER = {
        'consumer_key': 'abcdefghijklmnopqrstuvwxyz',
        'consumer_secret': 'abcdefghijklmnopqrstuvwxyz',
    }

IMPORTANT :

With all the service you will enable, to avoid to share your key by accident, It's strongly recommended that you put all of them in a separate local_settings.py that you include at the end of the main settings.py


Adding the service from the Admin
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once you did **python manage.py migrate** and followed the standard process to bootstrap the application, go to the admin panel of the application.

Admin Home of Trigger Happy :

.. image:: https://foxmask.trigger-happy.eu/static/trigger_happy/admin_home.png


Admin list of activated services if Trigger Happy :

.. image:: https://foxmask.trigger-happy.eu/static/trigger_happy/admin_service_list.png


Admin Detail of one service of Trigger Happy :

.. image:: https://foxmask.trigger-happy.eu/static/trigger_happy/admin_service_details.png

Activating the service from your account from the public part of the website
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once your services are setup from the admin, you can go on the public part of the website and activate the service you need.

"My activated services" :

.. image:: https://foxmask.trigger-happy.eu/static/trigger_happy/public_services_activated.png

Why this process ?
~~~~~~~~~~~~~~~~~~

* it is simple : actually, to use Trigger Happy you need to install and host it by yourself, and so, you need to "declare" for each service your instance of TriggerHappy to the service provider.
* Other details : you need to activate the service from the admin panel, BECAUSE, TriggerHappy is planed to be used by many other users soon. So the admin of the instance of TriggerHappy will decide if he wants to offer the possibility to use this service of this other one. Once the admin has done his job, the end user, from the "public part" can go to the list of services and add the new one etc.


Supported services
------------------

Here are the service that will follow almost the same previous path

.. toctree::
   :maxdepth: 2

   evernote
   github
   instapush
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


