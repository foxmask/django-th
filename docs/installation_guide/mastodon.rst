Mastodon
========

Service Description:
--------------------

Your self-hosted, globally interconnected microblogging community

User Guide
----------

Activation of the service
~~~~~~~~~~~~~~~~~~~~~~~~~

From the page http://127.0.0.1:8000/th/service/

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/public_services.png
   :alt: Services

from the "Services available" part of the page, select Mastodon then fill all the fields with the information you can have from mastodon:

* in Nickname ; put your mastodon nickname
* in Password ; put your mastodon password
* in Client ID ; put the "Client key"
* in Client Secret ; put the "Client Secret"
* in the Host ; put the host of the mastodon instance

Then press "Activate it"


Defining a trigger
~~~~~~~~~~~~~~~~~~

with Mastodon as provider, when another service is used as a consumer

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/mastodon_provider_step1.png
    :alt: mastodon step 1

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/mastodon_provider_step2.png
    :alt: mastodon step 2

with Mastodon as consumer, when another service is used as a provider

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/mastodon_consumer_step3.png
    :alt: mastodon step 3

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/mastodon_consumer_step4.png
    :alt: mastodon step 4

if you tick the "fav" checkbox, this will allow you to "save" the toot to another service, for example to Wallabag, to be read later.

Installation Guide
------------------

Requesting a key
~~~~~~~~~~~~~~~~

1) on the "new" page (https://<your mastodon instance>/settings/applications/new), fill `application name`, `application url`, `redirect uri`

the redirect uri is

    https://<your trigger happy instance>/th/callbackmastodon


2) once the page is validated, we can get the client_key and client_secret by editing the application  we created at step 1. Those two data will be needed in the form of the activation of the mastodon service

3) activation of the mastodon service

*  `username` is the email you used when you registered to your mastodon instance
*  `password` is your mastodon password
*  `client_ key` is the key you own from the step2
*  `client_ secret` is the key you own from the step2
*  `host` is the host of the mastodon instance

eg

* `username`: foxmask@somewhere.bar
* `password`: foobar
*  `client_ key`: abcdefg
*  `client_ secret`: abcdefg
* `host`: https://mastodon.xyz


Configuration from the Admin panel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

http://127.0.0.1:8000/admin/django_th/servicesactivated/

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/service_mastodon.png
    :target: https://joinmastodon.org/
    :alt: Mastdoon
