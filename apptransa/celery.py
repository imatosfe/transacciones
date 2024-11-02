import os
from celery import Celery

# Configura el módulo de configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apptransa.settings')

app = Celery('apptransa')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
