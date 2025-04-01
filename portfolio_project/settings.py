import os
from pathlib import Path
from dotenv.main import load_dotenv
from datetime import timedelta

DEBUG = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}


SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "change_me")

POLYGON_API_KEY = os.environ.get('POLYGON_API_KEY', '')

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',
        },
    },
}

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "channels",
    'portfolio_api',
    "rag_pipeline",
    'rest_framework_nested',
    'django_extensions',
    'market_data'

]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "portfolio_project.urls"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "portfolio_project.wsgi.application"
ASGI_APPLICATION = "portfolio_project.asgi.application"

STATIC_URL = "/static/"

# load_dotenv(os.path.join(BASE_DIR, ".env"))

BASE_DIR = Path('/Users/qiqi/Desktop/ai-investment-advisor/').resolve()
load_dotenv(os.path.join(BASE_DIR, ".env"))
print(f'{BASE_DIR}')
MONGO_DB_NAME = "ai_investment_db"
MONGO_DB_COLLECTION = "vector_search_collection_new"
MONGO_ATLAS_VECTOR_INDEX_NAME = "vector_index"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MONGO_URI = os.getenv("MONGO_URI")
print(f'MONGO_URI: {MONGO_URI}')
DJANGO_SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
OPEN_AI_MODEL = "gpt-4-turbo"


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ai_investment_advisor',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost', # os.getenv
        'PORT': '5432',
    }
}


KAFKA_BROKER_URL = "localhost:9092"
KAFKA_TOPIC = "ai-investment-advisor"

# 在 settings.py 的末尾添加
# Celery 设置
CELERY_BROKER_URL = 'filesystem://'
CELERY_BROKER_TRANSPORT_OPTIONS = {
    'data_folder_in': 'celery_data/in',
    'data_folder_out': 'celery_data/out',
}
CELERY_BEAT_SCHEDULE = {
    'update-market-data': {
        'task': 'market_data.tasks.update_market_data',
        'schedule': 3600,
    },
    'update-market-status': {
        'task': 'market_data.tasks.update_market_status',
        'schedule': 3600,  # 1 hour
    },
}

import os
for folder in (
    'celery_data/in',
    'celery_data/out'
):
    if not os.path.exists(folder):
        os.makedirs(folder)