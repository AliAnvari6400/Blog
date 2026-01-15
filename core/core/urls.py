from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.sitemaps.views import sitemap
from website.sitemaps import StaticViewSitemap
from blog.sitemaps import BlogSitemap
import debug_toolbar

sitemaps = {"static": StaticViewSitemap, "blog": BlogSitemap}


# for api document
schema_view = get_schema_view(
    openapi.Info(
        title="Blog API",
        default_version="v1",
        description="API documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="a_anvari@ymail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("comment/", include("comment.urls")),
    path("accounts/", include("accounts.urls")),
    path("", include("accounts.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("website/", include("website.urls")),
    path("blog/", include("blog.urls")),
    path("post/", include("post.urls")),
    # your API endpoints here
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    path(
        "swagger.json",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("robots.txt", include("robots.urls")),
    path("__debug__/", include(debug_toolbar.urls)),
    path("summernote/", include("django_summernote.urls")),
    path("captcha/", include("captcha.urls")),
    path("maintenance/", include("config.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
