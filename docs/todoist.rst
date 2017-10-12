Todoist
=======

Service Description:
--------------------

a Tasks Management tool

Nota: to be able to work, this service requires that your host uses HTTPS

Requesting a key
----------------

On https://api.todoist.com/app?lang=fr#start select "generate a new api key"


The service keys
----------------

Here are the modifications of .env file you will need to make to be able to use your credentials with Todoist

.. code-block:: python

    TH_TODOIST_CLIENT_ID= 'your todoist id'
    TH_TODOIST_CLIENT_SECRET= 'your todoist secret'


