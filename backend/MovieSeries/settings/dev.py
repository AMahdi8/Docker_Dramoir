from .common import *

DEBUG = True

ALLOWED_HOSTS = ['*']

SECRET_KEY = 'django-insecure-tl=)s2b@0&(+^s!2rni9iqxs@@p68et4&_@f7v+-_ll5&$1sm+'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
BASE_URL = "http://127.0.0.1:8000"

# CORS settings for development
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# Celery settings
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# Use console email backend for development
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Celery settings for development
CELERY_TASK_ALWAYS_EAGER = False  # Use worker processes for task execution
# Propagate exceptions when tasks are executed locally
CELERY_TASK_EAGER_PROPAGATES = True
CELERY_TASK_TRACK_STARTED = True  # Track started tasks

# Update logging for Celery
LOGGING['loggers']['celery'] = {
    'handlers': ['console'],
    'level': 'DEBUG',
    'propagate': True,
}
