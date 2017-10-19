Mastodon
========

Service Description:
--------------------

Your self-hosted, globally interconnected microblogging community

User Guide
----------

Activation of the service from the page http://127.0.0.1:8000/th/service/add/

.. image:: https://github.com/foxmask/django-th/blob/master/docs/public_service_wallabag_add.png
   :alt: My Activated Services

then in the form, select Mastodon in the dropdown box, and fill all the fields with the information you can have from mastodon :

* in Nickname ; put your mastodon nickname
* in Password ; put your mastodon password
* in Client ID ; put the "Client key"
* in Client Secret ; put the "Client Secret"
* in the Host ; put the host of the mastodon instance

Then press "Activate it"


Installation Guide
------------------

Requesting a key
~~~~~~~~~~~~~~~~

On https://<your mastodon instance>/settings/applications/new fill the form and get the information to be used from the page of the activation of the service http://127.0.0.1:8000/th/service/add/


Configuration from the Admin panel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

http://127.0.0.1:8000/admin/django_th/servicesactivated/

.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/service_mastodon.png
    :target: https://joinmastodon.org/
    :alt: Mastdoon
