from django.conf import settings
from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path
from django.conf.urls.static import static
from orders.views import IndexView,  register_order, OrderListView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("account/", include("account.urls")),
    path("", IndexView.as_view(), name="index"),
    path("api/order/", register_order, name="order"),
    path("manager/", OrderListView.as_view(), name="manager"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
