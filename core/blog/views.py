from django.shortcuts import render,redirect,reverse
from blog.models import Post,Comment
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from blog.forms import CommentForm
from django.contrib import messages
from django.http import HttpResponseRedirect


# Create your views here.
def page_management(request,posts):
    posts = Paginator(posts,2)
    totalpages = posts.page_range
    try:
        page_num = request.GET.get('page')
        posts = posts.get_page(page_num)
    except PageNotAnInteger:
        posts = posts.get_page(1)
    except EmptyPage:
        posts = posts.get_page(1)
    return posts,totalpages

def blog_home_view(request,cat_name = None,author = None,tag_name = None):
    posts = Post.objects.filter(published_date__lte = timezone.now(), status = True)
    s_flag = False
    if tag_name:
        posts = posts.filter(tags__name = tag_name) 
    if cat_name:
        posts = posts.filter(category__name = cat_name) 
    if author:
        posts = posts.filter(author__username = author)
    if s:= request.GET.get('s'):
        posts = posts.filter(content__contains = s) 
        s_flag = True  
    posts,totalpages = page_management(request,posts)
    context = {'posts':posts,'totalpages':totalpages,'s_flag':s_flag ,'s':s}
    return render(request,'blog/blog-home2.html',context)


def blog_single_view(request,pid):
    all_active_posts = Post.objects.filter(status = True, published_date__lte = timezone.now())
    l = len(all_active_posts)
    post_index = -1
    for i in range(l):
        if pid == all_active_posts[i].id:
            post_index = i   

    if post_index < l-1 and post_index > 0:
        after = True
        pre = True   
    elif post_index == l-1 and post_index > 0:
        after = False
        pre = True  
    elif post_index == 0 and post_index < l-1:
        after = True 
        pre = False
    else:
        after = False
        pre = False 
        
    if after == True:
        post_after = all_active_posts[post_index + 1]   
    else: 
        post_after = None   
    if pre == True: 
        post_pre = all_active_posts[post_index - 1]
    else: 
        post_pre = None
    
    post = get_object_or_404(Post,id = pid,status = True, published_date__lte = timezone.now())
    post.counted_views += 1
    post.save()
    
    # comment form:
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,"ok")  
        else: 
            messages.add_message(request,messages.ERROR,"error")
        return redirect(request.path)
        #return HttpResponseRedirect('')   
    form = CommentForm()
    
    # comments show:
    comments = Comment.objects.filter(post = post.id, approved = True)
    
    context = {'post':post,'after':after,'pre':pre,'post_after':post_after,'post_pre':post_pre,
               'form':form,'comments':comments}
    
    if request.user.is_authenticated:
        return render(request,'blog/blog-single2.html',context)
    else:
        if post.login_require == False:
            return render(request,'blog/blog-single2.html',context)
        else:
            return redirect('/accounts/login/')
