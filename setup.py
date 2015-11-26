from setuptools import setup, find_packages
from django_th import __version__ as version

install_requires = [
    'Django==1.8.7',
    'django-formtools==1.0',
    'arrow==0.5.4',
    'django-js-reverse==0.5.1',
    'celery==3.1.18',
    'django-redis==4.2.0',
    'django-redisboard==1.2.1',
    'pytidylib6==0.2.2',
    'pypandoc==1.0.5',
    'requests-oauthlib==0.5.0',
    'feedparser==5.2.1',
]

extras_require_github = [
    'github3.py==1.0.0a2',
]
extras_require_pocket = [
    'pocket==0.3.6',
]
extras_require_readability = [
    'readability-api==1.0.0',
]
extras_require_rss = [
    'feedparser==5.1.3',
]
extras_require_search = [
    'django-haystack==2.4.0',
]
extras_require_trello = [
    'py-trello==0.4.3',
]
extras_require_twitter = [
    'twython==3.2.0',
]

extras_require_all = extras_require_github\
    + extras_require_pocket + extras_require_readability + extras_require_rss\
    + extras_require_search + extras_require_trello + extras_require_twitter

setup(
    name='django_th',
    version=version,
    description='Trigger Happy - take the control of your data with this bridge between your internet services',
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
        'Programming Language :: Python :: 3.4',
        'Framework :: Django',
        'Topic :: Internet',
        'Topic :: Communications',
        'Topic :: Database',
    ],
    install_requires=install_requires,
    extras_require={
        'all': extras_require_all,
        'github': extras_require_github,
        'pocket': extras_require_pocket,
        'readability': extras_require_readability,
        'rss': extras_require_rss,
        'search': extras_require_search,
        'trello': extras_require_trello,
        'twitter': extras_require_twitter,
    },
    include_package_data=True,
)
