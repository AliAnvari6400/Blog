from django.urls import path
from .views import BlogHomeView, BlogSingleView
from blog.feeds import LatestEntriesFeed

app_name = "blog"

urlpatterns = [
    path("", BlogHomeView.as_view(), name="blog_home"),
    path("category/<str:cat_name>/", BlogHomeView.as_view(), name="category"),
    path("author/<str:author>/", BlogHomeView.as_view(), name="author"),
    path("search/", BlogHomeView.as_view(), name="search"),
    path("tag/<str:tag_name>/", BlogHomeView.as_view(), name="tag"),
    path("<int:pid>", BlogSingleView.as_view(), name="blog_single"),
    path("rss/feed/", LatestEntriesFeed()),
]
