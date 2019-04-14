import os
import sys
from settings.base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':  ':memory:',
    }
}
if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase'
    }

ELASTICSEARCH_INDEX_NAMES = {
    'search_indexes.documents.stocks': 'test_stock',
    # 'search_indexes.documents.publisher': 'publisher',
}
es_test_cluster_config = {
    "port": 9250, "number_of_nodes": 1,
    "network_host": '_local_',
    "cluster_name": 'group-project-test-cluster' 
}
SECRET_KEY = os.environ.get('SECRET_KEY')
