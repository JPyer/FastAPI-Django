"""
WSGI config for goatfish project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from fastapi import FastAPI

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'goatfish.settings')
application = get_wsgi_application()
from main.urls import router as main_router

app = FastAPI(
    title="Goatfish",
    description="A demo project. Also, an actual fish with a weird name.",
    version="We aren't doing versions yet. Point oh.",
)

app.include_router(main_router, prefix="/api")
