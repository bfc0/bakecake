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
from orders.tasks import check_payment_status
from orders.utils import generate_context
from .payment import create_payment


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
        self.context = generate_context(request)
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
                phone_number=request.data["phone_number"],
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
        order = serializer.save()
        response_data = serializer.data.copy()
        response_data.pop("content_object", None)

        payment_id, url = create_payment(order.id, order.price)
        response_data["payment_url"] = url
        order.payment_id = payment_id
        order.save()

        check_payment_status(order.id)

        print(response_data)
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
