import csv
from django.shortcuts import render
from rest_framework import (
    viewsets,
    decorators
)
from rest_framework import exceptions
from stocks.serializers import (
    StockSerializer, PortfolioSerializer, CreateStocksSerializer
)
from users.serializers import UserSerializer
from rest_framework import authentication, permissions
from api.response import NSEMonitoringAPIResponse
import stocks.services as stock_services


class StockViewSet(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        ''' Upload stock data'''
        try:
            stock_csv = request.FILES['stock_file']
            if not stock_csv.name.endswith('.csv'):
                raise exceptions.NotAcceptable(detail='Only csv format is allowed')
            elif(stock_csv.multiple_chunks()):
                raise exceptions.NotAcceptable(detail='File size too big')
        except:
            raise exceptions.NotAcceptable(detail='Please select stock data to upload')

        stocks = stock_services.load_stock(
            requestor=request.user,
            stock_csv=stock_csv
        )
        return NSEMonitoringAPIResponse(StockSerializer(stocks, many=True).data)
   
    def list(self, request):
        ''' List stocks for the the day '''
        stocks = stock_services.list_stocks(
            requestor=request.user,
            query_params=request.query_params
        )
        return NSEMonitoringAPIResponse(
            stocks
        )

    @decorators.action(
        methods=['get'],
        detail=False,
        url_path='company/(?P<name>[A-Za-z0-9_.\s]+)/week/(?P<week>[0-9+\-]+)'
        )
    def filter_per_week(self, request, *args, **kwargs):
        ''' View to list stock for a particular company in a given week'''
        stocks = stock_services.filter_stock_per_week(
            requestor=request.user,
            query_params=request.query_params,
            stock_name=kwargs.get('name'),
            week=kwargs.get('week'),
        ) 
        return NSEMonitoringAPIResponse(
            StockSerializer(stocks, many=True).data
        )
        