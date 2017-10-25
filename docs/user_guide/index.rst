User Guide
==========

That part of the guide will explain the following topics:


* Lexicon
* How to activate a service and fill the form
* How to create a trigger in 5 steps
* How to edit the trigger
* How to turn off/on a trigger
* What's happened when a trigger is set back to on.
* How to trigger a task from the application without using the commands line
* Filtering the list of trigger by a given service
* Trigger information (date of creation, last execution, number of time it has been run, the message of the last execution, why the trigger has been stopped by the engine)
* My trigger is "in grey" and I can't select it, edit it, launch it


Lexicon
-------

* `Provider`: the first of the 2 services. Used to provide the data
* `Consumer`: the second of the 2 services. Used to publish the data grabbed by the provider
* a `Trigger` is composed of one provider and one consumer (and a description)


How to activate a service and fill the form
-------------------------------------------

From the page "Services" http://127.0.0.1:8000/th/service/ you have the list of the services you can use to get date or publish data.

The page is divided in two parts.

One part: Activated Services, the ones that are already activated, the other part: Available Services, that you have not yet activated.

To activate them, have a look at the page :ref:`Services list<services>` of each service that pleases you.


What a line of the trigger contains
-----------------------------------

* at left :

 * description - provider name - consumer name
 * date creation - date last time a trigger has
 * the message OK, or the error related to one of the service
 * the number of times the trigger run successfully - unsuccessfully


* at right : buttons to :

 * launch the current trigger
 * set to off (when the button is blue) or on (if the button is green) the status of the trigger
 * delete the trigger


How to create a trigger in 5 steps
----------------------------------

* Page 1 select one of the service that will provide the data you want
* Page 2 fill the field(s) related to the service, if necessary
* Page 3 select one of the service that will consume the data you want
* Page 4 fill the field(s) related to the service, if necessary
* Page 5 fill a description

role of each couple of page :

* Page 1 and 3 are the same, except that, a provider can not be a consumer too
* Page 2 and 4 their content, depends of the choice you made page 1 and 3.

To know what information you need to enter, see the service of your choice from
the :ref:`Services list<services>`


How to edit the trigger
-----------------------

You can edit the provider or consumer by selecting its name, or change the description of the trigger by clicking of it.


How to turn off/on a trigger
----------------------------

on each line of the trigger, as explain earlier, at the right of the trigger line, set to off (when the button is blue) or on (if the button is green) the status of the trigger


What's happened when a trigger is set back to on
------------------------------------------------

When a trigger is set back to 'on', the date triggered is set to the current date.
This allow you to avoid to flood the consumer with the data you'd grabbed from
the provider from a long long time.

For example, imagine, it's summer, you go on holidays and to be quite, you set all your triggers to off.
Then when you will come back home, you are relax and ready to dive back into the active life.
Then you set all triggers back to on, and the trigger happy engine, won't flood all your consumer.


My trigger is "in grey" and I can't select it, edit it, launch it
-----------------------------------------------------------------

The administrator of the Trigger Happy instance, disabled one of the services or both. The trigger(s) won't be available at all, until the administrator set reactive it/them.
