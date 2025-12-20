from django.urls import path
from .views import blog_home_view,blog_single_view
from blog.feeds import LatestEntriesFeed

app_name = 'blog'

urlpatterns = [
    #path('',blog_home_view,name='blog_home'),
    
    path('',blog_home_view.as_view(),name='blog_home'),
    path('category/<str:cat_name>/',blog_home_view.as_view(), name='category'),
    path('author/<str:author>/',blog_home_view.as_view(), name='author'),
    path('search/',blog_home_view.as_view(),name='search'),
    path('tag/<str:tag_name>/',blog_home_view.as_view(),name='tag'),
    
    
    path('<int:pid>',blog_single_view,name='blog_single'),
    #path('category/<str:cat_name>/',blog_home_view, name='category'),
    #path('author/<str:author>/',blog_home_view, name='author'),
    #path('search/',blog_home_view,name='search'),
    #path('tag/<str:tag_name>/',blog_home_view,name='tag'),
    path("rss/feed/", LatestEntriesFeed()),

]