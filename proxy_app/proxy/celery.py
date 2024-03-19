import os

from django.conf import settings

from celery import Celery
from configurations import importer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proxy.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Dev")
os.environ.setdefault("SECRET_KEY", "proxy-iT859jujylqCR4mXOCUhd2N1d4gBat")
importer.install()

app = Celery("proxy")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
