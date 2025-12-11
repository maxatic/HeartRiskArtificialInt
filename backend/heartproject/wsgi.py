"""
WSGI config for heartproject.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'heartproject.settings')
application = get_wsgi_application()

