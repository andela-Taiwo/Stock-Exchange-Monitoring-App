import os
import pytz
from datetime import datetime
from django.urls.exceptions import NoReverseMatch
from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from stocks.models import Stock
from users.tests import factory as user_factory
from allauth.account.models import (
    EmailAddress
)
from django.core.files.uploadedfile import SimpleUploadedFile
from allauth.utils import get_user_model


class TestStockAPI(APITestCase):
   
    def setUp(self):
        self.invalid_token = 'Eyhbfhebjwkfbhjbuw3hiuhufhnffjjfjkhjfghgbsvvsk74576b873875t378568'
        self.user = user_factory._create_user(self,email='testadmin@gmail.com')
        self.date_ = datetime.now().strftime('%Y-%m-%d')
        self.stock = Stock.objects.create(
            opening_price=92.00,
            closing_price=167.00,
            lowest_price=178.00,
            highest_price=203,
            gains=75.00,
            loses=0.00,
            percentage=0.45,
            stock_name='Apple'
        )

        self.stock2 = Stock.objects.create(
            opening_price=115.00,
            closing_price=105.00,
            lowest_price=95.00,
            highest_price=217.00,
            gains=0,
            loses=-10,
            percentage=0.1,
            stock_name='ABC'
        )
        self.stock3 = Stock.objects.create(
            opening_price=92.00,
            closing_price=167.00,
            lowest_price=178.00,
            highest_price=203,
            gains=75.00,
            loses=0.00,
            percentage=0.45,
            stock_name='Samsung'
        )

    def _create_login_user_with_verified_email(self, email='user@example.com', password='$testeR1234', user_status=False):
        """Tests login """
        user = get_user_model().objects.create(email=email, password=password)
        user.set_password(password)
        user.is_staff = user_status
        user.save()
        EmailAddress.objects.create(user=user,
                                    email=email,
                                    primary=True,
                                    verified=True)
        response = self.client.post(reverse('account_login'),
                                {'email': email,
                                 'password': password})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['user']['email'], email)
        return response

    def test_upload_stock_data_csv(self):
        user = self._create_login_user_with_verified_email()
        base_path = os.path.dirname(os.path.realpath(__file__))
        with open(base_path + '/stocks.csv', 'rb') as f:
            file_upload = SimpleUploadedFile(content = f.read(), name = f.name)
            data = {
                "stock_file": file_upload
            }
            response = self.client.post(
                reverse(
                    'apiv1_stock-list'
                ),
                data=data,
                HTTP_AUTHORIZATION='Bearer {}'.format(user.data['token']),
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.data['payload']), 11)


    def test_list_stocks(self):
        user = self._create_login_user_with_verified_email()
        response = self.client.get(
            reverse(
                'apiv1_stock-list'
            ),
            data={
            },
            HTTP_AUTHORIZATION='Bearer {}'.format(user.data['token']),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['payload']['top_gainers']), 2)
        self.assertEqual(len(response.data['payload']['top_losers']), 1)


    def test_list_company_stocks_for_a_week(self):
        user = self._create_login_user_with_verified_email()
        
        response = self.client.get(
            reverse(
                'apiv1_stock-filter-per-week', args=['ABC', self.date_]
            ),
            data={},
            HTTP_AUTHORIZATION='Bearer {}'.format(user.data['token']),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['payload']), 1)
        self.assertEqual(response.data['payload'][0]['stock_name'], 'ABC')


class TestStockAPIExceptions(TestStockAPI):
    def test_can_not_list_stocks_without_valid_token(self):
        response = self.client.get(
            reverse(
                'apiv1_stock-list'
            ),
            data={
            },
            HTTP_AUTHORIZATION='Bearer {}'.format(self.invalid_token),
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data.get('detail'), 'Error decoding signature.')

    def test_can_not_list_company_stocks_for_a_week_without_valid_token(self):
        
        response = self.client.get(
            reverse(
                'apiv1_stock-filter-per-week', args=['ABC', self.date_]
            ),
            data={},
            HTTP_AUTHORIZATION='Bearer {}'.format(self.invalid_token),
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data.get('detail'), 'Error decoding signature.')

    def test_can_not_upload_stock_csv_without_valid_token(self):
        file_upload = SimpleUploadedFile('file3.csv', b'content')
        data = {
            "stock_file": file_upload
        }
        response = self.client.post(
            reverse(
                'apiv1_stock-list'
            ),
            data=data,
            HTTP_AUTHORIZATION='Bearer {}'.format(self.invalid_token),
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data.get('detail'), 'Error decoding signature.')

    def test_can_not_upload_file_with_invalid_format(self):
        user = self._create_login_user_with_verified_email()
        file_upload = SimpleUploadedFile('file3.jpeg', b'content')
        data = {
            "stock_file": file_upload
        }
        response = self.client.post(
            reverse(
                'apiv1_stock-list'
            ),
            data=data,
            HTTP_AUTHORIZATION='Bearer {}'.format(user.data['token']),
        )
        self.assertEqual(response.status_code, 406)
        self.assertEqual(response.data.get('detail'), 'Please select stock data to upload')
