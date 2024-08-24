from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from orders.views import IndexView,  register_order

urlpatterns = [
    path("admin/", admin.site.urls),
    path("account/", include("account.urls")),
    path("", IndexView.as_view(), name="index"),
    path("api/order/", register_order, name="order"),
    path("cakes/", include("cakes.urls")),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
