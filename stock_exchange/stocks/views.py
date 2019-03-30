from django.shortcuts import render
from rest_framework import (
    viewsets,
    decorators
)
from rest_framework import exceptions
from stocks.serializers import (
    StockSerializer, PortfolioSerializer
)
from users.serializers import UserSerializer
from rest_framework import authentication, permissions
from api.response import NSEMonitoringAPIResponse
# import flight.services as flight_services


# Create your views here.
class StockViewSet(viewsets.ViewSet):
    pass