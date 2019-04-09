import json

# from rest_framework import serializers
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from search_indexes.documents.stocks import StockDocument



class StockDocumentSerializer(DocumentSerializer):
    """Serializer for the Book document."""

    class Meta(object):
        """Meta options."""

        # Specify the correspondent document class
        document = StockDocument

        # List the serializer fields. Note, that the order of the fields
        # is preserved in the ViewSet.
        fields = (
            "id",
            "stock_name"
            "opening_price",
            "closing_price",
            "lowest_price",
            "pub_date",
            "gains",
            "loses",
            "percentage",    
        )