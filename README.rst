.. image:: https://codeclimate.com/github/foxmask/django-th/badges/gpa.svg
    :target: https://codeclimate.com/github/foxmask/django-th
    :alt: Code Climate


.. image:: https://scrutinizer-ci.com/g/foxmask/django-th/badges/quality-score.png?b=master
   :target: https://scrutinizer-ci.com/g/foxmask/django-th/?branch=master
   :alt: Scrutinizer


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
your own Wallabag or Pocket account and so on


Description
===========

The goal of this project is to be independent from any other solution like
IFTTT, CloudWork or others.

Thus you could host your own solution and manage your own triggers without
depending any non-free solution.

With this project you can host triggers for you.

All you need is to have a hosting provider (or simply your own server ;) )
who permits to use a manager of tasks like "cron" and, of course Python.

Requirements
============

The minimum are the following :

* Python 3.4.x or 3.5.x
* `Django <https://pypi.python.org/pypi/Django/>`_ < 1.9a
* `arrow <https://pypi.python.org/pypi/arrow>`_ < 0.7.0
* `django-formtools <https://pypi.python.org/pypi/django-formtools>`_ == 1.0
* `django-js-reverse <https://pypi.python.org/pypi/django-js-reverse>`_ == 0.7.1



Installation
============

.. code-block:: bash

    pip install django-th[all]


or to make your own "recipe" :


.. code-block:: bash

    pip install django-th[rss,wallabag]
    pip install django-th[rss,twitter,pocket,github]



Documentation
=============

For installation and settings, see http://trigger-happy.readthedocs.org/


