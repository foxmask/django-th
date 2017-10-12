Pushbullet
==========

Service Description:
--------------------

Your devices working better together

Nota: to be able to work, this service requires that your host uses HTTPS

Requesting a key
----------------

On https://www.pushbullet.com/#settings/account 

Fill the form and get the informations that you will need to provide in the next paragraph


The service keys
----------------

Here are the modifications of .env file you will need to do to be able to use your credentials with Pushbullet

.. code-block:: python

    TH_PUSHBULLET_CLIENT_ID= 'your pushbulet id'
    TH_PUSHBULLET_CLIENT_SECRET= 'your pushbulet secret'
