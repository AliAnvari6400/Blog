from django.urls import path, include
from .views import (
    PostEditView,
    PostDeleteView,
    PostCompleteView,
    PostView,
    test,
    weather,
    WeatherView,
)

app_name = "post"

urlpatterns = [
    path("", PostView.as_view(), name="post"),
    path("<int:pk>/edit/", PostEditView.as_view(), name="post-edit"),
    path("<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path(
        "<int:pk>/complete/",
        PostCompleteView.as_view(),
        name="post-complete",
    ),
    path("api/v1/", include("post.api.v1.urls")),
    # Test Celery:
    path("test/", test, name="test"),
    # Test Redis for cache:
    path("weather/", weather, name="weather"),
    # Show graphical weather data:
    path("weather_show/", WeatherView.as_view(), name="weather_show"),
]
