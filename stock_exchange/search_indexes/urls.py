
# from django.conf.urls import include, url
# from django.urls import path, re_path
from rest_framework.routers import DefaultRouter
from .views import (
    StockDocumentView
    )
router = DefaultRouter()
router.register(r'stocks', StockDocumentView, base_name='apiv1_stockview')
urlpatterns = []
urlpatterns += router.urls