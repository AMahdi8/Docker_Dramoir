from .common import *
import os
import environ

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    'https://api.dramoir.com',
    'https://www.api.dramoir.com',
    'https://dramoir.com',
    'https://www.dramoir.com',
]

DEBUG = env.bool("DEBUG", default=False)
SECRET_KEY = env("SECRET_KEY")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

CSRF_TRUSTED_ORIGINS = [
    'https://api.dramoir.com',
    'https://www.api.dramoir.com',
    'https://dramoir.com',
    'https://www.dramoir.com',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env("DATABASE_NAME"),
        'USER': env("DATABASE_USER"),
        'PASSWORD': env("DATABASE_PASSWORD"),
        'HOST': env("DATABASE_HOST", default="localhost"),
        'PORT': env("DATABASE_PORT", default="5432"),
    }
}

SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
