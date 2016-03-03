.. image:: https://codeclimate.com/github/foxmask/django-th/badges/gpa.svg
    :target: https://codeclimate.com/github/foxmask/django-th
    :alt: Code Climate


.. image:: https://travis-ci.org/foxmask/django-th.svg?branch=master
    :target: https://travis-ci.org/foxmask/django-th
    :alt: Travis Status

.. image:: https://readthedocs.org/projects/trigger-happy/badge/?version=latest
    :target: https://readthedocs.org/projects/trigger-happy/?badge=latest
    :alt: Documentation status


.. image:: http://img.shields.io/pypi/v/django-th.svg
    :target: https://pypi.python.org/pypi/django-th/
    :alt: Latest version


.. image:: http://img.shields.io/badge/python-3.4-orange.svg
    :target: https://pypi.python.org/pypi/django-th/
    :alt: Python version supported


.. image:: http://img.shields.io/badge/license-BSD-blue.svg
    :target: https://pypi.python.org/pypi/django-th/
    :alt: License


.. image:: http://img.shields.io/pypi/dm/django-th.svg
   :target: https://pypi.python.org/pypi/django-th/
   :alt: Downloads per month


=============
Trigger Happy
=============

Automatically share data between popular services you use on the web.
And instead of giving your credentials to them, become the owner of yours !

For example a new RSS item is published, "Trigger Happy" will be able to
automatically create a note on your Evernote account or create a bookmark to
your own Readability or Pocket account and so on

.. image:: http://trigger-happy.eu/static/th_esb.png


Description
===========

The goal of this project is to be independant from any other solution like
IFTTT, CloudWork or others.

Thus you could host your own solution and manage your own triggers without
depending any non-free solution.

With this project you can host triggers for you.

All you need is to have a hosting provider (or simply your own server ;) )
who permits to use a manager of tasks like "cron" and, of course Python.

Requirements
============

* Python 3.4.x
* `Django <https://pypi.python.org/pypi/Django/>`_ < 1.9a
* `arrow <https://pypi.python.org/pypi/arrow>`_ < 0.7.0
* `django-formtools <https://pypi.python.org/pypi/django-formtools>`_ == 1.0
* `django-js-reverse <https://pypi.python.org/pypi/django-js-reverse>`_ == 0.6.1
* `django-rq <https://pypi.python.org/pypi/django-rq>`_ == 0.9.0

for evernote support

* `Evernote for python 3 <https://github.com/evernote/evernote-sdk-python3>`_
* `libtidy-dev <http://tidy.sourceforge.net/>`_  >= 0.99

The latest libtidy-dev should be installed with your operating system package manager, not from pip.

On a Debian/Ubuntu system:

.. code:: bash

    apt-get install libtidy-dev


for github support

* `github <https://pypi.python.org/pypi/github3.py>`_ == 1.0.0a2

for pocket support

* `pocket <https://pypi.python.org/pypi/pocket>`_  == 0.3.6

for readability support

* `readability <https://pypi.python.org/pypi/readability-api>`_ == 1.0.2

for rss support

* `feedparser <https://pypi.python.org/pypi/feedparser>`_  == 5.2.1

for search engine

* `django-haystack <https://github.com/django-haystack/django-haystack>`_ == 2.4.1

for trello support

* `trello <https://github.com/sarumont/py-trello>`_  == 0.4.3
* `pypandoc <https://pypi.python.org/pypi/pypandoc>`_  == 1.1.3

Pandoc is also needed of the system, that you can install on a Debian/Ubuntu system like this:

.. code:: bash

    apt-get install pandoc


for twitter support

* `twython <https://github.com/ryanmcgrath/twython>`_  == 3.2.0


for redis support

* `django-redis <https://pypi.python.org/pypi/django-redis>`_ == 4.1.0


for pelican support

* `awesome-slugify <https://pypi.python.org/pypi/awesome-slugify>`_ == 1.6.5


and finally :

.. code-block:: bash

    pip install django-th[all]


or to make your own "recipe" :


.. code-block:: bash

    pip install django-th[rss,pocket]
    pip install django-th[rss,twitter,pocket,github]



Documentation
=============

For installation and settings, see http://trigger-happy.readthedocs.org/


Blog posts :
============

You can find all details of all existing services of the blog :

* https://foxmask.trigger-happy.eu/tag/triggerhappy.html
* https://blog.trigger-happy.eu/
