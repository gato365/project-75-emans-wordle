"""
WSGI config for wordle_gato365 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys
print("Current Python sys.path:", sys.path)
## Begin 1: Logging Information
import logging 
logger = logging.getLogger(__name__)
## End 1: Logging Information

## Begin 2: Logging Information
logger.debug("Setting DJANGO_SETTINGS_MODULE")
## End 2: Logging Information


from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wordle_gato365.settings')

## Begin 3: Logging Information
logger.debug("Getting WSGI application")
## End 3: Logging Information

application = get_wsgi_application()

