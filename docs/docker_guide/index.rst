.. _docker:

Docker Guide
============

The docker file is based on `build <https://docs.docker.com/engine/reference/commandline/build/>`_ and
`compose <https://docs.docker.com/compose/django/>`_ and a bit of `django hub <https://hub.docker.com/_/django/>`_

Build
-----

The first time you use the docker image of trigger happy, launch this command to build the image.

This won't be necessary for the next time

.. code-block:: bash

    docker-compose build


Run
---

This is necessary each time you want to use Trigger Happy

.. code-block:: bash

    docker-compose up


Database update/create
----------------------

This is necessary the first time, after building the docker image done above.

.. code-block:: bash

    docker-compose run web  python manage.py migrate --settings=django_th.settings_docker
    docker-compose run web  python manage.py loaddata initial_services --settings=django_th.settings_docker
    docker-compose run web  python manage.py createsuperuser --settings=django_th.settings_docker

This is necessary only when a new release of Trigger Happy is done

.. code-block:: bash

    docker-compose run web  python manage.py migrate --settings=django_th.settings_docker


Running tasks
-------------

2 tasks are usually in the crontab: one to read the data source, one to publish the grabbed data:

.. code-block:: bash

    docker-compose run web  python manage.py read --settings=django_th.settings_docker
    docker-compose run web  python manage.py publish --settings=django_th.settings_docker

