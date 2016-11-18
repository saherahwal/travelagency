"""
WSGI config for ota project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

import os
import sys

sys.path.append('/home/escanzaadmin/escanza/travelagency/ota')

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ota.settings")

os.environ.setdefault("PYTHON_EGG_CACHE", "/home/escanzaadmin/escanza/travelagency/ota/egg_cache")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ota.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
