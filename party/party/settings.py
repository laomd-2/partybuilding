"""
Django settings for party project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z2t6bzn=_805^)wl=h5aa2w7ss=e9)yg#ak^3efjm(1g%t!83&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', ]
INTERNAL_IPS = [
    '127.0.0.1',
]
# Application definition

INSTALLED_APPS = [
    'user.apps.UserConfig',
    'info.apps.InfoConfig',
    'teaching.apps.TeachingConfig',
    'work.apps.NoteConfig',
    'import_export',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'xadmin',
    'crispy_forms',
    'DjangoUeditor',
    'rules',
]

if DEBUG:
    INSTALLED_APPS += [
        'template_timings_panel',
        'debug_toolbar'
    ]

AUTHENTICATION_BACKENDS = (
    'rules.permissions.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware', ] + MIDDLEWARE

ROOT_URLCONF = 'party.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'party.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'party',
        'USER': 'sdcs_party',
        'PASSWORD': 'SDCS2019@party',
    },
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'party',
    #     'USER': 'root',
    #     'PASSWORD': 'laomadong',
    # },
    # 'slave': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'HOST': '47.112.202.35',
    #     'NAME': 'party',
    #     'USER': 'sdcscs2',
    #     'PASSWORD': '000000',
    # }
}

# DATABASE_ROUTERS = ['party.router.Router']

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
AUTH_USER_MODEL = 'user.User'

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'upload')
MEDIA_URL = '/media/'  # 这个是在浏览器上访问该上传文件的url的前缀

EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.exmail.qq.com'  # 如果是 163 改成 smtp.163.com
EMAIL_PORT = 465
EMAIL_HOST_USER = '*@mail2.*.edu.cn'  # 帐号
EMAIL_HOST_PASSWORD = 'Laomadong7113'  # 密码
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

HOST_IP = '*.*.*.*:8000'

DEBUG_TOOLBAR_CONFIG = {
    "JQUERY_URL": '//cdn.bootcss.com/jquery/2.2.4/jquery.min.js',
}

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'template_timings_panel.panels.TemplateTimings.TemplateTimings',
]
