from django.shortcuts import render
from cakes.models import CartAddition, Order


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
