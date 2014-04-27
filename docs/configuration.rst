=============
Configuration
=============
As usual with Django project, you will setup the database parameters.

Important parts are the settings of the available services :

Settings.py 
-----------

add the module django_th to the INSTALLED_APPS


.. code-block:: python

    INSTALLED_APPS = (
        'django_th',
        'th_rss',
        'th_evernote',
    )

TH_SERVICES
~~~~~~~~~~~

TH_SERVICES is a list of the services, like for example,  

.. code-block:: python

    TH_SERVICES = (
        'th_rss.my_rss.ServiceRss',
        'th_evernote.my_evernote.ServiceEvernote',
    )

If you plan to integrate django_th in an existing project then, to deal with the templates and avoid the TemplateDoesNotExist error you can 
copy the template in your own templates directory or set the path like this :

.. code-block:: python

    import os
    PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
    TEMPLATE_DIRS += (
        PROJECT_DIR + '/../../lib/<python-version>/site-package/django_th/templates/',
    )

also you'll need to look at the urls.py of **django_th** to copy a lot of existing the mapping.


Update the database
~~~~~~~~~~~~~~~~~~~

Once the settings is done, enter the following command to sync the database

.. code-block:: bash

    python manage.py syncdb


Setting up : Administration
===========================

once the module is installed, go to the admin panel and activate the service you want. 

All you can decide here is to tell if the service requires an external authentication or not.

Once they are activated. User can use them.


