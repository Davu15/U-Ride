"""
WSGI config for u_ride project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'u_ride.settings')

application = get_wsgi_application()
