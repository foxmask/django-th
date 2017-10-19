.. _index:

Administation Guide
===================

That part of the guide will explain the following topics:

* How to create, add a new service
* For the users of your TriggerHappy instance, What's happened when you disable a service.


How to create, add a new service
--------------------------------

from the admin panel at http://127.0.0.1:8000/admin/

Under the paragraph "Trigger Happy", select "Services", then press "add service".
Choose the new service name and fill the fields.
If you don't know how to fill them, see the "Configuration from the Admin panel" for each of the service from the :ref:`Services list<services>`


Disabling a service, what consequences
--------------------------------------

When you turn off a given service:

* if users did not use it before, the service will desappears from the dropdown list of the services, a user can add from the activated services page
* if users already used it before, then the triggers that use the service, will be disabled, the line of the trigger will become inert, impossible to interact with it, and the trigger-happy engine wont handle it all at.
