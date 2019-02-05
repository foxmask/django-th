JOPLIN
======

Service Description:
--------------------

An open source note taking and to-do application with synchronisation capabilities.

User Guide
----------

Activation of the service
~~~~~~~~~~~~~~~~~~~~~~~~~

From the page http://127.0.0.1:8000/th/service/

from the "Services available" part of the page, select Joplin and press "Activate it"

Defining a trigger
~~~~~~~~~~~~~~~~~~

with Joplin as consumer, when another service used as a provider.


Installation Guide
------------------

The Joplin Token
~~~~~~~~~~~~~~~~

open joplin and go to the menu `Tools > Webclipper options` to grab the token at the bottom of the page


The service keys
~~~~~~~~~~~~~~~~

Here are the modifications of .env file you will need to make to be able to use your credentials with Github

.. code-block:: python

    TH_JOPLIN_WEBCLIPPER = 'http://127.0.0.1:4881'
    TH_JOPLIN_TOKEN = ''

Configuration from the Admin panel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

http://127.0.0.1:8000/admin/django_th/servicesactivated/

add a new service and select Joplin. Then check .
