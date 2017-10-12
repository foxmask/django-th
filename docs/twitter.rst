Twitter
=======

Service Description:
--------------------

a Social Network

Requesting a key
----------------

Access the page https://apps.twitter.com/app/new

* in the field "WebSite", set https://<yourdomain.com>
* in the field "Callback URL", set https://<yourdomain.com>/th/callbacktwitter

then validate and grab the key on the next page

The service keys
----------------

Here are the modifications of .env file you will need to make to be able to use your credentials with Twitter

.. code-block:: python

    TH_TWITTER_CONSUMER_KEY= 'your twitter key'
    TH_TWITTER_CONSUMER_SECRET= 'your twitter secret'

