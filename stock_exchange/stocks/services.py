
import csv
import pytz
from datetime import datetime, timedelta
from rest_framework import exceptions
from helpers.date_helper import (get_week, normalize_week_begin)
from stocks.models import Stock
from stocks.serializers import (
    CreateStocksSerializer, 
    StockSerializer,
    PortfolioSerializer
)


def decode_utf8(input_iterator):
    for l in input_iterator:
        yield l.decode('utf-8')

def get_percentage(opening_price, closing_price):
    percentage = 0.00
    try:
        percentage = (closing_price - opening_price) / (closing_price)
        percentage = "%.2f" % percentage
    except:
        raise exceptions.NotAcceptable(detail='Closing price can not be zero')
    return float(percentage)

def load_stock(requestor, stock_csv):
    reader = csv.DictReader(decode_utf8(stock_csv))
    result = []
    for row in reader:
        opening_price = float(row.get('openingPrice', 0.00))
        closing_price = float(row.get('closingPrice', '0.00'))
        lowest_price = float(row.get('lowestPrice', 0.00))
        highest_price = float(row.get('highestPrice', 0.00))
        stock_name = row.get('stockName')
        data_info = {
            'opening_price': opening_price,
            'closing_price': closing_price,
            'stock_name': stock_name,
            'lowest_price': lowest_price,
            'highest_price': highest_price,
            'gains': (closing_price - opening_price) if (closing_price - opening_price) > 0 else 0.00,
            'loses': (closing_price - opening_price) if (closing_price - opening_price) < 0 else 0.00,
            'percentage': get_percentage(opening_price, closing_price)
        }
        serializer = CreateStocksSerializer(data=data_info)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            result.append(serializer.data)
    
    return result

def list_stocks(requestor, query_params):
    today = datetime.now(tz=pytz.UTC)
    today_begins = today.replace(hour=0, minute=0, second=0, microsecond=0)
    today_ends = today_begins + timedelta(days=1)
    stocks = Stock.objects.filter(
        pub_date__range=(today_begins, today_ends)
    ).order_by('-gains', 'pub_date')

    return stocks

def filter_stock_per_week(requestor, query_params, stock_name, week):
    ''' List the stock for a company in a given week '''
    week = get_week(week)
    week_begin = normalize_week_begin(week)
    week_end = week_begin + timedelta(days=7)
    stocks = Stock.objects.filter(
        pub_date__gte=week_begin, pub_date__lte=week_end, stock_name=stock_name
        ).order_by('-gains', 'loses', 'pub_date')
    return stocks
