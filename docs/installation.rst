=============
Installation
=============

To get the project do :

From GitHub 
===========

.. code-block:: bash

    git clone https://github.com/foxmask/django-th.git
    pip install -r requirements-all.txt

From Pypi
=========

.. code-block:: bash

    pip install django-th


Dependencies
------------
* Python 3.4.x
* `Django <https://pypi.python.org/pypi/Django/>`_ >= 1.8
* `arrow <https://pypi.python.org/pypi/arrow>`_ == 0.5.4
* django-formtools == 1.0
* `django-js-reverse <https://pypi.python.org/pypi/django-js-reverse>`_ == 0.5.1
* `libtidy-dev <http://tidy.sourceforge.net/>`_  >= 0.99

The latest libtidy-dev should be installed with your operating system package manager, not from pip.
On a Ubuntu system: 
 
.. code:: system
    apt-get install libtidy-dev


for celery

* `Celery <http://www.celeryproject.org/>`_ == 3.1.18

for evernote support

* `Evernote for python 3 <https://github.com/evernote/evernote-sdk-python3>`_ 

for pocket support

* `pocket <https://pypi.python.org/pypi/pocket>`_  == 0.3.5

for readability support

* `readability <https://pypi.python.org/pypi/readability-api>`_ == 1.0.0

for rss support

* `feedparser <https://pypi.python.org/pypi/feedparser>`_  == 5.1.3

for search engine

* `django-haystack <https://github.com/django-haystack/django-haystack>`_ == 2.3.1

for trello support

* `trello <https://github.com/sarumont/py-trello>`_  == 0.4.3

for twitter support

* `twython <https://github.com/ryanmcgrath/twython>`_  == 3.2.0


for redis support 

* `django-redis <https://pypi.python.org/pypi/django-redis>`_ == 4.1.0
* `django-redisboard <https://pypi.python.org/pypi/django-redisboard>`_ == 1.2.0
