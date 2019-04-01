from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from rest_auth.serializers import PasswordResetConfirmSerializer
from django.contrib.auth import get_user_model
from rest_framework import generics
from django.utils.translation import ugettext_lazy as _
from rest_auth.registration.serializers import VerifyEmailSerializer
from rest_framework import status
from rest_framework.decorators import api_view, APIView
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import exceptions

from rest_auth.views import LoginView
from rest_framework import (
    viewsets,
    decorators
)
import users.services as user_service
from users.serializers import (
    UserSerializer, 
    ProfileSerializer,
    FileUploadSerializer,
    ViewProfileSerializer
    )
from rest_framework import authentication, permissions
from api.response import NSEMonitoringAPIResponse

# Create your views here.
@api_view()
def django_rest_auth_null():
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view()
def complete_view(request):
    return Response("Email account is activated")

class UserViewSet(viewsets.ViewSet):
    ''' User Profile views '''

    def retrieve(self, request, *args, **kwargs):
        profile = user_service.retrieve_profile(
            requestor=request.user,
            profile_id=kwargs.get('pk')
        )
        return NSEMonitoringAPIResponse(ViewProfileSerializer(profile).data)


    
class UploadViewSet(viewsets.ViewSet):
    def create(self, request):
        try:
            profile_picture = request.FILES['picture']
        except:
            raise exceptions.NotAcceptable(detail='Please select picture to upload')
        profile = user_service.upload_profile_picture(
            data=request.data,
            requestor=request.user, 
            file=profile_picture
        )
        return NSEMonitoringAPIResponse(FileUploadSerializer(profile).data)

    def update(self, request, **kwargs):
        try:
            profile_picture = request.FILES['picture']
        except:
            raise exceptions.NotAcceptable(detail='Please select picture to upload')
        profile = user_service.update_profile_picture(
            requestor=request.user,
            file=profile_picture,
            upload_id=kwargs.get('pk')
          
        )
        return NSEMonitoringAPIResponse(FileUploadSerializer(profile).data)

    def delete(self, request, **kwargs):
        try:
            profile_picture = request.FILES['picture']
        except:
            profile_picture = None
        profile = user_service.delete_profile_picture(
            requestor=request.user,
            file=profile_picture,
            upload_id=kwargs.get('pk')
          
        )
        return NSEMonitoringAPIResponse(FileUploadSerializer(profile).data)

class CustomLoginView(LoginView):
    def get_response(self):
        orginal_response = super().get_response()
        mydata = {"message": "You have successfully logged in", "status": "success"}
        orginal_response.data.update(mydata)
        return orginal_response

class RolesViewSet(viewsets.ViewSet):
    def list(self, request, **kwargs):
        roles = user_service.list_roles(request.user)
        return NSEMonitoringAPIResponse(user_service.serialize_roles(request.user, roles, many=True, compact=True))

    def retrieve(self, request, **kwargs):
        role = user_service.retrieve_role(request.user, role_pk=kwargs.get('pk'))
        return NSEMonitoringAPIResponse(user_service.serialize_roles(request.user, role))

    def update(self, request, **kwargs):
        role = user_service.update_role(request.user, role_pk=kwargs.get('pk'), data=request.data)
        return NSEMonitoringAPIResponse(user_service.serialize_roles(request.user, role))

    @decorators.action(methods=['GET'], detail=False, url_path='init')
    def init(self, request, **kwargs):
        role = user_service.init_role(request.user)
        return NSEMonitoringAPIResponse(user_service.serialize_roles(request.user, role))

    def create(self, request, **kwargs):
        role = user_service.create_role(request.user, data=request.data)
        return NSEMonitoringAPIResponse(user_service.serialize_roles(request.user, role))


class UserRolesViewSet(viewsets.ViewSet):
    
    @decorators.action(methods=['GET'], detail=True, url_path='list')
    def list_user_roles(self, request, **kwargs):
        roles = user_service.list_user_roles(request.user, profile_pk=kwargs.get('pk'))
        return NSEMonitoringAPIResponse(user_service.serialize_user_roles(request.user, roles))

    @decorators.action(methods=['PUT'], detail=True, url_path='update')
    def update_user_roles(self, request, **kwargs):
        roles = user_service.update_user_roles(request.user, profile_pk=kwargs.get('pk'), data=request.data)
        return NSEMonitoringAPIResponse(user_service.serialize_user_roles(request.user, roles))
<<<<<<< HEAD
=======

>>>>>>> add permissions
