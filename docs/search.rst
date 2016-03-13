Search
======

Service Description:
--------------------

The search engine of Trigger Happy

modifications of settings.py
----------------------------

1) INSTALLED_APPS :

.. code-block:: python

    INSTALLED_APPS = (
        'haystack',
        'th_search',
    )

2) Haystack settings :

set the ENGINE backend of your choice regarding the django haystack doc http://django-haystack.readthedocs.org/en/v2.4.0/tutorial.html#installation

.. code-block:: python

    HAYSTACK_CONNECTIONS = {
        'default': {
            # set the backend of your choice from
            # http://django-haystack.readthedocs.org/en/v2.4.0/tutorial.html#installation
            # for example
            # 'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
            'URL': 'http://127.0.0.1:9200/',
            'INDEX_NAME': 'haystack',
        },
    }
