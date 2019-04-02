import json
from rest_framework.generics import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import exceptions
from rest_framework import serializers
from rest_framework.exceptions import APIException
from django.db import (
    transaction,
    IntegrityError,
    models
)
from api.s3_services import (
    s3_delete,
    s3_upload,
    s3_presigned_url
)
from users.models import (
  Profile, Upload, Role, Permission
)

from users.roles import (UserPermissions, has_permission, check_permission)
from users.permissions import (
    PERMISSION_READ, PERMISSION_WRITE, PERMISSIONS, PERMISSION_LEVELS
)
from users.serializers import ProfileSerializer, FileUploadSerializer



def make_file_key(category, name):
    return 'media/{}/{}'.format(category, name)

# def update_user(requestor, user_id, data):
#     user = get_object_or_404(User, id=user_id)
#     serializer = UserSerializer(
#         user,
#         data=data
#     )
#     if serializer.is_valid(raise_exception=True):
#         serializer.save()
#     return serializer.data

def deserialize_profile(upload, action, data, serializer_class):
    '''Deserialize and validate profile'''
    assert action == 'create' or action == 'update'
 
    serializer = serializer_class(
        instance=upload,
        partial=(action == 'update'),
        data=data
    )
    serializer.is_valid(raise_exception=True)  
    validated_data = serializer.validated_data
    validated_data.pop('uploader', None)
    for name, value in validated_data.items():
        setattr(upload, name, value)
    return upload

def create_or_update_profile_pic(requestor, file, uploaded_profile):
    profile = get_object_or_404(Profile, id=requestor.profile.pk)
    file_key = make_file_key("photo", file.name)
    s3obj = s3_upload(
            filekey=file_key,
            filebody=file.read(), 
            filename=file.name,
            uploader_pk=requestor.profile.pk,
            description='profile'
        )
    
    file_url = s3_presigned_url(file_key)

    try:
        file = Upload.objects.get(profile_picture_key=file_key)
        file.profile = profile
        file.profile_picture_name = file.name
        file.profile_picture_key = file_key
        file.profile_picture_url = file_url
        file.save()
        return file
    except Upload.DoesNotExist:
        # We're uploading this file for the first time
        uploaded_profile.profile = profile
        uploaded_profile.profile_picture_name = file.name
        uploaded_profile.profile_picture_key = file_key
        uploaded_profile.profile_picture_url = file_url
        uploaded_profile.save()
        return uploaded_profile

def upload_profile_picture(requestor, data, file):
    data.pop('picture', None)
    data = data.copy()
    
    if file is None:
        return []
    with transaction.atomic():  
   
        file_key = make_file_key("photo", file.name)
        profile = get_object_or_404(Profile, id=requestor.profile.pk)
        upload = Upload()
        # data['profile'] = profile
        uploaded_profile = deserialize_profile(
                upload=upload,
                action='create',
                data=data,
                serializer_class=FileUploadSerializer
        )
        s3obj = s3_upload(
            filekey=file_key,
            filebody=file.read(), 
            filename=file.name,
            uploader_pk=requestor.profile.pk,
            description='profile'
        )
        file_url = s3_presigned_url(file_key)
        uploaded_profile.profile = profile
        uploaded_profile.profile_picture_name = file.name
        uploaded_profile.profile_picture_key = file_key
        uploaded_profile.profile_picture_url = file_url
        uploaded_profile.save()
    return uploaded_profile

def retrieve_profile_picture(requestor, upload_id):
    profile_pic = get_object_or_404(Upload, id=upload_id)
    if requestor.is_staff or profile_pic.profile.user == requestor:
        return profile_pic
    raise exceptions.PermissionDenied('Not authorized to view the profile')


def delete_profile_picture(requestor, file, upload_id):
    profile_pic = retrieve_profile_picture(requestor, upload_id)
    if requestor.is_staff or requestor == profile_pic.profile.user:
        s3_delete(profile_pic.profile_picture_key)
        return profile_pic.delete()
    raise exceptions.PermissionDenied('Not authorized to perform the action.')

