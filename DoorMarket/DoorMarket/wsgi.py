"""
WSGI config for DoorMarket project.
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DoorMarket.settings')

application = get_wsgi_application()
