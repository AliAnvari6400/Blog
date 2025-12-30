from django.urls import path, include
from django.contrib.auth.views import LogoutView
from .views import SignUpView
from django.views.generic import RedirectView
from .views import MyLoginView
from blog.views import BlogHomeView

app_name = "accounts"

urlpatterns = [
    #path("", RedirectView.as_view(url="blog/", query_string=True, permanent=False)),
    path("", BlogHomeView.as_view()),
    # path('',include('django.contrib.auth.urls')),
    path("login/", MyLoginView.as_view(), name="login"),
    path(
        "logout/",
        LogoutView.as_view(next_page="/accounts/login/"),
        name="logout",
    ),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("api/v1/", include("accounts.api.v1.urls")),
]
