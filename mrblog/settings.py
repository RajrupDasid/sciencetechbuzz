from pathlib import Path
import os
from decouple import config
from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')
DEBUG = True if config('DEBUG') == "True" else False

PRODUCTION = True if config('PRODUCTION') == "True" else False
IS_REDIS = True if config('IS_REDIS') == "True" else False
IS_MEMCACHED = True if config('IS_MEMCACHED') == "True" else False
AUTH_USER_MODEL = 'accounts.User'
# SECURITY WARNING: don't run with debug turned on in production!

if PRODUCTION:
    maindomain = config('MAIN_DOMAIN')
    CSRF_TRUSTED_ORIGINS = [
        f"{maindomain}"
    ]

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'accounts.apps.AccountsConfig',
    'app.apps.AppConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sitemaps',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gallery.apps.GalleryConfig',
    'taggit',
    'storages',
    'tinymce',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# CACHE_MIDDLEWARE_ALIAS="default"
# CACHE_MIDDLEWARE_SECONDS=6
# CACHE_MIDDLEWARE_KEY_PREFIX="default"

ROOT_URLCONF = 'mrblog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'mrblog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
if PRODUCTION:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DATABASE_NAME'),
            'HOST': config('PGHOST'),
            'USER': config('DBUSERNAME'),
            'PASSWORD': config('DBPASSWORD'),
            'PORT': config('PGPORT'),
            'OPTIONS': {'sslmode': 'require'},

        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/staticdir/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticdir')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

TINYMCE_DEFAULT_CONFIG = {
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'theme': 'silver',
    'plugins': '''
            textcolor save link image media preview codesample contextmenu
            table code lists fullscreen  insertdatetime  nonbreaking
            contextmenu directionality searchreplace wordcount visualblocks
            visualchars code fullscreen autolink lists  charmap print  hr
            anchor pagebreak
            ''',
    'toolbar1': '''
            fullscreen preview bold italic underline | fontselect,
            fontsizeselect  | forecolor backcolor | alignleft alignright |
            aligncenter alignjustify | indent outdent | bullist numlist table |
            | link image media | codesample |
            ''',
    'toolbar2': '''
            visualblocks visualchars |
            charmap hr pagebreak nonbreaking anchor |  code |
            ''',
    'contextmenu': 'formats | link image',
    'menubar': True,
    'statusbar': True,
}


MESSAGE_TAGS = {
    messages.ERROR: 'danger',
    messages.SUCCESS: 'success'
}


if PRODUCTION:
    AZURE_QUERYSTRING_AUTH = False
    DEFAULT_FILE_STORAGE = 'mrblog.azure_storage.AzureMediaStorage'
    STATICFILES_STORAGE = 'mrblog.azure_storage.AzureStaticStorage'
    AZURE_CUSTOM_DOMAIN = config('AZURE_CUSTOM_DOMAIN')
    AZURE_ACCOUNT_NAME = config('AZURE_ACCOUNT_NAME')
    AZURE_ACCOUNT_KEY = config('AZURE_ACCOUNT_KEY')
    AWS_QUERYSTRING_AUTH = False
    AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'
    STATIC_URL = f'https://{AZURE_CUSTOM_DOMAIN}/static/'
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    MEDIA_URL = f'https://{AZURE_CUSTOM_DOMAIN}/media/'
    MEDIA_ROOT = BASE_DIR / 'mediafiles'
