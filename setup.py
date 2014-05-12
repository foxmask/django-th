from setuptools import setup, find_packages
from django_th import __version__ as version
import os


def strip_comments(l):
    return l.split('#', 1)[0].strip()


def reqs(*f):
    return list(filter(None, [strip_comments(l) for l in open(
        os.path.join(os.getcwd(), *f)).readlines()]))

install_requires = reqs('requirements.txt')

setup(
    name='django_th',
    version=version,
    description='Django Trigger Happy acts when events occur and triggers actions for your account on all the social networks',
    author='Olivier Demah',
    author_email='olivier@foxmask.info',
    url='https://github.com/foxmask/django-th',
    download_url="https://github.com/foxmask/django-th/archive/trigger-happy-"
    + version + ".zip",
    packages=find_packages(exclude=['django_th/local_settings']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
    ],
    install_requires=install_requires,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'trigger-happy = django_th.fire:go',
        ],
    }
)
