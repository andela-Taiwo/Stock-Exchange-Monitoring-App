"""
WSGI config for stock_exchange project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
<<<<<<< HEAD
<<<<<<< HEAD
=======
from whitenoise.django import DjangoWhiteNoise
>>>>>>> fixing css issues
=======
>>>>>>> fixing csss

application = get_wsgi_application()
