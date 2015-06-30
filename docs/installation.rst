=============
Installation
=============

To get the project do :

From GitHub 
===========

.. code-block:: bash

    git clone https://github.com/foxmask/django-th.git
    pip install -r requirements.txt

From Pypi
=========

.. code-block:: bash

    pip install django-th



Dependencies
------------
* Python 3.4
* Django >= 1.8
* arrow==0.5.4
* django-js-reverse==0.5.1

for formwizard 

* django-formtools==1.0

for celery

* celery==3.1.18

for redis

* django-redis==4.1.0
* django-redisboard==1.2.0

for evernote support

* pytidylib6==0.2.2
* -e git+https://github.com/evernote/evernote-sdk-python3#egg=evernote
* feedparser==5.1.3

for pocket support

* pocket==0.3.5

for twitter support

* twython==3.2.0

for search engine

* django-haystack==2.3.1