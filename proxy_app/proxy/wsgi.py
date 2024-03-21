"""
WSGI config for proxy project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
import newrelic.agent


newrelic.agent.initialize(
    os.path.join(os.path.dirname(__file__), "newrelic.ini"),
    environment="production",
)
settings_new_relic = newrelic.agent.global_settings()
settings_new_relic.license_key = os.getenv("NEW_RELIC_LICENSE_KEY")

newrelic.agent.register_application()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proxy.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Production")
application = get_wsgi_application()
