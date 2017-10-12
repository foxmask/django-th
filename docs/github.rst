GitHub
======

Service Description:
--------------------

Powerful collaboration, code review, and code management for open source and private projects. Public projects are always free.


Requesting a key
----------------

On https://github.com/settings/developers, click on "New Oauth App" button at right.

Fill the form and get the informations that you will need to provide in the next paragraph


The service keys
----------------

Here are the modifications of .env file you will need to make to be able to use your credentials with Github

.. code-block:: python

    TH_GITHUB_USERNAME= 'username'
    TH_GITHUB_PASSWORD= 'password'
    TH_GITHUB_CONSUMER_KEY= 'your consumer key'
    TH_GITHUB_CONSUMER_SECRET= 'your consumer secret'

