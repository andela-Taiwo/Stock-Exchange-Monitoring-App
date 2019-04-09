from django.conf import settings
from django_elasticsearch_dsl import DocType, Index, fields
from elasticsearch_dsl import analyzer

from stocks.models import Stock

# Name of the Elasticsearch index
INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])

# See Elasticsearch Indices API reference for available settings
INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1
)

html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["standard", "lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)


@INDEX.doc_type
class StockDocument(DocType):
    """Stock Elasticsearch document."""

    id = fields.IntegerField(attr='id')

    stock_name = fields.StringField(
        analyzer=html_strip,
        fields={
            'raw': fields.StringField(analyzer='keyword', fielddata=True),
        }
    )

    opening_price = fields.FloatField()
        # analyzer=html_strip,
        # fields={
        #     'raw': fields.FloatField(analyzer='keyword'),
        # }
    # )

    # summary = fields.StringField(
    #     analyzer=html_strip,
    #     fields={
    #         'raw': fields.StringField(analyzer='keyword'),
    #     }
    # )

    # publisher = fields.StringField(
    #     attr='publisher_indexing',
    #     analyzer=html_strip,
    #     fields={
    #         'raw': fields.StringField(analyzer='keyword'),
    #     }
    # )

    # pub_date = fields.DateField()

    # state = fields.StringField(
    #     analyzer=html_strip,
    #     fields={
    #         'raw': fields.StringField(analyzer='keyword'),
    #     }
    # )

    # isbn = fields.StringField(
    #     analyzer=html_strip,
    #     fields={
    #         'raw': fields.StringField(analyzer='keyword'),
    #     }
    # )

    closing_price = fields.FloatField()

    percentage = fields.FloatField()
    highest_price = fields.FloatField()
    gains = fields.FloatField()
    loses = fields.FloatField()
    lowest_price = fields.FloatField()

    class Meta():
        """Meta options."""

        model = Stock  # The model associate with this DocType