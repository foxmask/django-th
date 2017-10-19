.. _running:

=======
Running
=======

Setup the database and running the application


Update the database
-------------------

Once the settings step is done, enter the following command to sync the database :


.. code-block:: bash

    python manage.py migrate


If you meet some errors with this command, have a look at the :ref:`migration`


If you are installing the project from scratch, do not forget to create a super user:


.. code-block:: bash

    python manage.py createsuperuser


Start the application in development/local mode
-----------------------------------------------

.. code-block:: bash

    python manage.py runserver


Now open your browser and go to 127.0.0.1:8000/th/ to start using the application


Note, that if DEBUG Setting in the settings.py is set to DEBUG=False static files won't be served automatically and you'll need to setup a web server (e.g nginx or apache) to serve the statics files from the statics folder.

If you do wish to run locally with DEBUG=False and automatic static files served you'll need to run


.. code-block:: bash

    python manage.py runserver --insecure


This isn't a settings recommended for production deployments. for production deployments please follow the guide provided in django docs_

.. _Docs: https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/


Start the application in production mode
----------------------------------------

* Set `DEBUG` to `False` in `settings.py`

* you need a HTTP server to be up and running with the following settings:

For exemple for a Nginx HTTP server, with the following settings are just focused on the access to the application where `/home/sites/your-domain.com/th/` is the path to the virtualenv

.. code:: ini

    server {
        [...]
        # ROOT website
        root  /home/sites/your-domain.com/th/;

        location /static/ {
                root  /home/sites/your-domain.com/th/;
                gzip  on;
        }

        ## PROXY backend
        location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_next_upstream error timeout invalid_header;
            proxy_set_header        Host            $host;
            proxy_set_header        X-Real-IP       $remote_addr;
            proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header        X-Forwarded-Host $host;
            proxy_set_header        X-Forwarded-Proto $scheme;

        }
        [...]
    }


* then from the folder `/home/sites/your-domain.com/th/`, run

.. code:: python

    python manage.py collectstatics



Setup gunicorn that will start the applications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

From the path `/home/sites/your-domain.com/th/bin`

create a file `init.cfg` containing:

.. code:: ini

    NAME="th"                                      # Name of the application
    DJANGODIR=/home/sites/your-domain.com/th/      # Django project directory

    USER=foxmask                                   # the user to run gunicorn as
    GROUP=foxmask                                  # the group to run as
    NUM_WORKERS=1                                  # how many worker processes should Gunicorn spawn
    DJANGO_SETTINGS_MODULE=th.settings             # which settings file should Django use
    DJANGO_WSGI_MODULE=th.wsgi                     # WSGI module name
    IP=127.0.0.1
    PORT=8000
    #LOG
    LOGDIR=/home/sites/your-domain.com/logs

    LOG_LEVEL=INFO
    ERRORFILE="$LOGDIR$NAME-error.log"
    ACCESSFILE="$LOGDIR$NAME-access.log"

    # HTTPS=on

    # Activate the virtual environment
    cd $DJANGODIR
    source ../bin/activate
    export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
    export PYTHONPATH=$DJANGODIR:$PYTHONPATH


change USER and GROUP to the user and group that fit your needs


create a gunicorn_start script
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

in the folder `/home/sites/your-domain.com/th/bin/` put

.. code:: bash

    #!/bin/bash
    source $(dirname $0)/init.cfg

    echo "Starting Gunicorn for $NAME"

    exec ../bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
      --name $NAME \
      --workers $NUM_WORKERS \
      --user=$USER --group=$GROUP \
      --log-level=$LOG_LEVEL \
      --bind=$IP:$PORT \
      --access-logfile $ACCESSFILE --error-logfile $ERRORFILE


then make the script runnable

.. code:: bash

    chmod +x gunicorn_start

