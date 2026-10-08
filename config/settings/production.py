import os

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F403

if not os.getenv("DATABASE_URL"):
    raise ImproperlyConfigured("DATABASE_URL é obrigatória em produção.")
if SECRET_KEY == "unsafe-development-key-change-me":  # noqa: F405
    raise ImproperlyConfigured("DJANGO_SECRET_KEY segura é obrigatória em produção.")

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
