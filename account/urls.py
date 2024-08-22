from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import CustomLoginView, RegisterView, CustomLogoutView, JsLoginView, ProfileView


urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", CustomLogoutView.as_view(next_page="index"), name="logout"),
    path("jslogin/", JsLoginView.as_view(), name="jslogin")
]
