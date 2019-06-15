# The main settings file does not have these variables specified and expects
# you to provide them. To just get the app working, copy this file to
# local_settings.py in the same folder and modify as required.

import os

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '+eo5lhh%vc4vo(%=km4-xj)yy2ox=4974#_n$!ko#4ke5zi(#8')
DEBUG = os.environ.get('DJANGO_DEBUG', '') != False
ALLOWED_HOSTS = ['localhost', '0.0.0.0', '127.0.0.1']

# Stuff about the database
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Heroku: Update database configuration from $DATABASE_URL.
import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)# Heroku: Update database configuration from $DATABASE_URL.
