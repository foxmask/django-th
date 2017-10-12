Evernote
========

Service Description:
--------------------

This service allows to take notes, photos, schedule things and so on


Requesting a key
----------------

On https://dev.evernote.com/ at the top right of the page, click on 'get an api key'.

Fill the form and get the informations that you will need to provide in the next paragraph


The service keys
----------------

Here are the modifications of .env file you will need to make to be able to use your credentials with Evernote

.. code-block:: python

    TH_EVERNOTE_SANDBOX = False 
    TH_EVERNOTE_CONSUMER_KEY = 'your consumer key'
    TH_EVERNOTE_CONSUMER_SECRET =  'your consumer secret'

