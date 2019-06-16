# The main settings file does not have these variables specified and expects
# you to provide them. To just get the app working, copy this file to
# local_settings.py in the same folder and modify as required.

import os

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '+eo5lhh%vc4vo(%=km4-xj)yy2ox=4974#_n$!ko#4ke5zi(#8')
DEBUG = os.environ.get('DJANGO_DEBUG', '') != False
ALLOWED_HOSTS = ['nisergolf.herokuapp.com', '127.0.0.1']

# Stuff about the database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'golf',
        'USER': 'ayush',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

