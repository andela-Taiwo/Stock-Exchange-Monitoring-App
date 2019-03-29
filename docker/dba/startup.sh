#!/bin/sh

python3 ./stock_exchange/manage.py makemigrations && ./stock_exchange/manage.py migrate --no-input
