"""
Django settings for dmtry1 project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ak=+bsvp@vlq2umr3*0wi(#ih)3mc9&6cy1cu@(go6s=6n5!+4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['kd1.tustcs.com', '114.116.68.121','localhost', '0.0.0.0:8000','127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dm_demo',   # 新创建的
    'djangosecure',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dmtry1.urls'


MIDDLEWARE_CLASSES = [
    'djangosecure.middleware.SecurityMiddleware',
]


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
                "django.template.context_processors.media",
            ],
        },
    },
]

LOGIN_URL = '/login/'
# LOGIN_REDIRECT_URL='/server/'

WSGI_APPLICATION = 'dmtry1.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        "ENGINE": "django.db.backends.mysql",
        "NAME": "dmtry",  # 需要自己手动创建数据库
        "USER": "root",
        "PASSWORD": "zsjnb",
        "HOST": "127.0.0.1",
        "PORT": 3306
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/templates/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "templates"),
)

# 自动发送认证邮件
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = False   #是否使用TLS安全传输协议(用于在两个通信应用程序之间提供保密性和数据完整性。)
EMAIL_USE_SSL = True    #是否使用SSL加密，qq企业邮箱要求使用
EMAIL_HOST = 'smtp.163.com'   #发送邮件的邮箱 的 SMTP服务器，这里用了163邮箱
EMAIL_PORT = 465     #发件箱的SMTP服务器端口
EMAIL_HOST_USER = 'achievement_manage@163.com'    #发送邮件的邮箱地址
EMAIL_HOST_PASSWORD = 'AWTJMGTNWJPMJVKO'         #发送邮件的邮箱密码(这里使用的是授权码)


PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    # 'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    # 'django.contrib.auth.hashers.Argon2PasswordHasher',
    # 'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    # 'django.contrib.auth.hashers.BCryptPasswordHasher',

]

AUTH_USER_MODEL = 'dm_demo.admin_tab'
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.AllowAllUsersModelBackend']


SECURE_SSL_REDIRECT = True    #将所有非SSL请求永久重定向到SSL
SECURE_HSTS_SECONDS = 2
SECURE_HSTS_INCLUDE_SUBDOMAINS = True   #使用[HTTP严格传输安全]
SECURE_FRAME_DENY = True   #避免让自己的网页的框架和保护他们免受[点击劫持]
SECURE_CONTENT_TYPE_NOSNIFF = True   #防止浏览器猜测资产的内容类型
SECURE_BROWSER_XSS_FILTER = True  #启用浏览器的XSS过滤保护
SESSION_COOKIE_SECURE = True 
SESSION_COOKIE_HTTPONLY = True #防止COOKIE窃听，使客户端到服务端总是COOKIE加密传输
