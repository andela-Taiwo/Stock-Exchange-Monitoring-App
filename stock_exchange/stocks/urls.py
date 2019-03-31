from django.conf.urls import include, url
from django.urls import path, re_path
from rest_framework.routers import DefaultRouter
from .views import (
    StockViewSet
    )
router = DefaultRouter()
router.register(r'stock', StockViewSet, base_name='apiv1_stock')
urlpatterns = []
urlpatterns += router.urls
