# myproject/__init__.py
from apptransa.celery import app as celery_app

__all__ = ['celery_app']
