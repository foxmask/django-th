Django Trigger Happy
====================

A service like IFTTT which will fire an action from a service when a trigger occurs

for example a new RSS item is published, django-trigger-happy will be able to automatically create a note on your Evernote account

Setting up : Administration
---------------------------

once the module is installed, go to the admin panel and activate the service your want. Currently there are 2 services, RSS and Evernote.

All you can decide here is to tell if the service requires an external authentication or not.

Once they are activated. User can use them.


Usage :
-------

### Activating services : 

The user activates the service for their own need. If the service requires an external authentication, he will be redirected to the service which will ask him the authorization to acces the user's account. Once it's done, goes back to django-trigger-happy to finish and record the "auth token".

### Using the activated services :

a set of 3 pages will ask to the user information that will permit to trigger data from a service "provider" to a service "consummer".

For example : 
* page 1 : the user gives a RSS feed
* page 2 : the user gives the name of the notebook where notes will be stored and a tag if he wants
* page 3 : the user gives a description
