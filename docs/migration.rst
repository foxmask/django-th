=================================
MIGRATIONS from 0.10.x to 0.11.x:
=================================

Note: in the SQL queries below, I use CURRENT_TIMESTAMP because of Postgresql. Adapt it to your own RDBMS.

Trigger Happy tables
====================

To migrate, enter,

.. code-block:: bash

    python manage.py  migrate

if the migration complains that you've already created the table django_th_rss then check the following:

.. code-block:: sql

    select * from django_migrations ;

to find

    11 | django_th         | 0001_initial        | 2015-06-10 10:00:00.977958+02

if you don't have it then do:

.. code-block:: sql

    insert into django_migrations (app,name,applied) values('django_th','0001_initial',CURRENT_TIMESTAMP);


then replay

.. code-block:: bash

    python manage.py migrate



Trigger Happy Module tables
===========================

Evernote:
---------

if the migration complains that you've already created the table django_th_evernote then check it by:

.. code-block:: sql

    select * from django_migrations ;


check that you don't have those record in the django_migrations table

.. code-block:: sql

    select * from django_migrations ;

    13 | th_evernote       | 0001_initial        | 2015-06-10 10:00:00.977958+02


if it's not the case, then add the following by hand like that:

.. code-block:: sql

    insert into django_migrations (app,name,applied) values('th_evernote','0001_initial',CURRENT_TIMESTAMP);


Pocket:
-------

if the migration complains that you've already created the table django_th_pocket then check it by:

.. code-block:: sql

    select * from django_migrations ;


check that you don't have those record in the django_migrations table

.. code-block:: sql

    select * from django_migrations ;

    13 | th_pocket       | 0001_initial        | 2015-06-10 10:00:00.977958+02

if it's not the case, then add the following by hand like that:

.. code-block:: sql

    insert into django_migrations (app,name,applied) values('th_pocket','0001_initial',CURRENT_TIMESTAMP);


Twitter:
--------

if the migration complains that you've already created the table django_th_twitter then check it by:

.. code-block:: sql

    select * from django_migrations ;


check that you don't have those record in the django_migrations table

.. code-block:: sql

    select * from django_migrations ;

    13 | th_twitter     | 0001_initial        | 2015-06-10 10:00:00.977958+02


if it's not the case, then add the following by hand like that:

.. code-block:: sql

    insert into django_migrations (app,name,applied) values('th_twitter','0001_initial',CURRENT_TIMESTAMP);
    insert into django_migrations (app,name,applied) values('th_twitter','0002_int_to_bigint',CURRENT_TIMESTAMP);

before adding by hand the line below, check that the table django_th_twitter contains the column max_id and since_id as bigint and not just int

if that columns are not bigint add just this

.. code-block:: sql

    insert into django_migrations (app,name,applied) values('th_twitter','0001_initial',CURRENT_TIMESTAMP);


otherwise add this too

.. code-block:: sql

    insert into django_migrations (app,name,applied) values('th_twitter','0002_int_to_bigint',CURRENT_TIMESTAMP);


Table to drop:
--------------

with the last

.. code-block:: bash

    python manage.py migrate


you will see this message:


.. code-block:: bash

    Running migrations:
      No migrations to apply.
      Your models have changes that are not yet reflected in a migration, and so won't be applied.
      Run 'manage.py makemigrations' to make new migrations, and then re-run 'manage.py migrate' to apply them.
    The following content types are stale and need to be deleted:

        django_th | userprofile

answer yes as this one is not used at all


then play again

.. code-block:: bash

    python manage.py migrate

thus the migration will skip that step and will continue smoothly.
