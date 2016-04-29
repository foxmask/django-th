==========
Quickstart
==========

We will say we start from scratch

Create a virtualenv
===================

We just create a virtualenv with python 3.4

.. code-block:: bash

    virtualenv --pytyhon=/usr/bin/python34 myproject
    cd $_
    source bin/activate


Install from GitHub
===================

We install TriggerHappy from Pypi

.. code-block:: bash

    git clone https://github.com/foxmask/django-th
    pip install  Django<1.9a django-formtools arrow==0.6.0 django-js-reverse django-redis requests-oauthlib feedparser

I dont want to use django 1.9 now, and arrow 0.7.0 got a very annoying bug for the project so 0.6.0 is important to get

Configuration
=============

edit local_settings.py and put the consumer_key of your pocket account (you can get from http://getpocket.com/api/docs):


.. code-block:: python

    TH_POCKET = {
        'consumer_key': 'abcdefghijklmnopqrstuvwxyz',
    }


Once the settings is done, enter the following command to sync the database :


.. code-block:: bash

    python manage.py migrate
    python manage.py createsuperuser


Start the application
=====================

.. code-block:: bash

    python manage.py runserver


Now open your browser and go to 127.0.0.1:8000/ to start using the application


Adding the service pocket from the Admin
========================================


Admin Home of Trigger Happy :

click add from

.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/admin_home.png


and fill the fields.

.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/admin_service_details.png


For the service RSS (dont check auth required) and Pocket (check auth required)


This will give something like :

.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/admin_service_list.png



Activating the service
=======================

Now that the 2 service RSS and Pocket are enabled, go activate them for you :

"My activated services" :

.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/public_services_activated.png


Why this process from admin and non admin part ?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* The project is hosted by yourself for your own need, but the project is able to handle trigger for your and your friends if you need.
* Thus the 'admin' who hosts the project need to do some work of his admin part to add the service he will offer to user
* Thus the user will go the his "my activated services" page to activate his service too.
* But as you are all alone for the moment, you have the two hats : admin and end user, this is why you will need to do the two steps "Adding the service pocket from the Admin" and
"Activating the service"
