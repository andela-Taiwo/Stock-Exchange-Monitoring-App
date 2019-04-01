import warnings
from rest_framework import exceptions

from users.models import User
from users.permissions import PERMISSIONS

from django.conf import settings

PermissionDenied = exceptions.PermissionDenied


class UserPermissions:
    def __init__(self, requestor_user, resource=None):
        profile = None
        if isinstance(requestor_user, User):
            profile = requestor_user.profile
        else:
            raise AssertionError('invalid argument')

        permissions = []
        for role in profile.roles.all():
            for permission in role.permissions.all():
                permissions.append((permission.resource, permission.action))
        self.permissions = set(permissions)
        self.requestor = profile.user
        self.resource = resource

    def get_args(self, *args):
        if len(args) == 1:
            assert(self.resource is not None)
            resource = self.resource
            action = args[0]
        elif len(args) == 2:
            resource = args[0]
            action = args[1]

        return resource, action

    def has(self, *args, **kwargs):
        permission = self.get_args(*args)
        if permission in self.permissions:
            function = getattr(PERMISSIONS, '{}_{}'.format(*permission), None)
            if function is not None:
                return function(self, **kwargs)
            return True
        return False

    def check(self, *args, **kwargs):
        permission = self.get_args(*args)
        if self.has(*args, **kwargs) is False:
            if settings.DEBUG is True:
                raise PermissionDenied('Missing permission {}.{}'.format(*permission))
            else:
                raise PermissionDenied('Forbidden')


def has_permission(requestor, resource, action, **kwargs):
    return UserPermissions(requestor, resource=resource).has(action, **kwargs)


def check_permission(requestor, resource, action, **kwargs):
    return UserPermissions(requestor, resource=resource).check(action, **kwargs)
