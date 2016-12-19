from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        # 'PASSWORD': 'th_pass',
        'HOST': 'db',
        'PORT': 5432,
    }
}
