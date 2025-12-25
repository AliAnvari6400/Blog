from django.urls import path, include
from .views import (
    PostEditView,
    PostDeleteView,
    PostCompleteView,
    PostView,
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
]

