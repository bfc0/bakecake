from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.views import View
from .forms import CustomUserCreationForm


class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, "register.html", {"form": form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
        return render(request, "register.html", {"form": form})


class CustomLoginView(LoginView):
    template_name = "login.html"
    next_page = "index"


class CustomLogoutView(View):
    next_page = "index"

    def get(self, request):
        logout(request)
        return redirect("index")


class JsLoginView(LoginView):
    def form_invalid(self, form):
        return JsonResponse({'success': False, 'error': "Неправильный телефон или пароль"})

    def form_valid(self, form):
        login(self.request, form.get_user())
        return JsonResponse({'success': True})
