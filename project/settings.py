"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path
from configurations import Configuration
from configurations import values
import dj_database_url

class Dev(Configuration):
    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent


    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = values.BooleanValue(True)
    # security.W016
    CSRF_COOKIE_SECURE = True

    # security.W012
    SESSION_COOKIE_SECURE = True

    
    ALLOWED_HOSTS = values.ListValue(['*'])

    AUTH_USER_MODEL = "customers_auth.Customer"

    # django-registration
    ACCOUNT_ACTIVATION_DAYS = 7
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

    # Application definition

    INSTALLED_APPS = [
        "customers_auth",
        "store",
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "payments",
        "crispy_forms",
        "crispy_bootstrap5",
        "phonenumber_field",
        
    ]

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "whitenoise.middleware.WhiteNoiseMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    ROOT_URLCONF = "project.urls"

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [BASE_DIR / "templates"],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.template.context_processors.media",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ]

    WSGI_APPLICATION = "project.wsgi.application"
    # Database
    # https://docs.djangoproject.com/en/4.0/ref/settings/#databases
    # user = os.environ.get('db_user')
    # password = os.environ.get('db_password')
    # host = os.environ.get('db_hostname')
    # port = os.environ.get('db_port')
    # dbname = os.environ.get('db_name')
    db_internal_url = os.environ.get('db_internal_url')
    DATABASES = {
       
        "default":
        dj_database_url.config(
            default=f"{db_internal_url}",
            conn_max_age=600),
    }


    # Password validation
    # https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
        },
    ]


    # Internationalization
    # https://docs.djangoproject.com/en/4.0/topics/i18n/

    LANGUAGE_CODE = "en-us"

    TIME_ZONE = values.Value('UTC')

    USE_I18N = True

    USE_TZ = True


    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/4.0/howto/static-files/


    STATIC_URL = 'static/'
    STATIC_ROOT = BASE_DIR/"static/"
    MEDIA_ROOT = BASE_DIR/"media"
    MEDIA_URL = "media/"
    # https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
    STATICFILES_FINDERS = [
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    ]

    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
    # Default primary key field type
    # https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

class Prod(Dev):
    DEBUG = False
    SECRET_KEY = values.SecretValue()
    # security.W008
    SECURE_SSL_REDIRECT = True
    ALLOWED_HOSTS = []
    RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
    if RENDER_EXTERNAL_HOSTNAME:
        ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)