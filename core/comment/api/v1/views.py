from .serializers import TaskSerializer, WeatherSerializer
from ...models import Task
from blog.models import Post
from accounts.models import Profile
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend
from .paginations import DefaultPagination
from rest_framework.views import APIView
import requests
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.cache import cache


class TaskModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    # , IsOwnerOrReadOnly]
    serializer_class = TaskSerializer
    # queryset = Task.objects.all()

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["author", "status"]
    search_fields = ["title"]
    ordering_fields = ["published_date"]

    pagination_class = DefaultPagination

    def get_queryset(self):
        pid = self.kwargs["pid"]
        user = self.request.user
        if not user or not user.is_authenticated:
            return Task.objects.none()  # Avoid 500
        return Task.objects.filter(author__user=user, post__id=pid)

    def perform_create(self, serializer):
        post_id = self.kwargs["pid"]
        post = get_object_or_404(Post, id=post_id)
        profile = Profile.objects.get(
            user=self.request.user
        )  # Fetch profile explicitly
        serializer.save(post=post, author=profile)


# Weather API:
# @method_decorator(cache_page(10,key_prefix='weather'), name='dispatch')
class WeatherAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = WeatherSerializer

    def get(self, request):
        API_KEY = "6075f690e844e83ffc96d4ddf40c8b18"
        city = "Tehran"
        cache_key = "weather"
        cached_data = cache.get(cache_key)

        if cached_data is None:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                cache.set(cache_key, data, timeout=60 * 20)  # cache 20 minutes
                cached_data = data
            else:
                return Response(
                    {"error": "Failed to fetch weather data"},
                    status=response.status_code,
                )

        serializer = WeatherSerializer(cached_data)
        return Response(serializer.data)
