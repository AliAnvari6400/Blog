from django.urls import path
from .views import index_view,about_view,contact_view,notification_view,newsletter_view

app_name = 'website'

urlpatterns = [
    path('',index_view,name='index'),
    path('about',about_view,name='about'),
    path('contact',contact_view,name='contact'),
    path('notification',notification_view,name='notification'),
    path('newsletter',newsletter_view,name='newsletter')
]