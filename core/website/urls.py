from django.urls import path
from .views import IndexView, AboutView, ContactView, NotificationView, NewsletterView

app_name = "website"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("about", AboutView.as_view(), name="about"),
    path("contact", ContactView.as_view(), name="contact"),
    path("notification", NotificationView.as_view(), name="notification"),
    path("newsletter", NewsletterView.as_view(), name="newsletter"),
]
