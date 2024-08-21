from django.conf import settings
from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path
from django.conf.urls.static import static


def placeholder_view(request):
    return render(request, "index.html")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("account/", include("account.urls")),
    path("", placeholder_view, name="index")
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
