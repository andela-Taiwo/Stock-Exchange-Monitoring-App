from django.core.management.base import BaseCommand, CommandError
from  users.models import (User, Role, Permission)
from django.conf import settings
from django.contrib.sites.models import Site

class Command(BaseCommand):

    def add_user_roles(self, roles_and_permissions):
        ''' Creates multiple roles each with permissions passed as list of pair tuples (resource, action) '''
        ''' Generally just use `add_user_permissions`. '''

        assert isinstance(roles_and_permissions, list) or isinstance(roles_and_permissions, tuple)

        for role_name, role_permissions in roles_and_permissions:
            role = Role.objects.create(label=role_name)
            for resource, action in role_permissions:
                permission, _ = Permission.objects.get_or_create(resource=resource, action=action)
                role.permissions.add(permission)
 

    def handle(self, *args, **options):
        
        # admin_permissions = [
        #     ('roles', 'list'),
        #     ('roles', 'create'),
        #     ('roles', 'update'),
        #     ('roles', 'retrieve'),
        #     ('user.role', 'list'),
        #     ('user.role', 'update'),
        #     ('user', 'retrieve'),
        #     ('user', 'retrieve-any'),
        #     ('stocks', 'list'),
        #     ('stocks', 'upload'),
        #     ('stocks', 'filter'),
        # ]
        # user_permissions = [
        #     ('stocks', 'list'),
        #     ('stocks', 'filter'),
        # ]
        # roles_user = (
        #     ('Admin', admin_permissions),
        #     ('User', user_permissions)
        # )
        
        # self.add_user_roles(roles_user)
        # admin = User.objects.filter(email=settings.ADMIN_USER_EMAIL)
        # if admin.exists():
        #     admin = admin.first()
        #     admin.is_admin = True
        #     admin.is_superuser = False
        #     admin.save()
        #     admin.profile.roles.add(Role.objects.get(label='Admin'))
        # site = Site.objects.get(domain='example.com')
        # site.domain='stock-exchange-env.qdtzm52k3p.us-east-1.elasticbeanstalk.com'
        # site.name='elasticbeanstalk.com'
        # site.save()
        self.stdout.write('Successfully created created roles')

        