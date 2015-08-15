To migrate enter, 

.. code-block:: bash

    python manage.py  migrate


if the migration complains  that you've already created the table django_th_twitter then check it by :

.. code-block:: sql

    select * from django_migrations ;


check that you dont have those record in the django_migrations table


.. code-block:: sql

    11|django_th|0001_initial|a date

    12|th_twitter|0001_initial|a date


if its not the case, then add the following by hand like that :

.. code-block:: sql

    insert into django_migrations (app,name,applied) values('django_th','0001_initial','2015-08-14 06:37:32.165617');

before adding by hand the line below, check that the table django_th_twitter contains the column max_id and since_id as bigint and not just int

if that columns are not bigint add just this

.. code-block:: sql

    insert into django_migrations (app,name,applied) values('th_twitter','0001_initial','2015-08-14 06:37:32.165617');

otherwise add this too

.. code-block:: sql

    insert into django_migrations (app,name,applied) values('th_twitter','0002_int_to_bigint','2015-08-14 06:37:32.165617');


then play again

.. code-block:: bash

    python manage.py migrate

thus the migration will skip that steps and will continue smoothly