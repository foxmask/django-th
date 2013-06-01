Django Trigger Happy
====================

it is a service like IFTTT service which will fire action when events occur elsewhere on the web

for example a new RSS item is published, django-trigger-happy will be able to automatically create a note on your Evernote account

Description:
-----------
The goal of this project is to be independant from any other solution like IFTTT, CloudWork or others.

Thus you could host your own solution and manage your own triggers without depending any non-free solution.

With this project you can also host triggers for users, or just for you.

All you need is to have a hosting provider (or simply your own server ;) 
who permits to use a manager of tasks like "cron" and, of course Python 2.7

Requirements :
-------------
* Django 1.4.3
* batbelt 0.4
* django-profiles 0.2
* django-registration 0.8
* evernote 1.23.2
* feedparser 5.1.3
* httplib2 0.8
* oauth2 1.5.211
* ordereddict 1.1
* South 0.7.6
* PyTidylib : 0.2.1

Installation:
------------
to get the project, from your virtualenv, do :
```system
git clone https://github.com/foxmask/django-th.git
```
to add the needed modules , do :
```python
pip install -r https://github.com/foxmask/django-th/blob/master/django_th/requirements.txt
```
and at least :
```python
python manage.py syncdb
```
to startup the database

Parameters :
------------
As usual you will setup the database parameters.

Important parts are the settings of the available services :

### Settings.py 

#### TH_SERVICES 

TH_SERVICES is a list of the services we put in django_th/services directory

```python
TH_SERVICES = (
    'django_th.services.my_rss.ServiceRss',
    'django_th.services.my_evernote.ServiceEvernote',
)
```

##### TH_EVERNOTE
TH_EVERNOTE is the settings you will need to be able to add/read data in/from Evernote.
```python
TH_EVERNOTE = {
    'sandbox': True,
    'consumer_key': 'abcdefghijklmnopqrstuvwxyz',
    'consumer_secret': 'abcdefghijklmnopqrstuvwxyz',
}
```
set sandbox to False in production and provide your consummer_key and consumer_secret 



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


Fire the Triggers :
-------------------
To start handling the queue of triggers you/your users configure, just set the fire.py in a crontab or any other scheduler solution of your choice.
Keep in mind to avoid to set a too short duration between 2 run to avoid to be blocked by the externals services you/your users want to reach.
