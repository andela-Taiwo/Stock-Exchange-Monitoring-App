import os
import pytz
from datetime import datetime
from django.urls.exceptions import NoReverseMatch
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from users.models import (Role, Permission, User)
from users.tests import factory as user_factory
from allauth.account.models import (
    EmailAddress
)
from django.core.files.uploadedfile import SimpleUploadedFile
from allauth.utils import get_user_model


class TestStockAPI(APITestCase):
   
    def setUp(self):
        permissions_setup = [
            ('roles', 'list'),
            ('roles', 'create'),
            ('roles', 'update'),
            ('roles', 'retrieve'),
            ('user.role', 'list'),
            ('user.role', 'update'),
            ('user', 'retrieve'),
            ('user', 'retrieve-any'),

        ]
        permissions = []

        for perm in permissions_setup:
            resource, action = perm
            permissions.append(
                Permission.objects.create(resource=resource, action=action)
            )

        self.role = Role.objects.create(label='Admin')
        Role.objects.create(label='User')
        for permission in permissions:
            self.role.permissions.add(permission)

        self.invalid_token = 'Eyhbfhebjwkfbhjbuw3hiuhufhnffjjfjkhjfghgbsvvsk74576b873875t378568'
        self.user = user_factory._create_user(self,email='testadmin@gmail.com')
        self.user.profile.roles.add(self.role)
        self.date_ = datetime.now().strftime('%Y-%m-%d')
        

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

    def test_create_role(self):
        user = self._create_login_user_with_verified_email()
        User.objects.get(id=(user.data['user']['pk'])).profile.roles.add(self.role)
        
        data = {
            "label": 'operator'
        }
        response = self.client.post(
            reverse(
                'apiv1_roles-list'
            ),
            data=data,
            HTTP_AUTHORIZATION='Bearer {}'.format(user.data['token']),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['payload']['label'], data['label'])


    def test_list_roles(self):
        user = self._create_login_user_with_verified_email()
        User.objects.get(id=(user.data['user']['pk'])).profile.roles.add(self.role)
        response = self.client.get(
            reverse(
                'apiv1_roles-list'
            ),
            data={
            },
            HTTP_AUTHORIZATION='Bearer {}'.format(user.data['token']),
        )
        user_roles = User.objects.get(id=(user.data['user']['pk'])).profile.roles.count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['payload']), user_roles)


    def test_update_role(self):
        user = self._create_login_user_with_verified_email()
        User.objects.get(id=(user.data['user']['pk'])).profile.roles.add(self.role)
        data = {
            'label': 'Fellow'
        }
        response = self.client.put(
            reverse(
                'apiv1_roles-detail', args=[user.data['user']['pk']]
            ),
            data=data,
            HTTP_AUTHORIZATION='Bearer {}'.format(user.data['token']),
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['payload']['label'], 'Fellow')

    def test_update_user_roles(self):
        user = self._create_login_user_with_verified_email()
        User.objects.get(id=(user.data['user']['pk'])).profile.roles.add(self.role)
        data = {
            'roles': [1]
        }
        response = self.client.put(
            reverse(
                'apiv1_user_roles-update-user-roles', args=[user.data['user']['pk']]
            ),
            data=data,
            HTTP_AUTHORIZATION='Bearer {}'.format(user.data['token']),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['payload']['roles'], data['roles'])

    
    def test_list_user_roles(self):
        user = self._create_login_user_with_verified_email()
        User.objects.get(id=(user.data['user']['pk'])).profile.roles.add(self.role)
        data = {
            'roles': [1]
        }
        response = self.client.get(
            reverse(
                'apiv1_user_roles-list-user-roles', args=[user.data['user']['pk']]
            ),
            data=data,
            HTTP_AUTHORIZATION='Bearer {}'.format(user.data['token']),
        )
        user_roles = User.objects.get(id=(user.data['user']['pk'])).profile.roles.count()
 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['payload']['roles']), user_roles)
        

class TestStockAPIExceptions(TestStockAPI):

    def test_can_not_create_role_without_permission(self):
        user = self._create_login_user_with_verified_email()    
        data = {
            "label": 'operator'
        }
        response = self.client.post(
            reverse(
                'apiv1_roles-list'
            ),
            data=data,
            HTTP_AUTHORIZATION='Bearer {}'.format(user.data['token']),
        )
        self.assertEqual(response.status_code, 403)



    def test_can_not_list_roles_without_permission(self):
        user = self._create_login_user_with_verified_email()
        response = self.client.get(
            reverse(
                'apiv1_roles-list'
            ),
            data={
            },
            HTTP_AUTHORIZATION='Bearer {}'.format(user.data['token']),
        )
        self.assertEqual(response.status_code, 403)
     
    def test_can_not_update_user_roles_with_invalid_data(self):
        user = self._create_login_user_with_verified_email()
        User.objects.get(id=(user.data['user']['pk'])).profile.roles.add(self.role)
        response = self.client.put(
            reverse(
                'apiv1_roles-detail', args=[user.data['user']['pk']]
            ),
            data={
            },
            HTTP_AUTHORIZATION='Bearer {}'.format(user.data['token']),
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['label'][0], 'This field is required.')
