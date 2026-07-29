"""
ASGI config for portfolio project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os
import time

from django.core.asgi import get_asgi_application
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')

application = get_asgi_application()

# Use atomic file locking to prevent ASGI workers from running migrations concurrently on SQLite
lock_file = '/tmp/django_migration_asgi.lock'
try:
    fd = os.open(lock_file, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    try:
        print("Running database migrations programmatically on ASGI startup...")
        call_command('migrate', interactive=False)
        print("Database migrations applied successfully!")
    finally:
        os.close(fd)
except FileExistsError:
    print("Another worker is running migrations on ASGI startup. Waiting...")
    time.sleep(3)
except Exception as e:
    print(f"Error running database migrations: {e}")
