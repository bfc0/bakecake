from django.shortcuts import render
from django.views import View
from cakes.models import CartAddition, Order
from cakes.models import (
    Shape, Topping, Berry, Decoration, Level, Event, CustomCake, CatalogueCake
)


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

    Order.objects.create(user=user,
                         session_key=session_key,
                         total_amount=total_amount)


class IndexView(View):
    def setup(self):
        context = {
            "decorations": {

            }
        }
