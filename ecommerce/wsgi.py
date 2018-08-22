"""
WSGI config for ecommerce project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
from import_env import read_env
from django.core.wsgi import get_wsgi_application

'''set credential before application run on server, because applicaion do not
run by manage.py anymore on server.
'''
read_env('.env')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce.settings")

application = get_wsgi_application()
