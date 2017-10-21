Slack
=====

Service Description:
--------------------

A messaging app for teams who put robots on Mars

This app does not need any key, you need to have a Slack account and being able to provide incoming webhook or outgoing webhook

this webhook can be defined from https://<your community>.slack.com/apps/manage/custom-integrations > "customer integration" > incoming|outgoing webhook

User Guide
----------

Activation of the service
~~~~~~~~~~~~~~~~~~~~~~~~~

From the page http://127.0.0.1:8000/th/service/add/

.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/installation_guide/public_service_wallabag_add.png
   :alt: My Activated Services

then in the form, select Slack in the dropdown box and press "Activate it"

Defining a trigger
~~~~~~~~~~~~~~~~~~

with Slack as consumer, when another service is used as a provider

.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/installation_guide/slack_consumer_step3.png
    :alt: slack step 3

.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/installation_guide/slack_consumer_step4.png
    :alt: slack step 4

with Slack as provider, when another service is used as a consumer

.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/installation_guide/slack_provider_step1.png
    :alt: slack step 1

.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/installation_guide/slack_provider_step2.png
    :alt: slack step 2

Installation Guide
------------------

Configuration from the Admin panel
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

http://127.0.0.1:8000/admin/django_th/servicesactivated/

.. image:: https://raw.githubusercontent.com/foxmask/django-th/master/docs/installation_guide/service_slack.png
    :target: https://slack.com/
    :alt: Slack
