=======
Running
=======

SETUP THE DATABASE AND RUNNING THE APPLICATION


Update the database
-------------------

Once the settings step is done, enter the following command to sync the database :


.. code-block:: bash

    python manage.py migrate


If you meet some errors with this command, have a look at the MIGRATION_0.10.x_to_0.11.x.rst file


If you are installing the project from scratch, do not forget to create a super user:


.. code-block:: bash

    python manage.py createsuperuser


Start the application in development/local mode
---------------------

.. code-block:: bash

    python manage.py runserver


Now open your browser and go to 127.0.0.1:8000/th/ to start using the application


Note, that if DEBUG Setting in the settings.py is set to DEBUG=False static files won't be served automatically and you'll need to setup a web server (e.g nginx or apache) to serve the statics files from the statics folder.

If you do wish to run locally with DEBUG=False and automatic static files served you'll need to run


.. code-block:: bash

    python manage.py runserver --insecure


This isn't a settings recommended for production deployments. for production deployments please follow the guide provided in django docs_

.. _Docs: https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
