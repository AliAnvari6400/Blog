from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from blog.models import Post,Category


# Register your models here.

class PostAdmin(SummernoteModelAdmin):
    list_display = ('id','title','counted_views','status','login_require','published_date','author')
    search_fields = ['title','content']
    summernote_fields = ('content',)
    
admin.site.register(Post,PostAdmin)
admin.site.register(Category)
#admin.site.register(Comment)

