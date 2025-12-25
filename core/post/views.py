from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from blog.models import Post
from accounts.models import Profile
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.urls import reverse_lazy
from .forms import PostForm
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.urls import reverse


# customize LoginRequiredMixin for redirect to login page first
class MyLoginRequiredMixin(LoginRequiredMixin):
    def get_login_url(self):
        return reverse_lazy("accounts:login")


# Combined CreateView and ListView
class PostView(MyLoginRequiredMixin, CreateView, ListView):
    model = Post
    template_name = "post/post.html"
    context_object_name = "posts"
    paginate_by = 50
    form_class = PostForm

    def get_success_url(self):
        return reverse("post:post")

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(author__user=user).order_by("-created_date")

    def get_initial(self, **kwargs):
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            initial["author"] = Profile.objects.get(user=self.request.user)
        return initial

    def form_valid(self, form):
        self.object = form.save()
        user = self.request.user
        content_type = ContentType.objects.get_for_model(Post)
        view_permission = Permission.objects.get(
            codename="view_post", content_type=content_type
        )
        user.user_permissions.add(view_permission)
        return super().form_valid(form)


class PostEditView(MyLoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    permission_required = "blog.view_post"
    template_name = "post/post_form.html"
    form_class = PostForm

    def get_success_url(self):
        return reverse("post:post")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=Profile.objects.get(user=self.request.user))

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        try:
            obj = super().get_object(queryset)
        except Http404:
            # Instead of 404, raise 403 here
            raise PermissionDenied
        return obj


class PostDeleteView(MyLoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    permission_required = "blog.view_post"
    template_name = "post/post_confirm_delete.html"

    def get_success_url(self):
        return reverse("post:post")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=Profile.objects.get(user=self.request.user))

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        try:
            obj = super().get_object(queryset)
        except Http404:
            # Instead of 404, raise 403 here
            raise PermissionDenied
        return obj


class PostCompleteView(MyLoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    fields = ["status"]
    template_name = "post/post_complete.html"
    permission_required = "blog.view_post"

    def get_success_url(self):
        return reverse("post:post")

    def form_valid(self, form):
        instance = form.save(commit=False)
        if instance.status is False:
            instance.status = True
        else:
            instance.status = False
        instance.save()
        return super(PostCompleteView, self).form_valid(form)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=Profile.objects.get(user=self.request.user))

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        try:
            obj = super().get_object(queryset)
        except Http404:
            # Instead of 404, raise 403 here
            raise PermissionDenied
        return obj
