from django.urls import path, include
from .views import (
    TaskEditView,
    TaskDeleteView,
    TaskCompleteView,
    TaskView,
    test,
    weather,
    WeatherView,
)

app_name = "post"

urlpatterns = [
    path("", TaskView.as_view(), name="task"),
    path("<int:pk>/edit/", TaskEditView.as_view(), name="task-edit"),
    path("<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path(
        "<int:pk>/complete/",
        TaskCompleteView.as_view(),
        name="task-complete",
    ),
    path("api/v1/", include("post.api.v1.urls")),
    # Test Celery:
    path("test/", test, name="test"),
    # Test Redis for cache:
    path("weather/", weather, name="weather"),
    # Show graphical weather data:
    path("weather_show/", WeatherView.as_view(), name="weather_show"),
]
