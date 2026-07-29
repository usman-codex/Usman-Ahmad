"""
WSGI config for portfolio project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import time

from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')

application = get_wsgi_application()

# Use atomic file locking to prevent Gunicorn workers from running migrations concurrently on SQLite
lock_file = '/tmp/django_migration.lock'
try:
    fd = os.open(lock_file, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    try:
        print("Running database migrations programmatically on startup...")
        call_command('migrate', interactive=False)
        print("Database migrations applied successfully!")
    finally:
        os.close(fd)
except FileExistsError:
    print("Another worker is running migrations. Waiting...")
    time.sleep(3)
except Exception as e:
    print(f"Error running database migrations: {e}")
