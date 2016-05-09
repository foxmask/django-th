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
    python setup.py install


Installation From Pypi
======================


.. code-block:: bash

    pip install django-th[all]


or to make your own "receipe", for example to install some of the component and no all of them:


.. code-block:: bash

    pip install django-th[rss,wallabag]
    pip install django-th[rss,twitter,wallabag,github]


Once it's done, you can continue to the [configuration process](http://trigger-happy.readthedocs.org/en/latest/configuration.html)



Requirements
============

* Python 3.4.x
* `Django <https://pypi.python.org/pypi/Django/>`_ < 1.9a
* `arrow <https://pypi.python.org/pypi/arrow>`_ < 0.7.0
* `django-formtools <https://pypi.python.org/pypi/django-formtools`_ == 1.0
* `django-js-reverse <https://pypi.python.org/pypi/django-js-reverse>`_ == 0.7.1


for evernote support

* `Evernote for python 3 <https://pypi.python.org/pypi/evernote3>`_
* `libtidy-dev <http://tidy.sourceforge.net/>`_  >= 0.99

The latest libtidy-dev should be installed with your operating system package manager, not from pip.
On a Debian/Ubuntu system:

.. code:: bash

    apt-get install libtidy-dev



for github support

* `github <https://pypi.python.org/pypi/github3.py>`_ == 1.0.0a4

for pocket support

* `pocket <https://pypi.python.org/pypi/pocket>`_  == 0.3.6

for readability support

* `readability <https://pypi.python.org/pypi/readability-api>`_ == 1.0.2

for rss support

* `feedparser <https://pypi.python.org/pypi/feedparser>`_  == 5.2.1

for search engine

* `django-haystack <https://github.com/django-haystack/django-haystack>`_ == 2.4.1

for trello support

* `trello <https://github.com/sarumont/py-trello>`_  == 0.5.0
* `pypandoc <https://pypi.python.org/pypi/pypandoc>`_  == 1.1.3

Pandoc is also needed of the system, that you can install on a Debian/Ubuntu system like this:

.. code:: bash

    apt-get install pandoc


for twitter support

* `twython <https://github.com/ryanmcgrath/twython>`_  == 3.4.0


for redis support

* `django-redis <https://pypi.python.org/pypi/django-redis>`_ == 4.1.0


for pelican support

* `awesome-slugify <https://pypi.python.org/pypi/awesome-slugify>`_ == 1.6.5

for wallabag support

* `wallabag_api <https://pypi.python.org/pypi/wallabag_api>`_ == 1.1.0
