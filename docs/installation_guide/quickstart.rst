==========
Quickstart
==========

Requirements:

* Python 3.6
* Redis

for installing redis, on Linux,

.. code-block:: bash

    apt-get install redis

or

.. code-block:: bash

    yum install redis

for installing redis on macosx: 

.. code-block:: bash

    brew install redis


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
    pip install -e .


Database
========


.. code-block:: bash

    python manage.py migrate
    python manage.py createsuperuser

Load the initial services:

.. code-block:: bash

    python manage.py loaddata initial_services

Start the application
=====================

.. code-block:: bash

    python manage.py runserver &


Now open your browser and go to http://127.0.0.1:8000/th/ to start using the application by logged in


Activating the service
=======================

Go to activate the (at least) 2 services you plan to use:

"Activated services" (http://127.0.0.1:8000/th/service/):

.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/public_services_activated.png

1rst Service

* Select Rss and validate

2nd Service

* Select Wallabag and fill the fields that are required with the parameters, can find in then page http://your-wallabag-instance/developer and validate


Create a trigger: in 5 steps
============================

Once all of this is done, go back to the main page http://127.0.0.1:8000/th/ and create your first trigger

* Step One:

Select Rss

* Step 2:

enter the RSS URL that provide the data you want to grab

* Step 3:

Select Wallabag

* Step 4:

Set a tag (if you need)

* Step 5:

Set a description that will be displayed in the list of your triggers

Turn the engine on:
===================

Now that everything is setup, you can run the following commands:

.. code-block:: bash

    python manage.py read


.. code-block:: bash

    python manage.py publish

the first one, will read of the triggers that are enabled (with the blue "on/off" switch), and will download the data related to each of them, and will put them in the cache (available with Redis)

The second one, will read the data from the cache, and will publish them on Wallabag.


Once all of this is ok, you could automate this commands with :ref:`crontab` later


Have Fun, and happy automation ;-)
