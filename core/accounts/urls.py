from django.urls import path, include
from .views import SignUpView, ProfileView
from django.views.generic import RedirectView
from .views import MyLoginView, swagger_logout_view
from django.contrib.auth.views import LogoutView

app_name = "accounts"

urlpatterns = [
    path("", RedirectView.as_view(url="blog/", query_string=True, permanent=False)),
    # path('',include('django.contrib.auth.urls')),
    path("login/", MyLoginView.as_view(), name="login"),
    path(
        "logout/",
        LogoutView.as_view(next_page="/accounts/login/"),
        name="logout",
        kwargs={"swagger_schema": None},
    ),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("<int:pk>/profile/", ProfileView.as_view(), name="profile"),
    path("api/v1/", include("accounts.api.v1.urls")),
    # Swagger-only URL (appears in Swagger UI)
    path("swagger-logout/", swagger_logout_view, name="swagger-logout"),
]
