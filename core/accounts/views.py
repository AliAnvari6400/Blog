from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)
from .forms import ProfileForm
from .models import Profile
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

User = get_user_model()


# custom UserCreateForm for email as username
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email",)  # Only include email field


# Profile:
class ProfileView(CreateView, LoginRequiredMixin):
    model = Profile
    form_class = ProfileForm
    template_name = "registration/profile.html"
    success_url = reverse_lazy(
        "website:index"
    )  # Redirect to website page after complete profile

    def form_valid(self, form):
        self.object = form.save()
        user = self.request.user
        content_type = ContentType.objects.get_for_model(Profile)
        view_permission = Permission.objects.get(
            codename="view_profile", content_type=content_type
        )
        user.user_permissions.add(view_permission)
        return super().form_valid(form)


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
