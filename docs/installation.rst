=============
Installation
=============

TriggerHappy can be installed inside an existing project, or from scratch

Installation from scratch
=========================

We just create a virtualenv with python 3.4

.. code-block:: bash

    virtualenv --pytyhon=/usr/bin/python34 myproject
    cd $_
    source bin/activate
    
then you can continue with one of the two choice "From GitHub" or "From Pypi"


Installation from an existing project
=====================================

.. code-block:: bash

    cd /to/the/path/of/my/existing/project
    source bin/activate (if you have a virtualenv)
 
then you can continue with one of the two choice "From GitHub" or "From Pypi"


Installation From GitHub
========================

.. code-block:: bash

    git clone https://github.com/foxmask/django-th.git

then continue by installing :

.. code-block:: bash

    cd django-th
    python setup install
    cd ..
    pip install -r requirements-evernote.txt


Installation From Pypi
======================

in 2 steps :


step 1:

.. code-block:: bash

    pip install django-th[all]


or to make your own "receipe", for example to install some of the component and no all of them:


.. code-block:: bash

    pip install django-th[rss,pocket]
    pip install django-th[rss,twitter,pocket,github]


step 2:

if you need Evernote, you will have to finish by

.. code-block:: bash

    pip install -r https://raw.githubusercontent.com/foxmask/django-th/master/requirements-evernote.txt

this is because Evernote SDK for Python 3 is not yet available on pypi, then we get it from GitHub


Once you have made this steps, you can continue to the [configuration process](http://trigger-happy.readthedocs.org/en/latest/configuration.html)



Requirements
============

* Python 3.4.x
* `Django <https://pypi.python.org/pypi/Django/>`_ >= 1.8 < 1.9
* `arrow <https://pypi.python.org/pypi/arrow>`_ == 0.5.4
* django-formtools == 1.0
* `django-js-reverse <https://pypi.python.org/pypi/django-js-reverse>`_ == 0.5.1
* `libtidy-dev <http://tidy.sourceforge.net/>`_  >= 0.99

The latest libtidy-dev should be installed with your operating system package manager, not from pip.
On a Debian/Ubuntu system:

.. code:: bash

    apt-get install libtidy-dev


for celery

* `Celery <http://www.celeryproject.org/>`_ == 3.1.18

for evernote support

* `Evernote for python 3 <https://github.com/evernote/evernote-sdk-python3>`_

for github support

* `github <https://pypi.python.org/pypi/github3.py>`_ == 1.0.0a2

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
* `pypandoc <https://pypi.python.org/pypi/pypandoc>`_  == 1.0.5

Pandoc is also needed of the system, that you can install on a Debian/Ubuntu system like this:

.. code:: bash

    apt-get install pandoc


for twitter support

* `twython <https://github.com/ryanmcgrath/twython>`_  == 3.2.0


for redis support

* `django-redis <https://pypi.python.org/pypi/django-redis>`_ == 4.1.0
* `django-redisboard <https://pypi.python.org/pypi/django-redisboard>`_ == 1.2.0
