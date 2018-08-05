.. _installation:

========
Updating
========


From GitHub
===========

.. code-block:: bash

    git pull https://github.com/push-things/django-th.git

then continue by installing :

.. code-block:: bash

    cd django-th
    pip install -e .[all]


From Pypi
=========


.. code-block:: bash

    pip install -U django-th


Database
========

update the database

.. code-block:: bash

    python manage.py migrate


Start the application
=====================

.. code-block:: bash

    python manage.py runserver &


Now open your browser and go to http://127.0.0.1:8000/th/ to start using the application by logged in
