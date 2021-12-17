"""
WSGI config for MeiduoRegisterLogin project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MeiduoRegisterLogin.settings')

# 自定义配置路径.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MeiduoRegisterLogin.settings.dev')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MeiduoRegisterLogin.settings.pro')

application = get_wsgi_application()
