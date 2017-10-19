Pocket
======

Service Description:
--------------------

a "Read it Later" service

User Guide
----------

Activation of the service from the page http://127.0.0.1:8000/th/service/add/

.. image:: https://github.com/foxmask/django-th/blob/master/docs/public_service_wallabag_add.png
   :alt: My Activated Services

then in the form, select Pocket in the dropdown box and press "Activate it"


Installation Guide
------------------

Requesting a key
~~~~~~~~~~~~~~~~

On https://getpocket.com/developer/ , click on 'create a new app'

Fill the form and get the information that you will need to provide in the next paragraph


The service keys
~~~~~~~~~~~~~~~~

.. code-block:: python

    TH_POCKET_CONSUMER_KEY= 'your pocket key'

Configuration from the Admin panel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

http://127.0.0.1:8000/admin/django_th/servicesactivated/

.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/service_pocket.png
    :target: https://getpocket.com/
    :alt: Pocket
