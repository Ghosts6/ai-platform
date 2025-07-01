import os
import logging
import dj_database_url
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from pathlib import Path
import sys

# Base directory & dotenv setup
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# ENV VARS
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() == "true"
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",")
IS_TESTING = os.getenv("TEST_MODE", "False") == "True"

# External Services
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
TEST_MODE = os.getenv("TEST_MODE", "False").lower() == "true"

# Microsoft Graph API credentials
MS_CLIENT_ID = os.getenv("MS_CLIENT_ID")
MS_CLIENT_SECRET = os.getenv("MS_CLIENT_SECRET")
MS_TENANT_ID = os.getenv("MS_TENANT_ID")
MS_REDIRECT_URI = os.getenv("MS_REDIRECT_URI")

# security settings
# # **Content Security Policy (CSP)**
# CSP_DEFAULT_SRC = ["'self'"]  
# CSP_SCRIPT_SRC = ["'self'"]  
# CSP_STYLE_SRC = ["'self'", "[https://trusted-cdn.com](https://trusted-cdn.com)"]  
# CSP_IMG_SRC = ["'self'", "data:"]  
# CSP_CONNECT_SRC = ["'self'"]  
# SECURE_REFERRER_POLICY = 'same-origin'

# CROSS config
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

CORS_ALLOW_CREDENTIALS = True

# Installed apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "agent",
    "core_services",
    "scheduler",
    "shared_utils",
    'corsheaders',
]

# Middleware
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # for CORS support
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # for static file serving
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# URL & WSGI
ROOT_URLCONF = "backend_core.urls"
WSGI_APPLICATION = "backend_core.wsgi.application"

# Media & Static files

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / '..' / 'frontend' / 'dist',
    BASE_DIR / 'backend_core' / 'Static',
]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Configure WhiteNoise for static files
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

# Add MIME type configuration
WHITENOISE_MIMETYPES = {
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.ico': 'image/x-icon',
    '.woff': 'application/font-woff',
    '.woff2': 'application/font-woff2',
    '.ttf': 'application/font-ttf',
    '.eot': 'application/vnd.ms-fontobject',
    '.otf': 'application/font-otf',
}

# WhiteNoise configuration
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = True
WHITENOISE_ROOT = STATIC_ROOT

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'backend_core/Media'

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, '../frontend/dist'),
            os.path.join(BASE_DIR, 'backend_core/Templates'),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# DATABASE 
if IS_TESTING:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "test_db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": dj_database_url.config(
            default=f"postgres://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}"
        )
    }

# Testrunner
if IS_TESTING:
    TEST_RUNNER = "pytest_django.runner.DiscoverRunner"

# Password validators
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ───────────────────────────────────────────────────────────────
# Logging Setup (creates Logs/log.txt automatically if not exists)
# ───────────────────────────────────────────────────────────────

LOG_DIR = BASE_DIR / "Logs"
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] [{levelname}] [{name}:{lineno}] {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(LOG_DIR / 'log.txt'),
            'formatter': 'verbose',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'delay': True,  # Delay file creation until first write
        },
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'stream': sys.stdout,
        },
        'null': {
            'class': 'logging.NullHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file', 'console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
}

# Suppress 404/403/400 warnings during tests and development
if 'test' in sys.argv[0] or 'pytest' in sys.argv[0]:
    # During tests, use only console handler
    LOGGING['loggers']['django.request']['handlers'] = ['console']
    LOGGING['loggers']['django.request']['level'] = 'CRITICAL'
    # Disable file logging during tests by removing the file handler
    if 'file' in LOGGING['handlers']:
        del LOGGING['handlers']['file']

