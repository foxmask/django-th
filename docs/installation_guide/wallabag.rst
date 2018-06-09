Wallabag
========

Service Description:
--------------------

a self hostable application for saving web pages

.. image:: https://raw.githubusercontent.com/push-things/wallabag_api/master/wallabag.png

User Guide
----------

Activation of the service
~~~~~~~~~~~~~~~~~~~~~~~~~

From the page http://127.0.0.1:8000/th/service/

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/public_services.png
   :alt: Services

from the "Services available" part of the page, select Mastodon then fill all the fields with the information you can have from mastodon:

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/public_service_wallabag_settings.png

* in Username ; put your wallabag username
* in Password ; put your wallabag password
* in Client ID ; put the "Client key"
* in Client Secret ; put the "Client Secret"
* in the Host ; put the host of the wallabag instance

Then press "Activate it"


Installation Guide
------------------

Requesting a key
~~~~~~~~~~~~~~~~

Those will be required when activating the service for each user

Have a look at https://github.com/push-things/wallabag_api/blob/master/README.rst for more details about them


Configuration from the Admin panel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

http://127.0.0.1:8000/admin/django_th/servicesactivated/

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/public_service_wallabag_add.png
    :target: https://wallabag.org
    :alt: Wallabag
