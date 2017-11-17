# CONTRIBUTING

Creating a new issue for a bug report
-------------------------------------

:bug: If you think you've spotted a bug, fill an [issue](https://github.com/foxmask/django-th/issues/new) and give as many details as possible by starting with that informations: 

* Version of the project you use
* How you installed it (with `pip install django_th` or `git clone https://github.com/foxmask/django-th/`)
* Python version: 
* Django version: 
* RDBMS version: 
* OS version: 
* Dedicated server (Yes / No):


New Feature
-----------

:bulb: If you want ot see a new feature included to the project, then open an [issue](https://github.com/foxmask/django-th/issues/new) to request this feature, thus we will check if it matches the spirit of the project.


New Module
----------

You have an idea for a new module ? 

If you have skill with Python/Django :

To Create a new module, [I made this project](https://github.com/foxmask/django-th-ansible) which allow to build a new module from scratch. Just launch `ansible` with the parameters you setup in the file `site.yml` and 80% of the code of the module will be done. 

If you don't have skill or don't plan to contribute, just open an issue as explain ealier


Bug Fixing
----------

:bug: You can pick up [one of the issue](https://github.com/foxmask/django-th/issues). The sort order can be priority, issues that remain to be closed for a given milestone, or issues tagged as "bug".


Development
-----------

:sparkles:

1. first of all, clone the project
1. create a new branch for the issue you want to fix
1. if it's:
 1. a bug fix, checkout the branch on which this bug occurs
1. commit and push to your cloned repository
1. make a Pull Request
1. wait patiently ;)

Unit Test
---------

:coffee: those are great to help to test how your code is working, and most of this, to check that your improvements don't break the existing code.
All of them are in a test.py module on in a folder test/ that hosts several testing modules

To avoid to commit things that could fail, in the **.git/hooks/pre-commit** add this

```shell
#!/bin/bash
python manage.py test -v2
RESULT=$?
[ $RESULT -ne 0 ] && exit 1
flake8
RESULT=$?
[ $RESULT -ne 0 ] && exit 1
exit 0
```

Thus, if the tests pass, the commit will be done and you could push without any problem.

If you don't plan to make `unit test`, the continuous integration tool (Travis CI) will analyze the code, and if it fails, this will take a lot of time to be validated by hand as we will need to:
* create a dedicated branch <github-name>-issue<number>
* pull your code
* run the tests
* debug 

Pull Request
------------

:gift: Create first an [issue](https://github.com/foxmask/django-th/issues/new), then follow the step above in 'development' 

Issue labels
------------
:snake: some explanation on the labels of the issues

* **Hacktoberfest**: for [the Hacktoberfest event](https://hacktoberfest.digitalocean.com)
* **up-for-grabs**: for new users that have never been involved in any other opensource project
* **easy**: this label tells you this issue is easy to fix
* **middle**: this label tells you this issue is not complicated to fix, it just takes a little more time
* **hard**: this label tells you this issue needs you to know the core of the project or a knowledge of a new lib
* **help wanted**: this label tells you this issue needs YOU :)
* **good first issue**: for new users on the project

