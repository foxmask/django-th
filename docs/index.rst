.. Trigger Happy documentation master file, created by foxmask

Trigger Happy: Steamer Bridge for your internet services
========================================================

.. image:: https://travis-ci.org/foxmask/django-th.svg?branch=master
    :target: https://travis-ci.org/foxmask/django-th
    :alt: Travis Status


.. image:: http://img.shields.io/pypi/v/django-th.svg
    :target: https://pypi.python.org/pypi/django-th/
    :alt: Latest version


.. image:: https://codeclimate.com/github/foxmask/django-th/badges/gpa.svg
    :target: https://codeclimate.com/github/foxmask/django-th
    :alt: Code Climate


.. image:: https://coveralls.io/repos/github/foxmask/django-th/badge.svg
   :target: https://coveralls.io/github/foxmask/django-th
   :alt: Test Coverage


.. image:: https://scrutinizer-ci.com/g/foxmask/django-th/badges/quality-score.png?b=master
   :target: https://scrutinizer-ci.com/g/foxmask/django-th/?branch=master
   :alt: Scrutinizer Code Quality


.. image:: https://readthedocs.org/projects/trigger-happy/badge/?version=latest
    :target: https://readthedocs.org/projects/trigger-happy/?badge=latest
    :alt: Documentation status


.. image:: http://img.shields.io/badge/python-3.6-orange.svg
    :target: https://pypi.python.org/pypi/django-th/
    :alt: Python version supported


.. image:: http://img.shields.io/badge/license-BSD-blue.svg
    :target: https://pypi.python.org/pypi/django-th/
    :alt: License


Description:
------------

`Trigger Happy` is a free software that provides a steamer bridge to automatically share data between popular services you use on the web.

The goal of this project is to be independent from any other solution like IFTTT, CloudWork or others.

Thus you could host your own solution and manage your own triggers without depending on any non-open solution.

And then, instead of giving your credentials to those companies, keep them with your own **Trigger Happy** to keep the control of your data!


How does it work?
-----------------

For example:

* A news is published on your favorites website, **Trigger Happy** will be able to automatically create a bookmark on your own Wallabag account, for later use, or create a note in your Evernote notebook.

* On your Slack or Mattermost community channel, **Trigger Happy** can publish the issue of github.

* When you add a tweet as favorite, **Trigger Happy** you can "toot" this one, on Mastodon

And so on.

.. image:: https://trigger-happy.eu/static/th_esb.png
   :alt: Trigger Happy Architecture



.. toctree::
   :maxdepth: 2

   quickstart
   installation
   configuration
   running
   crontab
   usage
   services
   migration



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

