==========
Quickstart
==========

We will say we start from scratch.
Assuming you already have python3.6 installed, with redis too.


Create a virtualenv
===================

We just create a virtualenv with python 3.6 (or 3.5)

.. code-block:: bash

    python3.6 -m venv myproject
    cd $_
    source bin/activate


Install from GitHub
===================

We install Trigger-Happy from Pypi

.. code-block:: bash

    git clone https://github.com/foxmask/django-th.git
    cd django-th
    pip install -e .[min]


Database
========


.. code-block:: bash

    python manage.py migrate
    python manage.py createsuperuser

You may choose to load the initial services:

.. code-block:: bash

    python manage.py loaddata initial_services

Start the application
=====================

.. code-block:: bash

    python manage.py runserver &


Now open your browser and go to http://127.0.0.1:8000/th/ to start using the application


Adding the service Wallabag from the Admin
==========================================


Admin Home of Trigger Happy :

click add from

.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/admin_home.png


and fill the fields.

.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/admin_service_details.png


For the service RSS (dont check auth required) and Wallabag (check auth required)


This will give something like :

.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/admin_service_list.png



Activating the service
=======================

Now that the 2 service RSS and Wallabag are enabled, go activate them for you :

"Activated services" (http://127.0.0.1:8000/th/service/):

.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/public_services_activated.png


Why this process from admin and non admin part ?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* The project is hosted by yourself for your own need, but the project is able to handle trigger for your and your friends if you need.
* Thus the 'admin' who hosts the project need to do some work of his admin part to add the service he will offer to user
* Thus the user will go the his "my activated services" page to activate his service too.
* But as you are all alone for the moment, you have the two hats : admin and end user, this is why you will need to do the two steps "Adding the service wallabag from the Admin" and "Activating the service"

Create a trigger
================

Once all of this is done, go back to the main page http://127.0.0.1:8000/th/ and create your first trigger
