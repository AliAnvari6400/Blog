from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)
from .forms import ProfileForm
from .models import Profile

User = get_user_model()


# custom UserCreateForm for email as username
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email",)  # Only include email field


# Profile:
class ProfileView(UpdateView, LoginRequiredMixin):
    model = Profile
    form_class = ProfileForm
    template_name = "registration/profile.html"
    success_url = reverse_lazy(
        "website:index"
    )  # Redirect to website page after complete profile

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Profile.objects.filter(user__id=pk)


# Signup
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("accounts:login")  # Redirect to login page after signup


class MyLoginView(LoginView):
    redirect_authenticated_user = True

    def get_success_url(self):
        next_url = self.get_redirect_url()
        print(next_url)
        if next_url:
            return next_url
        return reverse_lazy("blog:blog_home")
