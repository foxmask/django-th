DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}
SECRET_KEY = 'wtf'
ROOT_URLCONF = None
USE_TZ = True
INSTALLED_APPS = (
    'django_js_reverse',
)
ALLOWED_HOSTS = ['testserver']