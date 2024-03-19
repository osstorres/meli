from django.urls import path

from .views import HealthCheckApiView

urlpatterns = [
    path("health-check/", HealthCheckApiView.as_view()),
]
