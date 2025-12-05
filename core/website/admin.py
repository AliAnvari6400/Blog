from django.contrib import admin
from website.models import Contact, Newsletter

# Register your models here.
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name','email','subject')
    
admin.site.register(Contact,ContactAdmin)

class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('EMAIL',)
    
admin.site.register(Newsletter,NewsletterAdmin)