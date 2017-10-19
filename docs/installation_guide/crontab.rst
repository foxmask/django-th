.. _crontab:

Crontab
=======

a crontab is a system that automates tasks for you, at a given moment.

Here are the tasks to run the **Trigger Happy** engine automatically


.. code-block:: bash

    # trigger happy
    20,40 * * * * . /home/trigger-happy/bin/recycle
    10,25,41,55 * * * * . /home/trigger-happy/bin/read
    */15 * * * * . /home/trigger-happy/bin/publish


The first line is used to recycle the data, that is unpublished, for example, because of reaching a rate limit.
When this behavior occurs, the data stays in the cache, to be used at the next loop.

content of the **recycle** command

.. code-block:: bash

    . /home/trigger-happy/bin/activate && cd /home/trigger-happy/th/ && python manage.py recycle


content of the **read** command

.. code-block:: bash

    . /home/trigger-happy/bin/activate && cd /home/trigger-happy/th/ && python manage.py read


content of the **publish** command

.. code-block:: bash

    . /home/trigger-happy/bin/activate && cd /home/trigger-happy/th/ && python manage.py publish

You may notice the folder `/home/trigger-happy/th/` in each command, this is a virtualenv given for the example

The periodicity of the execution is set like this, to avoid to make 2 tasks run in same time, and also, to avoid to reach often the rate limitation of Twitter and others sensitives services.
