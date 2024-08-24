from django.urls import path
from cakes import views
from orders.views import IndexView


urlpatterns = [
    path("catalogue/", views.catalogue, name="catalogue"),
    path("", IndexView.as_view(), name="index"),
    
]
