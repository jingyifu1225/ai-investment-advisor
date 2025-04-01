import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings')
celery_app = Celery('market_data')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')