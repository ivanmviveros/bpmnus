"""
Django settings for bpmnus project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import datetime, platform
from pathlib import Path
from django.contrib.staticfiles import handlers
# Build paths inside the project like this: BASE_DIR / 'subdir'.



BASE_DIR = Path(__file__).resolve().parent.parent

ALLOWED_HOSTS = ['bpmnus', 'localhost', '127.0.0.1']
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 't&ay-r4k5+lm)ocb9y8xmp6t%8m-lq8pc65v428ie7dft_(+q*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework.authtoken',
    'rest_framework',
    'corsheaders',
    'projects',
    'diagrams',
    'usersapi',
    'dj_rest_auth',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware'
]

ROOT_URLCONF = 'bpmnus.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'bpmnus.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'bpmnus',
        'USER': 'bpmnus',
        'PASSWORD': 'bpmnus',
        'HOST': 'localhost',
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

REST_SESSION_LOGIN = True
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
SITE_ID = 1
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'optional'

REST_USE_JWT = True
JWT_AUTH_COOKIE = 'auth'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=7),
}

REST_FRAMEWORK = { 
    'DEFAULT_AUTHENTICATION_CLASSES': [ 
        'rest_framework.authentication.TokenAuthentication',
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': [  
        'rest_framework.permissions.IsAuthenticated'  
    ]
}


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
if platform.system() == 'Windows':
    STATIC_ROOT = 'C:\\Users\\Public\\Documents'  
else: 
    STATIC_ROOT = '/opt/app/static'

REST_FRAMEWORK = {
    'DATETIME_FORMAT': "%Y-%m-%d",
}

CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:3000',
    'http://localhost:3000',
    'https://127.0.0.1:3000',
    'https://localhost:3000',
    'http://localhost:80',
    'http://127.0.0.1:80',
    'http://localhost',
    'http://127.0.0.1',
)

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'https://127.0.0.1:3000',
    'https://localhost:3000',
    'http://localhost:80',
    'http://127.0.0.1:80',
    'http://localhost',
    'http://127.0.0.1',
]


class CORSStaticFilesHandler(handlers.StaticFilesHandler):
    def serve(self, request):
        response = super().serve(request)
        try:
            if request.headers['Origin'] in CORS_ALLOWED_ORIGINS:
                response['Access-Control-Allow-Origin'] = '*'
        except KeyError:
            pass
        return response

handlers.StaticFilesHandler = CORSStaticFilesHandler
