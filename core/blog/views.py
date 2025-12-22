from .models import Post
from django.utils import timezone
from django.views.generic import DetailView
from django.db.models import F
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)


# customize LoginRequiredMixin for redirect to login page first
class MyLoginRequiredMixin(LoginRequiredMixin):
    def get_login_url(self):
        return reverse_lazy("accounts:login")


class BlogHomeView(MyLoginRequiredMixin, ListView):
    model = Post
    template_name = "blog/blog-home2.html"
    context_object_name = "posts"
    paginate_by = 2

    def get_queryset(self):
        queryset = Post.objects.filter(published_date__lte=timezone.now(), status=True)

        cat_name = self.kwargs.get("cat_name")
        author = self.kwargs.get("author")
        tag_name = self.kwargs.get("tag_name")
        s = self.request.GET.get("s")

        if tag_name:
            queryset = queryset.filter(tags__name=tag_name)
        if cat_name:
            queryset = queryset.filter(category__name=cat_name)
        if author:
            queryset = queryset.filter(author__username=author)
        if s:
            queryset = queryset.filter(content__contains=s)

        return queryset


class BlogSingleView(MyLoginRequiredMixin, DetailView):
    model = Post
    template_name = "blog/blog-single2.html"
    context_object_name = "post"
    pk_url_kwarg = "pid"

    def get_queryset(self):
        return Post.objects.filter(status=True, published_date__lte=timezone.now())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object

        # Next post (newer)
        post_after = (
            Post.objects.filter(
                status=True,
                published_date__lte=timezone.now(),
                published_date__gt=post.published_date,
            )
            .order_by("published_date")
            .first()
        )

        # Previous post (older)
        post_pre = (
            Post.objects.filter(
                status=True,
                published_date__lte=timezone.now(),
                published_date__lt=post.published_date,
            )
            .order_by("-published_date")
            .first()
        )

        context.update(
            {
                "post_after": post_after,
                "post_pre": post_pre,
                "after": post_after is not None,
                "pre": post_pre is not None,
            }
        )

        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Count views safely
        Post.objects.filter(pk=self.object.pk).update(
            counted_views=F("counted_views") + 1
        )
        self.object.refresh_from_db()

        return super().get(request, *args, **kwargs)
