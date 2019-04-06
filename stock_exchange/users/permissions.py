from collections import OrderedDict

PERMISSION_READ = 1
PERMISSION_WRITE = 2

PERMISSION_LEVELS = {
    PERMISSION_READ: 'read',
    PERMISSION_WRITE: 'write'
}

_PERMISSIONS = []


def _add(name, permissions):
    _PERMISSIONS.append((name, permissions))


_add('roles', {
    PERMISSION_READ: [
        ('roles', 'list'),
        ('roles', 'retrieve'),
        ('user.role', 'list'),
    ],
    PERMISSION_WRITE: [
        ('roles', 'create'),
        ('roles', 'update'),
        ('user.role', 'update'),
    ],
})


_add('user.list', {
    PERMISSION_READ: [
        ('user', 'list'),
        ('user', 'list-any'),
    ],
    PERMISSION_WRITE: [
        ('user', 'create'),
        ('user', 'create-operator'),
        ('user', 'create-client'),
    ]
})

_add('user.profile', {
    PERMISSION_READ: [
        ('ui', 'users.profile.view'),
        ('user', 'retrieve'),
        ('user', 'retrieve-any'),
        ('user', 'list-operators'),

    ],
    PERMISSION_WRITE: [

    ]
})

_add('stocks', {
    PERMISSION_WRITE: [
        ('stocks', 'upload-any'),
        ('stocks', 'upload'),
    ],
    PERMISSION_READ: [
        ('stocks', 'list'),
        ('stocks', 'list-all'),
        ('stocks', 'filter'),
    ]
})



PERMISSIONS = OrderedDict(_PERMISSIONS)
