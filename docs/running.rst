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


Start the application
---------------------

.. code-block:: bash

    python manage.py runserver


Now open your browser and go to 127.0.0.1:8000/th/ to start using the application

