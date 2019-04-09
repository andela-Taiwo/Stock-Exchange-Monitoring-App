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
ELASTICSEARCH_INDEX_NAMES = {
    'search_indexes.documents.stocks': 'test_stock',
    # 'search_indexes.documents.publisher': 'publisher',
}
SECRET_KEY = os.environ.get('SECRET_KEY')
