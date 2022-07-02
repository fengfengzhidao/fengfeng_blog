"""
Django settings for Fengfengblog project.

Generated by 'django-admin startproject' using Django 3.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-hy&u3h8i&3#a9y4qvz*^80zak#l-3t1=+%k)hz9u3)#i2dcnu5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app01.apps.App01Config',
    'api.apps.ApiConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'app01.middleware_decode.Md1',
    'app01.middleware_decode.Statistical',
]

ROOT_URLCONF = 'Fengfengblog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
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

WSGI_APPLICATION = 'Fengfengblog.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fengfeng_blog',
        'USER': 'fengfeng_blog',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': 3306
    }
}
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake'
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = (
    'app01.valid.auth.CustomBackend',
)

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

# LANGUAGE_CODE = 'en-us'
#
# TIME_ZONE = 'UTC'

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
# 收集项目的静态文件
STATIC_ROOT = os.path.join(BASE_DIR, 'feng_static')

# 用户自己上传文件
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# 请求最大
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 默认设置为5M

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 用户扩展第三张表
# 自己创建第三张表
AUTH_USER_MODEL = "app01.UserInfo"

#######  simepui  ####

SIMPLEUI_HOME_INFO = False  # 关闭服务器信息
SIMPLEUI_HOME_QUICK = False  # 关闭快捷操作
SIMPLEUI_HOME_ACTION = False  # 关闭最近动作

SIMPLEUI_HOME_PAGE = '/admin_home/'
SIMPLEUI_HOME_TITLE = '首页'
SIMPLEUI_HOME_ICON = 'fa fa-user'

# 发送邮箱配置
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = '你的邮箱'
EMAIL_HOST_PASSWORD = '你的密码'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_USE_SSL = True
EMAIL_USER_TLS = False

# 七牛云配置
QINIU_ACCESS_KEY = '七牛云AK'
QINIU_SECRET_KEY = '七牛云SK'
QINIU_BUCKET_NAME = '七牛云存储空间'
QINIU_DOMAIN = 'xxx.xxx.xxx'  # 访问的域名，按照这样的格式

# QQ登录
QQ_APPID = '你的QQ appid'
QQ_KEY = '你的QQ_KEY'
QQ_REDIRECT = 'QQ登录之后的回调地址'

# gitee登录
GITEE_ID = 'GiteeID'
GITEE_SECRET = 'GiteeSECRET'
GITEE_REDIRECT = 'gitee登录之后的回调地址'

# 网站版本从这里获取
VERSION = '5.0.2'

try:
    from .local_settings import *
except:
    pass
