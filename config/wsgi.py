"""
WSGI config for task_manager project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""
import os, sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
# add the hellodjango project path into the sys.path
sys.path.append(BASE_DIR)

# add the virtualenv site-packages path to the sys.path
sys.path.append(os.path.join(BASE_DIR, '.env', 'lib', 'python3.10', 'site-packages'))


from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
