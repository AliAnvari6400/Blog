from django.urls import path
from .views import maintenance_view

app_name = "config"

urlpatterns = [
    path("", maintenance_view, name="maintenance"),
]
