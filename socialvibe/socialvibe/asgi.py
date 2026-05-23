"""
ASGI config for socialvibe project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os
import sys
from pathlib import Path

# Add the parent directory of this file to sys.path so 'App' can be found
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'socialvibe.settings')

application = get_asgi_application()
