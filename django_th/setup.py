from setuptools import setup, find_packages

setup(
    name='django_th',
    version='0.2.0',
    description='Django Trigger Happy acts when events occur and triggers actions for your account on all the social networks',
    author='Olivier Demah',
    author_email='olivier@foxmask.info',
    url='https://github.com/foxmask/django_th',
    download_url="https://github.com/foxmask/django-th/archive/trigger-happy-0.2.0.zip",
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)
