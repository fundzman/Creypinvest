import os
from pathlib import Path
import django
import dj_database_url
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False") == "True"
USE_R2 = os.getenv("USE_R2", "False") == "True"

ALLOWED_HOSTS = ["*"]
LOGIN_URL = "/auth/account/login"
LOGIN_REDIRECT_URL = "/dashboard"

CSRF_COOKIE_SECURE = DEBUG == False
SESSION_COOKIE_SECURE = DEBUG == False
SECURE_SSL_REDIRECT = DEBUG == False
SECURE_HSTS_SECONDS = 518400 if (DEBUG == False) else None
SECURE_HSTS_INCLUDE_SUBDOMAINS = DEBUG == False
SECURE_HSTS_PRELOAD = DEBUG == False
SECURE_PROXY_SSL_HEADER = (
    ("HTTP_X_FORWARDED_PROTO", "https") if (DEBUG == False) else None
)

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "core",
    "users",
    "dashboard",
    "site_admin",
    "storages",
    "crispy_forms",
    "crispy_tailwind",
    "anymail",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.apple",
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"

CRISPY_TEMPLATE_PACK = "tailwind"
SITE_ID = 1
SOCIALACCOUNT_PROVIDERS = {
    "google": {"SCOPE": ["profile", "email"], "AUTH_PARAMS": {"access_type": "online"}}
}
ACCOUNT_FORMS = {"signup": "users.forms.CustomSignupForm"}
# Add the 'allauth' backend to AUTHENTICATION_BACKEND and keep default ModelBackend
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Custom allauth settings
# Use email as the primary identifier
ACCOUNT_AUTHENTICATION_METHOD = "username"
ACCOUNT_EMAIL_REQUIRED = True

# Make email verification mandatory to avoid junk email accounts
ACCOUNT_EMAIL_VERIFICATION = "mandatory"

# Eliminate need to provide username, as it's a very old practice
ACCOUNT_USERNAME_REQUIRED = True

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # "allauth.account.middleware.AccountMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# if DEBUG:
#     MIDDLEWARE += ["allauth.account.middleware.AccountMiddleware"]

ROOT_URLCONF = "creyp.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = "creyp.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES["default"].update(db_from_env)

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

if USE_R2:
    # Cloudflare R2 (S3-compatible API via django-storages)
    R2_ACCOUNT_ID = os.getenv("R2_ACCOUNT_ID")
    R2_ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID")
    R2_SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY")
    R2_BUCKET_NAME = os.getenv("R2_BUCKET_NAME")
    R2_REGION = os.getenv("R2_REGION", "auto")
    # Public custom domain connected to the R2 bucket
    R2_CDN_DOMAIN = os.getenv("R2_CDN_DOMAIN", "cdn.creypinvest.com")

    AWS_S3_ENDPOINT_URL = f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com"
    AWS_S3_REGION_NAME = R2_REGION
    AWS_S3_SIGNATURE_VERSION = "s3v4"
    AWS_S3_ADDRESSING_STYLE = "path"
    AWS_STORAGE_BUCKET_NAME = R2_BUCKET_NAME
    AWS_ACCESS_KEY_ID = R2_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = R2_SECRET_ACCESS_KEY
    AWS_DEFAULT_ACL = None  # R2 has no object ACLs; access is set on the bucket
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_CUSTOM_DOMAIN = R2_CDN_DOMAIN

    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"

    # Django 4.2+ replaced DEFAULT_FILE_STORAGE/STATICFILES_STORAGE with STORAGES
    # (and 5.1 ignores the old names); requirements_divine.txt is unpinned.
    if django.VERSION >= (4, 2):
        STORAGES = {
            "default": {"BACKEND": "creyp.storage_backends.R2MediaStorage"},
            "staticfiles": {"BACKEND": "creyp.storage_backends.R2StaticStorage"},
        }
    else:
        DEFAULT_FILE_STORAGE = "creyp.storage_backends.R2MediaStorage"
        STATICFILES_STORAGE = "creyp.storage_backends.R2StaticStorage"

else:
    STATIC_URL = "/static/"
    MEDIA_URL = "/media/"
    STATIC_ROOT = BASE_DIR / "static-root"
    MEDIA_ROOT = BASE_DIR / "media-root"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Email (Resend via Anymail)
EMAIL_BACKEND = "anymail.backends.resend.EmailBackend"
ANYMAIL = {
    "RESEND_API_KEY": os.getenv("RESEND_API_KEY"),
}

# Must be an address on a domain verified in Resend
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
