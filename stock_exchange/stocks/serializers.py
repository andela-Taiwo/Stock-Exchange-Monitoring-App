from django.db import models
from dateutil.parser import parse
from rest_framework import serializers
from .models import (
  Stock, Portfolio
)
from users.serializers import UserSerializer
from users.models import Profile


class CreateStocksSerializer(serializers.ModelSerializer):
    
    ''' Serializer for loading the stocks data'''
    class Meta:
        model = Stock
        fields = [
            "id",
            "opening_price",
            "closing_price",
            "lowest_price"
        ]


class StockSerializer(serializers.ModelSerializer):
    ''' Serializer for retrieving the stocks data'''

    class Meta:
        model = Stock
        fields = [
            "id",
            "opening_price",
            "closing_price",
            "lowest_price",
            "pub_date",
            "gains",
            "loses",
            "percentage"
        ]


class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        stocks = StockSerializer(many=True, read_only=True)
        owner = UserSerializer(read_only=True)
        fields = [
            "stocks",
            "owner"
        ]