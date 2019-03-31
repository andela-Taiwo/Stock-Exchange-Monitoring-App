from django.db import models
from users.models import User

# Create your models here.

class Stock(models.Model):
    # author = models.ForeignKey(User, related_name='%(class)s_author', on_delete=models.PROTECT, blank=True, null=True)
    opening_price = models.DecimalField(decimal_places=2, max_digits=6)
    highest_price = models.DecimalField(decimal_places=2, max_digits=6)
    lowest_price = models.DecimalField(decimal_places=2, max_digits=6)
    closing_price = models.DecimalField(decimal_places=2, max_digits=6)
    gains = models.DecimalField(decimal_places=2, max_digits=6)
    loses = models.DecimalField(decimal_places=2, max_digits=6)
    percentage = models.DecimalField(decimal_places=2, max_digits=6)
    stock_name = models.CharField(max_length=100)
    pub_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['pub_date']
    


class Portfolio(models.Model):
    owner = models.ForeignKey(User, related_name='%(class)s_owner', on_delete=models.PROTECT)
    stocks = models.ForeignKey(Stock, related_name='user_stocks', on_delete=models.PROTECT, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UploadedCSV(models.Model):
    stocks = models.ForeignKey(Stock, related_name='%(class)s_stocks', on_delete=models.PROTECT, blank=True, null=True)
    url = models.TextField()
    key = models.TextField()
