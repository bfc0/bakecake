import json
from django.contrib.auth import login
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import CustomUserCreationForm
from phonenumber_field.phonenumber import PhoneNumber

from orders.models import Order


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


@method_decorator(login_required, name="dispatch")
class ProfileView(View):
    template_name = "lk.html"

    def setup(self, request, *args, **kwargs):
        orders = Order.objects.filter(customer=request.user).all()
        serialized_orders = [order.serialize() for order in orders]
        self.context = {
            "orders": serialized_orders,
        }
        super().setup(request, *args, **kwargs)

    def get(self, request):
        u = {
            "phone_number": str(request.user.phone_number),
            "email": request.user.email,
            "name": request.user.name
        }

        return render(request, self.template_name, self.context)

    def post(self, request):
        name = request.POST.get('NAME')
        phone = request.POST.get('PHONE')
        email = request.POST.get('EMAIL')

        try:
            phone_number = PhoneNumber.from_string(phone)
            if not phone_number.is_valid():
                self.context["error"] = "Invalid phone number"
                return render(request, self.template_name, self.context)

            user = request.user
            user.name = name
            user.phone_number = phone_number
            user.email = email
            user.save()

        except Exception as e:
            user.refresh_from_db()
            self.context["error"] = "Failed to update user"
            return render(request, self.template_name, self.context)

        return render(request, self.template_name, self.context)
