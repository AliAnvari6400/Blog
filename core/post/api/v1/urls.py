from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostModelViewSet, WeatherAPIView

app_name = "api-v1"

router = DefaultRouter()
router.register("post", PostModelViewSet, basename="post")

urlpatterns = [
    path("", include(router.urls)),
    path("weather/", WeatherAPIView.as_view(), name="weather"),
]
