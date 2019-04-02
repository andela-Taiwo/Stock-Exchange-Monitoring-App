from django.contrib.auth.models import User
from allauth.utils import get_user_model
from users.models import Profile, Role, Permission


def _create_user(self, email='johndoe@gmail.com', password='tester123'):
    user = get_user_model().objects.create(
        email=email, password=password,
        is_active=True)
    if password:
        user.set_password(password)
    else:
        user.set_unusable_password()
    user.save()
    return user
    