from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path
from django.conf.urls.static import static


def placeholder_view(request):
    user_id = request.session.get("_auth_user_id")
    print(f"id is {user_id}")
    return HttpResponse(f"{request.user.is_authenticated=} {request.user}")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("account/", include("account.urls")),
    path("", placeholder_view, name="index")
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
