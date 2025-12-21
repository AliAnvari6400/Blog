from django.shortcuts import render,redirect,reverse
from .models import Post
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
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
    template_name = 'blog/blog-home2.html'
    context_object_name = "posts"
    paginate_by = 2

    def get_queryset(self):
        queryset = Post.objects.filter(
            published_date__lte=timezone.now(),
            status=True
        )

        cat_name = self.kwargs.get('cat_name')
        author = self.kwargs.get('author')
        tag_name = self.kwargs.get('tag_name')
        s = self.request.GET.get('s')

        if tag_name:
            queryset = queryset.filter(tags__name=tag_name)
        if cat_name:
            queryset = queryset.filter(category__name=cat_name)
        if author:
            queryset = queryset.filter(author__username=author)
        if s:
            queryset = queryset.filter(content__contains=s)

        return queryset
    

class BlogSingleView(MyLoginRequiredMixin,DetailView):
    model = Post
    template_name = 'blog/blog-single2.html'
    context_object_name = 'post'
    pk_url_kwarg = 'pid'

    def get_queryset(self):
        return Post.objects.filter(
            status=True,
            published_date__lte=timezone.now()
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object

        # Next post (newer)
        post_after = Post.objects.filter(
            status=True,
            published_date__lte=timezone.now(),
            published_date__gt=post.published_date
        ).order_by('published_date').first()

        # Previous post (older)
        post_pre = Post.objects.filter(
            status=True,
            published_date__lte=timezone.now(),
            published_date__lt=post.published_date
        ).order_by('-published_date').first()

        context.update({
            'post_after': post_after,
            'post_pre': post_pre,
            'after': post_after is not None,
            'pre': post_pre is not None,
        })

        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Count views safely
        Post.objects.filter(pk=self.object.pk).update(
            counted_views=F('counted_views') + 1
        )
        self.object.refresh_from_db()

        return super().get(request, *args, **kwargs)



# Create your views here.
# def page_management(request,posts):
#     posts = Paginator(posts,2)
#     totalpages = posts.page_range
#     try:
#         page_num = request.GET.get('page')
#         posts = posts.get_page(page_num)
#     except PageNotAnInteger:
#         posts = posts.get_page(1)
#     except EmptyPage:
#         posts = posts.get_page(1)
#     return posts,totalpages

# def blog_home_view(request,cat_name = None,author = None,tag_name = None):
#     posts = Post.objects.filter(published_date__lte = timezone.now(), status = True)
#     s_flag = False
#     if tag_name:
#         posts = posts.filter(tags__name = tag_name) 
#     if cat_name:
#         posts = posts.filter(category__name = cat_name) 
#     if author:
#         posts = posts.filter(author__username = author)
#     if s:= request.GET.get('s'):
#         posts = posts.filter(content__contains = s) 
#         s_flag = True  
#     posts,totalpages = page_management(request,posts)
#     context = {'posts':posts,'totalpages':totalpages,'s_flag':s_flag ,'s':s}
#     return render(request,'blog/blog-home2.html',context)


# def blog_single_view(request,pid):
#     all_active_posts = Post.objects.filter(status = True, published_date__lte = timezone.now())
#     l = len(all_active_posts)
#     post_index = -1
#     for i in range(l):
#         if pid == all_active_posts[i].id:
#             post_index = i   

#     if post_index < l-1 and post_index > 0:
#         after = True
#         pre = True   
#     elif post_index == l-1 and post_index > 0:
#         after = False
#         pre = True  
#     elif post_index == 0 and post_index < l-1:
#         after = True 
#         pre = False
#     else:
#         after = False
#         pre = False 
        
#     if after == True:
#         post_after = all_active_posts[post_index + 1]   
#     else: 
#         post_after = None   
#     if pre == True: 
#         post_pre = all_active_posts[post_index - 1]
#     else: 
#         post_pre = None
    
#     post = get_object_or_404(Post,id = pid,status = True, published_date__lte = timezone.now())
#     post.counted_views += 1
#     post.save()
    
#     context = {'post':post,'after':after,'pre':pre,'post_after':post_after,'post_pre':post_pre}
    
#     if request.user.is_authenticated:
#         return render(request,'blog/blog-single2.html',context)
#     else:
#         if post.login_require == False:
#             return render(request,'blog/blog-single2.html',context)
#         else:
#             return redirect('/accounts/login/')

