import os
import sys
from settings.base import *

if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase'
    }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':  ':memory:',
    }
}

SECRET_KEY = os.environ.get('SECRET_KEY')
