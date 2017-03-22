=============
Installation
=============

TriggerHappy can be installed inside an existing project, or from scratch

Installation from scratch
=========================

We just create a virtualenv with python 3.6 (or 3.5)

.. code-block:: bash

    python3.6 -m venv myproject
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


or to make your own "recipe", for example to install some of the component and not all of them:


.. code-block:: bash

    pip install django-th[rss,wallabag]
    pip install django-th[rss,twitter,wallabag,github]


Once it's done, you can continue to the [configuration process](http://trigger-happy.readthedocs.org/en/latest/configuration.html)



Requirements
============

* Python 3.6.x, 3.5.x
* `Django <https://pypi.python.org/pypi/Django/>`_
* `arrow <https://pypi.python.org/pypi/arrow>`_
* `django-formtools <https://pypi.python.org/pypi/django-formtools>`_
* `django-js-reverse <https://pypi.python.org/pypi/django-js-reverse>`_


for evernote support

* `Evernote for python 3 <https://pypi.python.org/pypi/evernote3>`_
* `libtidy-dev <http://tidy.sourceforge.net/>`_

The latest libtidy-dev should be installed with your operating system package manager, not from pip.

On a Debian/Ubuntu system:

.. code:: bash

    apt-get install libtidy-dev

for github support

* `github <https://pypi.python.org/pypi/github3.py>`_

for pocket support

* `pocket <https://pypi.python.org/pypi/pocket>`_

for rss support

* `feedparser <https://pypi.python.org/pypi/feedparser>`_

for trello support

* `trello <https://github.com/sarumont/py-trello>`_
* `pypandoc <https://pypi.python.org/pypi/pypandoc>`_

Pandoc is also needed of the system, that you can install on a Debian/Ubuntu system like this:

.. code:: bash

    apt-get install pandoc


for twitter support

* `twython <https://github.com/ryanmcgrath/twython>`_


for redis support

* `django-redis <https://pypi.python.org/pypi/django-redis>`_


for pelican support

* `awesome-slugify <https://pypi.python.org/pypi/awesome-slugify>`_

for wallabag support

* `wallabag_api <https://pypi.python.org/pypi/wallabag_api>`_

for todoist support

* `todoist-python <https://pypi.python.org/pypi/todoist-python>`_

for pushbullet support

* `pushbullet.py <https://pypi.python.org/pypi/pushbullet.py>`_
