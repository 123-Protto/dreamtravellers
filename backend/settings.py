"""
Django settings for backend project.
Generated for Render deployment.
"""

from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

# ----------------------------------------------------
# BASE DIR
# ----------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env locally (Render uses environment variables you set in dashboard)
load_dotenv(os.path.join(BASE_DIR, ".env"))

# ----------------------------------------------------
# SECURITY
# ----------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "local-dev-secret-key")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Add your Render domain and localhost
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    ".onrender.com",
]

# ----------------------------------------------------
# INSTALLED APPS
# ----------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party
    'corsheaders',
    'rest_framework',

    # Local apps
    'enquiries',
]

# ----------------------------------------------------
# MIDDLEWARE
# ----------------------------------------------------
MIDDLEWARE = [
    # CORS FIRST
    'corsheaders.middleware.CorsMiddleware',

    # Security
    'django.middleware.security.SecurityMiddleware',

    # Whitenoise AFTER SecurityMiddleware
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ----------------------------------------------------
# URLS & WSGI
# ----------------------------------------------------
ROOT_URLCONF = 'backend.urls'
WSGI_APPLICATION = 'backend.wsgi.application'

# ----------------------------------------------------
# TEMPLATES
# ----------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "backend" / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ----------------------------------------------------
# DATABASE (Render Auto Config)
# ----------------------------------------------------
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}

# ----------------------------------------------------
# STATIC FILES (Render FIXED)
# ----------------------------------------------------
STATIC_URL = "/static/"

# Collectstatic output
STATIC_ROOT = BASE_DIR / "staticfiles"

# Static folder used in development
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ----------------------------------------------------
# CORS
# ----------------------------------------------------
CORS_ALLOW_ALL_ORIGINS = True

# ----------------------------------------------------
# DEFAULT FIELD TYPE
# ----------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ----------------------------------------------------
# API KEYS
# ----------------------------------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
