# CONTRIBUTING

New Feature
-----------

:bulb: open an [issue](https://github.com/foxmask/django-th/issues/new
) to ask this feature, thus we will check if this one will match the main line of the project.


Bug Fixing
-----------

:bug: You can pick [one of the issue](https://github.com/foxmask/django-th/issues). The sort order can be in priority, the issues that remain to be closed for a given milestone, then the issues tagged as "bug".


Development
-----------

:sparkles:

1. first of all, clone the project
1. create a new branch for the issue you want to fix
1. if its :
 1. a bug fixing, checkout the branch on which this bug occurs
1. commit and push to your cloned repository
1. make a Pull Request
1. wait patiently ;)


Pull Request
-----------

:gift: Create first an [issue](https://github.com/foxmask/django-th/issues/new), then follow the step above in 'development' 

Issue labels
-----------
:snake: some explanation on the labels of the issues

* **Hacktoberfest** : for [the Hacktoberfest event](https://hacktoberfest.digitalocean.com)
* **up-for-grabs** : for new users that have never been involved in any other opensource project
* **easy** : this label tells you this issue is easy to fix
* **middle** : this label tells you this issue is not complicate to fix, just take a little more time
* **hard** : this label tells you this issue need you to know the core of the projet or a knwoledge of a new lib

Unit Test
-----------

:coffee: those are great to help to test how your code is working, and most of this, to check that your improvements dont break the existing code.
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
