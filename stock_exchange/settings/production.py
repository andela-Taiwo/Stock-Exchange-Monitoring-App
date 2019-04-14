from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    'stock-exchange-env.qdtzm52k3p.us-east-1.elasticbeanstalk.com','stormy-lake-21329.herokuapp.com'
]

ADMINS = (('@memunat', 'thepanache27@gmail.com'), )

ELASTICSEARCH_INDEX_NAMES = {
    'search_indexes.documents.stocks': 'prod_stock',
    # 'search_indexes.documents.publisher': 'publisher',
}