def update_profile_picture(requestor, file, upload_id):
    # if requestor.is_staff or requestor == profile_pic.profile.user:
    profile_pic = retrieve_profile_picture(requestor, upload_id)  
    if file is None:
        return []
    with transaction.atomic():  
        # data['profile'] = profile
        uploaded_profile = deserialize_profile(
                upload=profile_pic,
                action='update',
                data={},
                serializer_class=FileUploadSerializer
        )
        upload = create_or_update_profile_pic(requestor, file, uploaded_profile)
    return upload

def retrieve_profile(requestor, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)

    if requestor.is_staff or requestor.id == profile.user_id:
        return profile
    raise exceptions.PermissionDenied()



class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = [
            'id',
            'label',

        ]



class CompactRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = [
            'id',
            'label'
        ]


def serialize_roles(requestor, roles, *, many=False, compact=False):
    serializer = RoleSerializer if compact is False else CompactRoleSerializer
    return serializer(roles, many=many).data


def list_roles(requestor):
    permissions = UserPermissions(requestor, 'roles')
    permissions.check('list')

    roles = Role.objects.all()

    return roles


def retrieve_role(requestor, *, role_pk):
    permissions = UserPermissions(requestor, 'roles')
    permissions.check('retrieve')

    role = get_object_or_404(Role, pk=role_pk)

    return role


def init_role(requestor):
    permissions = UserPermissions(requestor, 'roles')
    permissions.check('create')

    role = Role()

    return role


def _save_role(requestor, role_pk, data):
    role = None

    with transaction.atomic():
        if role_pk is not None:
            role = retrieve_role(requestor, role_pk=role_pk)
        serializer = RoleSerializer(instance=role, data=data)
        serializer.is_valid(raise_exception=True)
        role = serializer.save()

    return role


def create_role(requestor, *, data):
    permissions = UserPermissions(requestor, 'roles')
    permissions.check('create')

    role = _save_role(requestor, None, data)

    return role


def update_role(requestor, *, role_pk, data):
    permissions = UserPermissions(requestor, 'roles')
    permissions.check('update')

    role = _save_role(requestor, role_pk, data)

    return role

#
# User roles
#


def serialize_user_roles(requestor, roles):
    return {
        'roles': [role.id for role in roles]
    }


def list_user_roles(requestor, *, profile_pk):
    permissions = UserPermissions(requestor, 'user.role')
    permissions.check('list')

    profile = retrieve_user(requestor, pk=profile_pk)

    roles = profile.roles.all()

    return roles


def update_user_roles(requestor, *, profile_pk, data):
    permissions = UserPermissions(requestor, 'user.role')
    permissions.check('update')

    profile = retrieve_user(requestor, pk=profile_pk)

    new_ids = set(data['roles'])

    # get_potus = None
    # try:
    #     get_potus = Role.objects.get(label='POTUS')
    # except:
    #     raise AssertionError('Role POTUS is not found in DB')
    # if get_potus.id in new_ids:
    #     raise exceptions.PermissionDenied(detail="")

    unchanged_ids = []
    roles = list(profile.roles.all())
    for role in roles:
        if role.id not in new_ids:
            profile.roles.remove(role)
        else:
            unchanged_ids.append(role.id)

    for id in (new_ids - set(unchanged_ids)):
        role = Role.objects.get(pk=id)
        profile.roles.add(role)

    return profile.roles.all()


# def get_permissions(user):
#     assert isinstance(user, User)
#     permissions = UserPermissions(user)

#     ui_permissions = {}
#     for p in permissions.permissions:
#         if p[0] == 'ui':
#             ui_permissions['{}.{}'.format(p[0], p[1])] = True
#     # print(ui_permissions)

def retrieve_user(requestor, pk):
    permissions = UserPermissions(requestor, 'user')
    permissions.check('retrieve')

    if permissions.has('retrieve-any'):
        return Profile.objects.get(pk=pk)

    elif permissions.has('retrieve-self'):
        if requestor.profile.pk != int(pk):
            raise exceptions.PermissionDenied(detail="")

        return Profile.objects.get(pk=pk)

    raise exceptions.PermissionDenied(detail="")
