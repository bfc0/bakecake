from datetime import datetime, timedelta
import logging
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.utils import timezone
from django.views import View
from django.db import transaction
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from account.models import CustomUser
from cakes.models import CartAddition, CatalogueCake, adjust_cake_price
from cakes.models import Order as StatsOrder
from orders.serializers import CakeSerializer, OrderSerializer
from orders.models import Order


def add_to_cart(request, product):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
    session_key = request.session.session_key
    user = request.user if request.user.is_authenticated else None

    CartAddition.objects.create(user=user,
                                session_key=session_key,
                                product_name=product.name)


def create_order(request, total_amount):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
    session_key = request.session.session_key
    user = request.user if request.user.is_authenticated else None

    StatsOrder.objects.create(user=user,
                              session_key=session_key,
                              total_amount=total_amount)


class IndexView(View):
    def setup(self, request, *args, **kwargs):
        form = AuthenticationForm()

        address = email = name = phone = ""
        if request.user.is_authenticated:
            last_order = Order.objects.filter(customer=request.user).last()
            if last_order:
                address = last_order.address
                email = last_order.email
                name = last_order.customer_name
                phone = last_order.phone_number

        self.context = {
            "DATA": {
                "Levels": ['не выбрано', '1', '2', '3'],
                "Forms": ['не выбрано', 'Круг', 'Квадрат', 'Прямоугольник'],
                "Toppings": ['не выбрано', 'Без', 'Белый соус', 'Карамельный', 'Кленовый', 'Черничный', 'Молочный шоколад', 'Клубничный'],
                "Berries": ['нет', 'Ежевика', 'Малина', 'Голубика', 'Клубника'],
                "Decors": ['нет', 'Фисташки', 'Безе', 'Фундук',
                           'Пекан', 'Маршмеллоу', 'Марципан'],
                "lastorder": {
                    "address": address,
                    "email": email,
                    "name": name,
                    "phone": phone,
                },
            },
            "Costs": {
                "Levels": [0, 400, 750, 1100],
                "Forms": [0, 600, 400, 1000],
                "Toppings": [0, 0, 200, 180, 200, 300, 350, 200],
                "Berries": [0, 400, 300, 450, 500],
                "Decors": [0, 300, 400, 350, 300, 200, 280],
                "Words": 500
            },
            "ChosenCakeSpecs": {
                "Levels": 0,
                "Form": 0,
                "Toppings": 0,
                "Berries": 0,
                "Decors": 0,
            },
            "form": form,
        }
        super().setup(request, *args, **kwargs)

    def get(self, request):
        return render(request, "index.html", self.context)


@api_view(["POST"])
@transaction.atomic()
def register_order(request):
    logging.debug(request.data)
    print(request.data)
    try:
        if not request.user.is_authenticated:
            user = CustomUser.objects.create_user(
                phone_number=request.data["phone"],
                name=request.data["customer_name"],
                email=request.data["email"],
            )
            login(request, user)

        if cake_data := request.data.get("cataloguecake"):
            cake = CatalogueCake.objects.get(id=cake_data["id"])

        else:
            cake_data = request.data.pop("customcake")
            cake_serializer = CakeSerializer(data=cake_data)
            cake_serializer.is_valid(raise_exception=True)
            cake = cake_serializer.save()

        content_type = ContentType.objects.get_for_model(cake)

        desired_date = request.data["desired_date"]
        desired_time = request.data["desired_time"]
        desired_dt = datetime.strptime(
            f"{desired_date} {desired_time}", "%Y-%m-%d %H:%M")
        adjust_cake_price(cake, desired_dt)

        data = {
            "object_id": cake.id,
            "content_type": content_type.id,
            "content_object": cake,
            "price": cake.price,
            "customer": request.user.id,
            "preferred_date": desired_dt,
            ** request.data,
        }

        serializer = OrderSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = serializer.data.copy()
        response_data.pop("content_object", None)

    except Exception as e:
        logging.error(e)
        return Response({"error": "Ошибка при добавлении заказа"}, status=400)
    return Response(response_data, status=201)


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "manager.html"

    def get_queryset(self) -> QuerySet:
        return Order.objects.order_by("-date_created")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = self.get_queryset()
        serialized = [o.serialize for o in orders]
        context["orders"] = serialized
        return context
