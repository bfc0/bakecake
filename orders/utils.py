import cakes.models as m
from orders.models import Order
from django.contrib.auth.forms import AuthenticationForm


def generate_context(request):

    toppings = m.Topping.objects.all()
    shapes = m.Shape.objects.all()
    berries = m.Berry.objects.all()
    decors = m.Decoration.objects.all()
    levels = m.Level.objects.all()
    toppings = m.Topping.objects.all()

    address = email = name = phone = ""
    if request.user.is_authenticated:
        last_order = Order.objects.filter(customer=request.user).last()
        if last_order:
            address = last_order.address
            email = last_order.email
            name = last_order.customer_name
            phone = last_order.phone_number

    form = AuthenticationForm()

    context = {
        "DATA": {
            "Levels": ["не выбрано"]+[l.name for l in levels],
            "Forms": ["не выбрано"]+[s.name for s in shapes],
            "Toppings": ["не выбрано"]+[t.name for t in toppings],
            "Berries": ["нет"]+[b.name for b in berries],
            "Decors": ["нет"]+[d.name for d in decors],

            "lastorder": {
                "address": address,
                "email": email,
                "name": name,
                "phone": phone,
            },
        },
        "Costs": {
            "Levels": [0]+[l.price for l in levels],
            "Forms": [0]+[s.price for s in shapes],
            "Toppings": [0]+[t.price for t in toppings],
            "Berries": [0]+[b.price for b in berries],
            "Decors": [0]+[d.price for d in decors],
            "Words": 500,
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

    return context
