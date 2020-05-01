.. image:: https://travis-ci.org/push-things/django-th.svg?branch=master
    :target: https://travis-ci.org/push-things/django-th
    :alt: Travis Status


.. image:: http://img.shields.io/pypi/v/django-th.svg
    :target: https://pypi.org/project/django_th/
    :alt: Latest version


.. image:: https://codeclimate.com/github/push-things/django-th/badges/gpa.svg
    :target: https://codeclimate.com/github/push-things/django-th
    :alt: Code Climate


.. image:: https://coveralls.io/repos/github/push-things/django-th/badge.svg
   :target: https://coveralls.io/github/push-things/django-th
   :alt: Test Coverage


.. image:: https://scrutinizer-ci.com/g/push-things/django-th/badges/quality-score.png?b=master
   :target: https://scrutinizer-ci.com/g/push-things/django-th/?branch=master
   :alt: Scrutinizer Code Quality


.. image:: https://readthedocs.org/projects/trigger-happy/badge/?version=latest
    :target: https://readthedocs.org/projects/trigger-happy/?badge=latest
    :alt: Documentation status


.. image:: http://img.shields.io/badge/python-3.6-orange.svg
    :target: https://pypi.org/pypi/django-th/
    :alt: Python version supported


.. image:: http://img.shields.io/badge/license-BSD-blue.svg
    :target: https://pypi.org/pypi/django-th/
    :alt: License


.. image:: https://img.shields.io/badge/SayThanks.io-%E2%98%BC-1EAEDB.svg
    :target: https://saythanks.io/to/foxmask
    :alt: Say thanks to foxmask


=============
Trigger Happy
=============

Automate the exchanges of the data between the applications and services you use on the web.

Make Twitter talk to Mastodon, make Github talk to Mattermost, store your favorite tweets by creating notes in Evernote, follow RSS feeds and post each news in Wallabag, Pocket or Evernote.

The possibilities are too numerous to name all of them, but with that project you won't have to raise your little finger at all: automate everything and make your life easier.

And last but not least, as this is your project, all the credentials you used to give to IFTTT and consorts, are now safe in your hands.

.. image:: https://raw.githubusercontent.com/push-things/django-th/master/docs/installation_guide/th_esb.png
   :alt: Trigger Happy Architecture


Requirements
============

The minimum requirements are the following:

* `Python 3.6+ <https://python.org/>`_
* `Redis <https://redis.io/>`_
* `Django <https://www.djangoproject.com/>`_  **up to v 2.2, not 3.0**
* `DjangoRestFramework <http://www.django-rest-framework.org/>`_
* `Django-formtools <https://pypi.org/pypi/django-formtools>`_
* `Django-js-reverse <https://pypi.org/pypi/django-js-reverse>`_
* `Django-Redis <https://pypi.org/pypi/django-redis/>`_
* `Pypandoc <https://pypi.org/pypi/pypandoc/>`_
* `Requests-oAuthlib <https://pypi.org/pypi/requests-oauthlib/>`_
* `Arrow <https://pypi.org/pypi/arrow>`_

Installation
============

.. code-block:: bash

    pip install django-th


Documentation
=============

For installation and settings, see http://trigger-happy.readthedocs.org/



Archiving the projet (5/1/2020)
===============================

I could try to migrate to **django 3.0**, but I don't use any of the supported services anymore, so I can't migrate to django 3.x

The project use a lots of tricks to handle Form Tools Wizard, required to create triggers ;) And many many others ones to load service class automatically, use webhooks and so on.

The **Furture** is now in `yeoboseyo <https://github.com/foxmask/yeoseyo>`_, a little "Trigger Happy" made with `starlette <https://starlette.io>`_ (and its projects ecosystem) 
