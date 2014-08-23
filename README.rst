====================
Django Trigger Happy
====================

Automatically share data between popular services you use on the web.
And instead of giving your credentials to them, become the owner of yours !

For example a new RSS item is published, django-trigger-happy will be able to 
automatically create a note on your Evernote account or create a bookmark to
your own Readability or Pocket account and so on

|ImageLink|_

.. |ImageLink| image:: https://drone.io/github.com/foxmask/django-th/status.png
.. _ImageLink: https://drone.io/github.com/foxmask/django-th/status.png
.. |ImageLink| image:: http://foxmask.info/public/trigger_happy/trigger_happy_small.png


Description:
============
The goal of this project is to be independant from any other solution like 
IFTTT, CloudWork or others.

Thus you could host your own solution and manage your own triggers without 
depending any non-free solution.

With this project you can host triggers for you.

All you need is to have a hosting provider (or simply your own server ;) 
who permits to use a manager of tasks like "cron" and, of course Python

Requirements :
==============
* Python 3.4.0, sould be ok with 2.7.x
* Django > 1.6
* django-th-rss >= 0.3.0
* django-th-pocket >= 0.2.0

Installation:
=============
to get the project, from your virtualenv, do :

.. code: system

    git clone https://github.com/foxmask/django-th.git

to add the needed modules , do :

.. code:: python

    pip install -r https://github.com/foxmask/django-th/blob/master/django_th/requirements.txt

and at least :

.. code:: python

    python manage.py syncdb

to startup the database

Parameters :
============
As usual you will setup the database parameters.

Important parts are the settings of the available services :

Settings.py 
-----------

add the module django_th to the INSTALLED_APPS


.. code:: python

    INSTALLED_APPS = (
        'django_th',
        'th_rss',
        'th_pocket',
    )

TH_SERVICES
~~~~~~~~~~~

TH_SERVICES is a list of the services we, like for example,  

.. code:: python

    TH_SERVICES = (
        'th_rss.my_rss.ServiceRss',
        'th_pocket.my_pocket.ServicePocket',
    )

If you plan to integrate django_th in an existing project then, to deal with the templates and avoid the TemplateDoesNotExist error you can 
copy the template in your own templates directory or set the path like this :

.. code:: python

    import os
    PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
    TEMPLATE_DIRS += (
        PROJECT_DIR + '/../../lib/<python-version>/site-package/django_th/templates/',
    )

also you'll need to look at the urls.py of django_th to copy a lot of existing the mapping.


Setting up : Administration
===========================

once the module is installed, go to the admin panel and activate the service you want. 
Currently there are 4 services, RSS, Evernote, Pocket and Readability.

All you can decide here is to tell if the service requires an external authentication or not.

Once they are activated. User can use them.


Usage :
=======

Activating services : 
---------------------

The user activates the service for their own need. If the service requires an external authentication, he will be redirected to the service which will ask him the authorization to acces the user's account. Once it's done, goes back to django-trigger-happy to finish and record the "auth token".

Using the activated services :
------------------------------

a set of 3 pages will ask to the user information that will permit to trigger data from a service "provider" to a service "consummer".

For example : 

* page 1 : the user gives a RSS feed
* page 2 : the user gives the name of the notebook where notes will be stored and a tag if he wants
* page 3 : the user gives a description


Fire the Triggers :
===================
To start handling the queue of triggers you/your users configured, just set the fire.py in a crontab or any other scheduler solution of your choice.
Keep in mind to avoid to set a too short duration between 2 run to avoid to be blocked by the externals services (by their rate limitation)  you/your users want to reach.

Blog posts : 
===========
You can find all details of all existing services of the blog :
http://www.foxmask.info/tag/TriggerHappy
